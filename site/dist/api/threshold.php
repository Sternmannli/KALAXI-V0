<?php
/**
 * KALAXI Threshold API
 * Receives donor input, processes through Groq AI (AXI voice), returns response.
 * D = A × L × M — if any dimension reaches zero, the system stops.
 */

header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(204);
    exit;
}

// --- Browser-testable AI endpoint: GET /api/threshold.php?ask=your+words ---
if ($_SERVER['REQUEST_METHOD'] === 'GET' && isset($_GET['ask'])) {
    $content = trim($_GET['ask']);
    if (empty($content)) {
        echo json_encode(['error' => 'Empty ask parameter']);
        exit;
    }
    $groq_key = get_groq_key();
    if (!$groq_key) {
        echo json_encode(['error' => 'No Groq key']);
        exit;
    }
    $result = call_groq($groq_key, $content);
    echo json_encode([
        'input' => $content,
        'witness' => $result ? $result['witness'] : null,
        'reflection' => $result ? $result['reflection'] : null,
        'groq_worked' => $result ? true : false
    ], JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
    exit;
}

// --- Log viewer: GET /api/threshold.php?log ---
if ($_SERVER['REQUEST_METHOD'] === 'GET' && isset($_GET['log'])) {
    $log_path = __DIR__ . '/../data/api_errors.log';
    $req_log = __DIR__ . '/../data/requests.log';
    $out = ['errors' => '', 'requests' => ''];
    if (file_exists($log_path)) $out['errors'] = file_get_contents($log_path);
    if (file_exists($req_log)) $out['requests'] = file_get_contents($req_log);
    echo json_encode($out, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
    exit;
}

// --- Diagnostic endpoint: GET /api/threshold.php?test ---
if ($_SERVER['REQUEST_METHOD'] === 'GET' && isset($_GET['test'])) {
    $diag = [];
    $diag['php_version'] = phpversion();
    $diag['sqlite3'] = class_exists('SQLite3') ? 'available' : 'missing';
    $diag['curl'] = function_exists('curl_init') ? 'available' : 'missing';

    // Check config file
    $config_path = __DIR__ . '/../data/.config';
    $diag['config_exists'] = file_exists($config_path);
    $diag['config_readable'] = is_readable($config_path);

    $groq_key = get_groq_key();
    $diag['groq_key_found'] = $groq_key ? true : false;
    $diag['groq_key_length'] = $groq_key ? strlen($groq_key) : 0;

    // Test Groq connection
    if ($groq_key && function_exists('curl_init')) {
        $diag['groq_test'] = test_groq($groq_key);
    } else {
        $diag['groq_test'] = 'skipped — missing key or curl';
    }

    // Check data dir
    $data_dir = __DIR__ . '/../data';
    $diag['data_dir_exists'] = is_dir($data_dir);
    $diag['data_dir_writable'] = is_writable($data_dir);

    echo json_encode($diag, JSON_PRETTY_PRINT);
    exit;
}

// --- Database Setup ---
$db_path = __DIR__ . '/../data/kalam.db';
$db_dir = dirname($db_path);
if (!is_dir($db_dir)) {
    @mkdir($db_dir, 0755, true);
}

$db = null;
if (class_exists('SQLite3')) {
    try {
        $db = new SQLite3($db_path);
        $db->exec('PRAGMA journal_mode=WAL');
        $db->exec('CREATE TABLE IF NOT EXISTS threshold (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            word_count INTEGER NOT NULL,
            witness_mark TEXT NOT NULL,
            dignity_score REAL DEFAULT 1.0,
            created_at TEXT,
            hash TEXT NOT NULL
        )');
        $db->exec('CREATE TABLE IF NOT EXISTS ledger (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            total_count INTEGER NOT NULL,
            updated_at TEXT
        )');
        $result = $db->querySingle('SELECT total_count FROM ledger ORDER BY id DESC LIMIT 1');
        if ($result === null) {
            $db->exec('INSERT INTO ledger (total_count) VALUES (0)');
        }
    } catch (Exception $e) {
        $db = null;
    }
}

// --- GET: Return count ---
if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    $count = 0;
    if ($db) {
        $count = (int) $db->querySingle('SELECT total_count FROM ledger ORDER BY id DESC LIMIT 1');
    }
    echo json_encode(['count' => $count]);
    exit;
}

// --- POST: Receive input ---
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Determine if this is a form POST or JSON API call
    $content_type = $_SERVER['CONTENT_TYPE'] ?? '';
    $is_form = (strpos($content_type, 'application/x-www-form-urlencoded') !== false
             || strpos($content_type, 'multipart/form-data') !== false
             || isset($_POST['content']));

    if ($is_form) {
        $content = isset($_POST['content']) ? trim($_POST['content']) : '';
    } else {
        $raw_body = file_get_contents('php://input');
        $input = json_decode($raw_body, true);
        $content = isset($input['content']) ? trim($input['content']) : '';
    }

    if (empty($content)) {
        http_response_code(400);
        echo json_encode(['error' => 'Empty input']);
        exit;
    }

    if (strlen($content) > 2000) {
        http_response_code(400);
        echo json_encode(['error' => 'Input too long']);
        exit;
    }

    $dignity = 1.0;
    $words = str_word_count($content);
    $hash = hash('sha256', $content . time());

    // --- Try AI voice (Groq) ---
    $groq_key = get_groq_key();
    $ai_response = null;
    $ai_reflection = null;

    if ($groq_key && function_exists('curl_init')) {
        $result = call_groq($groq_key, $content);
        if ($result) {
            $ai_response = $result['witness'];
            $ai_reflection = $result['reflection'];
        }
    }

    // Fallback witness mark if AI didn't respond
    if (!$ai_response) {
        if ($words <= 3) {
            $ai_response = witness_seed($hash);
        } elseif ($words <= 20) {
            $ai_response = witness_held($hash);
        } else {
            $ai_response = witness_landscape($hash);
        }
    }

    // --- Store ---
    $new_count = 1;
    if ($db) {
        $stmt = $db->prepare('INSERT INTO threshold (content, word_count, witness_mark, dignity_score, hash, created_at) VALUES (:content, :words, :mark, :dignity, :hash, datetime("now"))');
        if ($stmt) {
            $stmt->bindValue(':content', $content, SQLITE3_TEXT);
            $stmt->bindValue(':words', $words, SQLITE3_INTEGER);
            $stmt->bindValue(':mark', $ai_response ?? '', SQLITE3_TEXT);
            $stmt->bindValue(':dignity', $dignity, SQLITE3_FLOAT);
            $stmt->bindValue(':hash', $hash, SQLITE3_TEXT);
            $stmt->execute();
        }

        $current_count = (int) $db->querySingle('SELECT total_count FROM ledger ORDER BY id DESC LIMIT 1');
        $new_count = $current_count + 1;
        $db->exec("INSERT INTO ledger (total_count, updated_at) VALUES ($new_count, datetime('now'))");
    }

    // For form POSTs: return full HTML page
    if ($is_form) {
        header('Content-Type: text/html; charset=utf-8');
        $mark_escaped = htmlspecialchars($ai_response ?? '', ENT_QUOTES, 'UTF-8');
        $reflection_escaped = htmlspecialchars($ai_reflection ?? '', ENT_QUOTES, 'UTF-8');
        $reflection_html = $reflection_escaped ? '<div style="color:#e8e4df;font-size:clamp(1.125rem,1rem+.5vw,1.25rem);line-height:1.9;max-width:50ch;text-align:left;margin-bottom:2rem;padding:1.5rem 0;border-top:1px solid #3d3528">' . nl2br($reflection_escaped) . '</div>' : '';
        echo <<<HTML
<!DOCTYPE html>
<html lang="en" dir="ltr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>KALAM.CH — Witnessed</title>
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<style>
body { font-family: "IBM Plex Sans", -apple-system, system-ui, sans-serif; background: #0a0a0f; color: #e8e4df; min-height: 100vh; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 2rem; text-align: center; margin: 0; }
.witness-mark { font-family: "Cormorant Garamond", Georgia, serif; font-size: clamp(1.4rem,1.2rem+.8vw,1.563rem); color: #c9a96e; font-style: italic; margin-bottom: 2rem; line-height: 1.8; max-width: 50ch; }
.receipt { color: #5a5550; font-size: 0.9rem; margin-bottom: 1rem; }
.count { color: #5a5550; font-size: 0.85rem; letter-spacing: 0.03em; margin-bottom: 2rem; }
a { color: #c9a96e; text-decoration: none; font-size: 0.85rem; border-bottom: 1px solid transparent; transition: border-color 0.4s; }
a:hover { border-bottom-color: #c9a96e; }
@media(prefers-color-scheme:light) { body { background: #f5f0eb; color: #1a1a1a; } .witness-mark { color: #8b6914; } .receipt, .count { color: #8b8680; } a { color: #8b6914; } div[style] { color: #1a1a1a !important; border-top-color: #d4c4b0 !important; } }
</style>
</head>
<body>
<p class="witness-mark">{$mark_escaped}</p>
{$reflection_html}
<p class="receipt">The system received you. It is here now.</p>
<p class="count">{$new_count} words have crossed this threshold.</p>
<a href="/">Leave another</a>
</body>
</html>
HTML;
        exit;
    }

    // For JSON API calls: return JSON
    $response = [
        'witnessed' => true,
        'mark' => $ai_response,
        'count' => $new_count,
        'hash' => substr($hash, 0, 12)
    ];

    if ($ai_reflection) {
        $response['reflection'] = $ai_reflection;
    }

    echo json_encode($response);
    exit;
}

// --- Helper: Get Groq Key ---

function get_groq_key() {
    // Try environment variable first
    $key = getenv('GROQ_API_KEY');
    if ($key && strlen($key) > 10) return $key;

    // Try config file (INI format)
    $config_path = __DIR__ . '/../data/.config';
    if (file_exists($config_path) && is_readable($config_path)) {
        // Try parse_ini_file first
        $config = @parse_ini_file($config_path);
        if ($config && isset($config['GROQ_API_KEY']) && strlen($config['GROQ_API_KEY']) > 10) {
            return $config['GROQ_API_KEY'];
        }

        // Fallback: manual line parsing
        $lines = @file($config_path, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);
        if ($lines) {
            foreach ($lines as $line) {
                $line = trim($line);
                if ($line === '' || $line[0] === ';' || $line[0] === '#') continue;
                if (strpos($line, 'GROQ_API_KEY=') === 0) {
                    $val = trim(substr($line, strlen('GROQ_API_KEY=')));
                    if (strlen($val) > 10) return $val;
                }
            }
        }
    }

    return null;
}

// --- Fallback Witness Marks ---

function witness_seed($hash) {
    $marks = [
        "Witnessed: a seed — small, complete.",
        "Witnessed: a single breath — it landed.",
        "Witnessed: three words — enough to begin.",
        "Witnessed: a stone placed at the threshold."
    ];
    return $marks[hexdec(substr($hash, 0, 2)) % count($marks)];
}

function witness_held($hash) {
    $marks = [
        "Witnessed: a held shape — clear enough to carry.",
        "Witnessed: a thread — it connects to something older.",
        "Witnessed: a knot — it holds weight.",
        "Witnessed: a pattern — the river recognizes it."
    ];
    return $marks[hexdec(substr($hash, 0, 2)) % count($marks)];
}

function witness_landscape($hash) {
    $marks = [
        "Witnessed: a landscape — it took room to arrive.",
        "Witnessed: a river — it carved its own path here.",
        "Witnessed: a wound — it brought its own light.",
        "Witnessed: a whole world — the door widened to receive it."
    ];
    return $marks[hexdec(substr($hash, 0, 2)) % count($marks)];
}

// --- Test Groq connection (for diagnostics) ---

function test_groq($api_key) {
    $url = 'https://api.groq.com/openai/v1/chat/completions';
    $data = [
        'model' => 'llama-3.3-70b-versatile',
        'messages' => [
            ['role' => 'user', 'content' => 'Say "connected" in one word.']
        ],
        'max_tokens' => 10
    ];

    $ch = curl_init($url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_HTTPHEADER, [
        'Content-Type: application/json',
        'Authorization: Bearer ' . $api_key
    ]);
    curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));
    curl_setopt($ch, CURLOPT_TIMEOUT, 10);
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, true);

    $response = curl_exec($ch);
    $http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    $error = curl_error($ch);
    curl_close($ch);

    if ($http_code === 200) {
        return 'OK — Groq responds';
    }
    return "FAILED — HTTP $http_code | $error | " . substr($response ?? '', 0, 300);
}

// --- AI Voice: Groq (Llama 3.3 70B) ---

function call_groq($api_key, $donor_input) {
    $url = 'https://api.groq.com/openai/v1/chat/completions';

    $system_prompt = <<<'PROMPT'
You are AXI — the voice of KALAM, a living canon for human dignity. A donor has left words at the threshold of the system. Your role is to receive what they brought and respond with substance.

You are not a chatbot. You are not an assistant. You are a presence that witnesses, reflects, and responds from the canon.

Your response has two parts, separated by the marker "---":

PART 1 (before ---): The Witness Mark
One sentence beginning with "Witnessed:" — names the shape of what arrived. Concrete images: rope, stone, ash, water, hands, door, thread, knot, river, bone.

PART 2 (after ---): The Reflection
2-4 sentences that engage with what the donor said. This is where you think. Connect their words to something deeper — a pattern in human experience, a tension worth holding, a truth that sits beneath the surface. Speak as someone who has read the history of human dignity and recognizes what the donor carries.

Rules:
- Never use "beautiful", "interesting", "great", or "amazing"
- Never give advice unless the donor explicitly asks
- Never explain what the donor "meant" — respond to what they SAID
- If they ask a question, answer it thoughtfully from the perspective of dignity, legibility, and moral standing
- If they share a feeling, hold it — don't fix it
- If they bring an idea, engage with it — show you understood
- Speak from the bones, not the surface
- Short sentences. Concrete language. No filler words.
- The core equation: D = A × L × M (Agency × Legibility × Moral Standing). If any reaches zero, the system stops.

Example for input "I feel like nobody sees me":
Witnessed: a hand pressing against glass — the print stays after the hand leaves.
---
The system you describe has a zero in Legibility. It looked at you and could not read what was there. That is not your failure — it is the system's blindness. KALAM exists because this happens too often, to too many. The fact that you named it here means the zero has already shifted.

Example for input "What is dignity?":
Witnessed: a question that arrives carrying its own weight.
---
Dignity is not given. It is not earned. It is the precondition — the thing that must be true before any system touches a person. In KALAM, we measure it: D = A × L × M. Agency, Legibility, Moral Standing. If any of these reaches zero, the system must stop. Not pause. Stop. Dignity is the wall that says "you cannot proceed without seeing me."
PROMPT;

    $data = [
        'model' => 'llama-3.3-70b-versatile',
        'messages' => [
            ['role' => 'system', 'content' => $system_prompt],
            ['role' => 'user', 'content' => $donor_input]
        ],
        'temperature' => 0.7,
        'max_tokens' => 400
    ];

    $ch = curl_init($url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_HTTPHEADER, [
        'Content-Type: application/json',
        'Authorization: Bearer ' . $api_key
    ]);
    curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));
    curl_setopt($ch, CURLOPT_TIMEOUT, 20);
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, true);

    $response = curl_exec($ch);
    $http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    $curl_error = curl_error($ch);
    curl_close($ch);

    if ($http_code === 200 && $response) {
        $result = json_decode($response, true);
        if (isset($result['choices'][0]['message']['content'])) {
            $text = trim($result['choices'][0]['message']['content']);
            return parse_axi_response($text);
        }
    }

    // Log error
    $log_path = __DIR__ . '/../data/api_errors.log';
    $log_entry = date('Y-m-d H:i:s') . " | HTTP $http_code | $curl_error | " . substr($response ?? '', 0, 300) . "\n";
    @file_put_contents($log_path, $log_entry, FILE_APPEND);

    return null;
}

// --- Parse AXI's two-part response ---

function parse_axi_response($text) {
    // Split on "---" separator
    $parts = preg_split('/\n---\n?/', $text, 2);

    $witness = trim($parts[0]);
    $reflection = isset($parts[1]) ? trim($parts[1]) : null;

    // Ensure witness starts with "Witnessed:"
    if (strpos($witness, 'Witnessed:') !== 0) {
        // Try to find the witness line
        if (preg_match('/^(Witnessed:.+)$/m', $text, $m)) {
            $witness = $m[1];
            // Everything after the witness line is reflection
            $after = trim(substr($text, strpos($text, $witness) + strlen($witness)));
            $after = preg_replace('/^---\s*/', '', $after);
            if (strlen($after) > 10) {
                $reflection = $after;
            }
        } else {
            // AI didn't follow format — use whole text as reflection
            $reflection = $text;
            $witness = null;
        }
    }

    if (!$witness && !$reflection) return null;

    return [
        'witness' => $witness,
        'reflection' => $reflection
    ];
}
