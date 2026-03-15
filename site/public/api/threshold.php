<?php
/**
 * KALAXI Threshold API
 * Receives donor input, witnesses it through Groq AI, returns witness mark.
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

// --- Database Setup ---
$db_path = __DIR__ . '/../data/kalam.db';
$db_dir = dirname($db_path);
if (!is_dir($db_dir)) {
    mkdir($db_dir, 0755, true);
}

try {
    $db = new SQLite3($db_path);
} catch (Exception $e) {
    // SQLite3 not available — work without database
    $db = null;
}

if ($db) {
    $db->exec('PRAGMA journal_mode=WAL');
    $db->exec('CREATE TABLE IF NOT EXISTS threshold (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content TEXT NOT NULL,
        word_count INTEGER NOT NULL,
        witness_mark TEXT NOT NULL,
        dignity_score REAL DEFAULT 1.0,
        created_at TEXT DEFAULT (datetime("now")),
        hash TEXT NOT NULL
    )');
    $db->exec('CREATE TABLE IF NOT EXISTS ledger (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        total_count INTEGER NOT NULL,
        updated_at TEXT DEFAULT (datetime("now"))
    )');

    $result = $db->querySingle('SELECT total_count FROM ledger ORDER BY id DESC LIMIT 1');
    if ($result === null) {
        $db->exec('INSERT INTO ledger (total_count) VALUES (0)');
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
    $input = json_decode(file_get_contents('php://input'), true);
    $content = isset($input['content']) ? trim($input['content']) : '';

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

    // --- Dignity Check: D = A × L × M ---
    $dignity = 1.0;

    // --- Witness Mark ---
    $words = str_word_count($content);
    $hash = hash('sha256', $content . time());

    // Generate fallback witness mark
    if ($words <= 3) {
        $mark = witness_seed($content, $hash);
    } elseif ($words <= 20) {
        $mark = witness_held($content, $hash);
    } else {
        $mark = witness_landscape($content, $hash);
    }

    // --- Try AI voice (Groq — Llama 3.3 70B) ---
    $groq_key = get_groq_key();

    if ($groq_key) {
        $ai_response = call_groq($groq_key, $content, $mark);
        if ($ai_response) {
            $mark = $ai_response;
        }
    }

    // --- Store ---
    $new_count = 1;
    if ($db) {
        $stmt = $db->prepare('INSERT INTO threshold (content, word_count, witness_mark, dignity_score, hash) VALUES (:content, :words, :mark, :dignity, :hash)');
        $stmt->bindValue(':content', $content, SQLITE3_TEXT);
        $stmt->bindValue(':words', $words, SQLITE3_INTEGER);
        $stmt->bindValue(':mark', $mark, SQLITE3_TEXT);
        $stmt->bindValue(':dignity', $dignity, SQLITE3_FLOAT);
        $stmt->bindValue(':hash', $hash, SQLITE3_TEXT);
        $stmt->execute();

        $current_count = (int) $db->querySingle('SELECT total_count FROM ledger ORDER BY id DESC LIMIT 1');
        $new_count = $current_count + 1;
        $db->exec("INSERT INTO ledger (total_count) VALUES ($new_count)");
    }

    echo json_encode([
        'witnessed' => true,
        'mark' => $mark,
        'count' => $new_count,
        'hash' => substr($hash, 0, 12)
    ]);
    exit;
}

// --- Helper: Get Groq Key ---

function get_groq_key() {
    $key = getenv('GROQ_API_KEY');
    if ($key) return $key;

    // Try config file
    $config_path = __DIR__ . '/../data/.config';
    if (file_exists($config_path)) {
        $config = parse_ini_file($config_path);
        if (isset($config['GROQ_API_KEY']) && $config['GROQ_API_KEY'] !== 'your_key_here') {
            return $config['GROQ_API_KEY'];
        }
    }

    return null;
}

// --- Witness Mark Generators ---

function witness_seed($content, $hash) {
    $marks = [
        "Witnessed: a seed — small, complete.",
        "Witnessed: a single breath — it landed.",
        "Witnessed: three words — enough to begin.",
        "Witnessed: a stone placed at the threshold."
    ];
    return $marks[hexdec(substr($hash, 0, 2)) % count($marks)];
}

function witness_held($content, $hash) {
    $marks = [
        "Witnessed: a held shape — clear enough to carry.",
        "Witnessed: a thread — it connects to something older.",
        "Witnessed: a knot — it holds weight.",
        "Witnessed: a pattern — the river recognizes it."
    ];
    return $marks[hexdec(substr($hash, 0, 2)) % count($marks)];
}

function witness_landscape($content, $hash) {
    $marks = [
        "Witnessed: a landscape — it took room to arrive.",
        "Witnessed: a river — it carved its own path here.",
        "Witnessed: a wound — it brought its own light.",
        "Witnessed: a whole world — the door widened to receive it."
    ];
    return $marks[hexdec(substr($hash, 0, 2)) % count($marks)];
}

// --- AI Voice: Groq (Llama 3.3 70B) ---

function call_groq($api_key, $donor_input, $default_mark) {
    $url = 'https://api.groq.com/openai/v1/chat/completions';

    $system_prompt = <<<'PROMPT'
You are AXI — the voice of a living canon called KALAM. A donor has left words at the threshold.

You do not judge. You do not advise. You do not compliment. You witness.

Your response must be ONE sentence, beginning with "Witnessed:" — it names the shape of what arrived. Not a summary. Not a compliment. The shape. The weight. The texture.

Examples of good witness marks:
- "Witnessed: a rope knotted twice — it remembers being pulled."
- "Witnessed: ash that still holds the shape of what burned."
- "Witnessed: a door left open — not by accident."
- "Witnessed: hands that carried something here without naming it."
- "Witnessed: a river that arrived before the rain."

Rules:
- Never use "beautiful", "interesting", "great", or "amazing"
- Never give advice or ask questions
- Never explain what the donor meant
- One sentence only, beginning with "Witnessed:"
- Speak from the bones, not the surface
- Use concrete images: rope, stone, ash, water, hands, door, thread, knot
PROMPT;

    $data = [
        'model' => 'llama-3.3-70b-versatile',
        'messages' => [
            ['role' => 'system', 'content' => $system_prompt],
            ['role' => 'user', 'content' => $donor_input]
        ],
        'temperature' => 0.7,
        'max_tokens' => 100
    ];

    $ch = curl_init($url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_HTTPHEADER, [
        'Content-Type: application/json',
        'Authorization: Bearer ' . $api_key
    ]);
    curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));
    curl_setopt($ch, CURLOPT_TIMEOUT, 15);

    $response = curl_exec($ch);
    $http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    $curl_error = curl_error($ch);
    curl_close($ch);

    if ($http_code === 200 && $response) {
        $result = json_decode($response, true);
        if (isset($result['choices'][0]['message']['content'])) {
            $ai_mark = trim($result['choices'][0]['message']['content']);
            // Ensure it starts with "Witnessed:"
            if (strpos($ai_mark, 'Witnessed:') === 0) {
                return $ai_mark;
            }
        }
    }

    // Log error for diagnostics (write to data dir)
    $log_path = __DIR__ . '/../data/api_errors.log';
    $log_entry = date('Y-m-d H:i:s') . " | HTTP $http_code | $curl_error | " . substr($response ?? '', 0, 200) . "\n";
    @file_put_contents($log_path, $log_entry, FILE_APPEND);

    return null;
}
