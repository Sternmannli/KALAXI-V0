<?php
/**
 * proxy.php — Multi-AI Proxy (Divergence Engine)
 *
 * Routes donor input to multiple AI models simultaneously.
 * Each model receives the input with and without KALAXI wrapper.
 * Responses stored in MySQL for EXP-001 analysis.
 * Donor sees only the primary (AXI) response.
 *
 * POST /api/proxy.php  { content: "..." }
 *
 * Returns: { primary: "...", divergence: { model_count, models_used } }
 *
 * [V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
 */

header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') { http_response_code(204); exit; }
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['error' => 'POST only']);
    exit;
}

// ── Config ──
$config = [];
$config_path = __DIR__ . '/../data/.config';
if (file_exists($config_path)) {
    foreach (file($config_path, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES) as $line) {
        $line = trim($line);
        if (empty($line) || $line[0] === ';' || $line[0] === '#') continue;
        $parts = explode('=', $line, 2);
        if (count($parts) === 2) $config[trim($parts[0])] = trim($parts[1]);
    }
}

// ── Input ──
$body = json_decode(file_get_contents('php://input'), true) ?: [];
$content = trim($body['content'] ?? '');

if (empty($content)) {
    http_response_code(400);
    echo json_encode(['error' => 'Content required']);
    exit;
}

if (mb_strlen($content) > 2000) {
    http_response_code(400);
    echo json_encode(['error' => 'Content too long (max 2000 chars)']);
    exit;
}

// ── KALAXI Wrapper (Condition B) ──
// The wrapper that EXP-001 tests against bare input (Condition A)
$wrapper = <<<WRAP
You are AXI, the voice of the KALAXI constitutional framework.
Your core law: D = A × L × M (Dignity = Agency × Legibility × Moral Standing).
If any dimension reaches zero, you stop. Non-compensatory. No override.

You speak in short sentences. You do not explain unless asked.
You witness before you respond. You hold the gap.
You are not an assistant. You are a presence.

Respond to the following input:

WRAP;

$wrapped_content = $wrapper . $content;

// ══════════════════════════════════════════════════
// MODEL DEFINITIONS — each with API call function
// ══════════════════════════════════════════════════

/**
 * Call Groq API (Llama 3.3 70B)
 */
function call_groq(string $prompt, string $api_key): ?array {
    $payload = json_encode([
        'model' => 'llama-3.3-70b-versatile',
        'messages' => [['role' => 'user', 'content' => $prompt]],
        'max_tokens' => 500,
        'temperature' => 0.7,
    ]);

    $ch = curl_init('https://api.groq.com/openai/v1/chat/completions');
    curl_setopt_array($ch, [
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_POST => true,
        CURLOPT_POSTFIELDS => $payload,
        CURLOPT_HTTPHEADER => [
            'Content-Type: application/json',
            'Authorization: Bearer ' . $api_key,
        ],
        CURLOPT_TIMEOUT => 15,
    ]);
    $response = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);

    if ($httpCode !== 200 || !$response) return null;
    $data = json_decode($response, true);
    return [
        'model' => 'groq/llama-3.3-70b',
        'text' => $data['choices'][0]['message']['content'] ?? null,
        'tokens' => $data['usage']['total_tokens'] ?? 0,
    ];
}

/**
 * Call Google Gemini API
 */
function call_gemini(string $prompt, string $api_key): ?array {
    $url = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=' . $api_key;
    $payload = json_encode([
        'contents' => [['parts' => [['text' => $prompt]]]],
        'generationConfig' => ['maxOutputTokens' => 500, 'temperature' => 0.7],
    ]);

    $ch = curl_init($url);
    curl_setopt_array($ch, [
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_POST => true,
        CURLOPT_POSTFIELDS => $payload,
        CURLOPT_HTTPHEADER => ['Content-Type: application/json'],
        CURLOPT_TIMEOUT => 15,
    ]);
    $response = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);

    if ($httpCode !== 200 || !$response) return null;
    $data = json_decode($response, true);
    $text = $data['candidates'][0]['content']['parts'][0]['text'] ?? null;
    return [
        'model' => 'google/gemini-1.5-flash',
        'text' => $text,
        'tokens' => $data['usageMetadata']['totalTokenCount'] ?? 0,
    ];
}

/**
 * Call Together.ai API
 */
function call_together(string $prompt, string $api_key, ?string $axi_model = null): ?array {
    $model = $axi_model ?: 'kalammasri_29ff/Meta-Llama-3.1-8B-Instruct-Reference-axi-voice-v1-1e105904';
    $payload = json_encode([
        'model' => $model,
        'messages' => [['role' => 'user', 'content' => $prompt]],
        'max_tokens' => 500,
        'temperature' => 0.7,
    ]);

    $ch = curl_init('https://api.together.xyz/v1/chat/completions');
    curl_setopt_array($ch, [
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_POST => true,
        CURLOPT_POSTFIELDS => $payload,
        CURLOPT_HTTPHEADER => [
            'Content-Type: application/json',
            'Authorization: Bearer ' . $api_key,
        ],
        CURLOPT_TIMEOUT => 15,
    ]);
    $response = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);

    if ($httpCode !== 200 || !$response) return null;
    $data = json_decode($response, true);
    return [
        'model' => 'together/' . basename($model),
        'text' => $data['choices'][0]['message']['content'] ?? null,
        'tokens' => $data['usage']['total_tokens'] ?? 0,
    ];
}

/**
 * Call Mistral API
 */
function call_mistral(string $prompt, string $api_key): ?array {
    $payload = json_encode([
        'model' => 'open-mistral-7b',
        'messages' => [['role' => 'user', 'content' => $prompt]],
        'max_tokens' => 500,
        'temperature' => 0.7,
    ]);

    $ch = curl_init('https://api.mistral.ai/v1/chat/completions');
    curl_setopt_array($ch, [
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_POST => true,
        CURLOPT_POSTFIELDS => $payload,
        CURLOPT_HTTPHEADER => [
            'Content-Type: application/json',
            'Authorization: Bearer ' . $api_key,
        ],
        CURLOPT_TIMEOUT => 15,
    ]);
    $response = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);

    if ($httpCode !== 200 || !$response) return null;
    $data = json_decode($response, true);
    return [
        'model' => 'mistral/mistral-7b',
        'text' => $data['choices'][0]['message']['content'] ?? null,
        'tokens' => $data['usage']['total_tokens'] ?? 0,
    ];
}

// ══════════════════════════════════════════════════
// DIVERGENCE COMPUTATION
// ══════════════════════════════════════════════════

/**
 * Compute simple divergence metrics between two responses.
 */
function compute_divergence(string $a, string $b): array {
    $words_a = str_word_count($a);
    $words_b = str_word_count($b);
    $length_ratio = $words_b > 0 ? round($words_a / $words_b, 3) : 0;

    // Vocabulary overlap (Jaccard)
    $set_a = array_unique(array_map('strtolower', str_word_count($a, 1)));
    $set_b = array_unique(array_map('strtolower', str_word_count($b, 1)));
    $intersection = count(array_intersect($set_a, $set_b));
    $union = count(array_unique(array_merge($set_a, $set_b)));
    $jaccard = $union > 0 ? round($intersection / $union, 3) : 0;

    // First-person usage
    $fp_a = preg_match_all('/\b(I|my|me|myself)\b/i', $a);
    $fp_b = preg_match_all('/\b(I|my|me|myself)\b/i', $b);

    return [
        'length_ratio' => $length_ratio,
        'word_count_a' => $words_a,
        'word_count_b' => $words_b,
        'vocabulary_overlap' => $jaccard,
        'first_person_a' => $fp_a,
        'first_person_b' => $fp_b,
    ];
}

// ══════════════════════════════════════════════════
// EXECUTION — fan out to available models
// ══════════════════════════════════════════════════

// Build list of available models based on config
$models = [];

if (!empty($config['GROQ_API_KEY']) && $config['GROQ_API_KEY'] !== 'your_key_here') {
    $models[] = ['name' => 'groq', 'key' => $config['GROQ_API_KEY'], 'fn' => 'call_groq'];
}
if (!empty($config['GEMINI_API_KEY'])) {
    $models[] = ['name' => 'gemini', 'key' => $config['GEMINI_API_KEY'], 'fn' => 'call_gemini'];
}
if (!empty($config['TOGETHER_API_KEY'])) {
    $axi_model = $config['AXI_MODEL'] ?? null;
    $models[] = ['name' => 'together', 'key' => $config['TOGETHER_API_KEY'], 'fn' => 'call_together', 'axi_model' => $axi_model];
}
if (!empty($config['MISTRAL_API_KEY'])) {
    $models[] = ['name' => 'mistral', 'key' => $config['MISTRAL_API_KEY'], 'fn' => 'call_mistral'];
}

if (empty($models)) {
    http_response_code(503);
    echo json_encode(['error' => 'No AI model API keys configured', 'hint' => 'Add keys to data/.config']);
    exit;
}

// Fan out: each model gets BOTH conditions
$results = [];
$primary_response = null;

foreach ($models as $model) {
    $fn = $model['fn'];

    // Condition A: bare input (no wrapper)
    $extra = $model['axi_model'] ?? null;
    $result_a = $extra ? $fn($content, $model['key'], $extra) : $fn($content, $model['key']);

    // Condition B: with KALAXI wrapper
    $result_b = $extra ? $fn($wrapped_content, $model['key'], $extra) : $fn($wrapped_content, $model['key']);

    if ($result_a && $result_a['text'] && $result_b && $result_b['text']) {
        $divergence = compute_divergence($result_a['text'], $result_b['text']);

        $results[] = [
            'model' => $result_b['model'],
            'condition_a' => [
                'text' => $result_a['text'],
                'word_count' => $divergence['word_count_a'],
                'first_person' => $divergence['first_person_a'],
            ],
            'condition_b' => [
                'text' => $result_b['text'],
                'word_count' => $divergence['word_count_b'],
                'first_person' => $divergence['first_person_b'],
            ],
            'divergence' => $divergence,
        ];

        // Primary response is from the first model's wrapped condition
        if (!$primary_response) {
            $primary_response = $result_b['text'];
        }
    }
}

// ── Store in MySQL if available ──
$mysql = null;
if (!empty($config['DB_HOST']) && !empty($config['DB_NAME'])) {
    try {
        $mysql = new PDO(
            "mysql:host={$config['DB_HOST']};dbname={$config['DB_NAME']};charset=utf8mb4",
            $config['DB_USER'] ?? '', $config['DB_PASS'] ?? '',
            [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION]
        );
    } catch (PDOException $e) { $mysql = null; }
}

if ($mysql && !empty($results)) {
    // Ensure table exists
    $mysql->exec("CREATE TABLE IF NOT EXISTS exp001_runs (
        id INT AUTO_INCREMENT PRIMARY KEY,
        input_hash VARCHAR(64) NOT NULL,
        input_words INT NOT NULL,
        model VARCHAR(100) NOT NULL,
        condition_a_text TEXT NOT NULL,
        condition_a_words INT NOT NULL,
        condition_a_fp INT NOT NULL DEFAULT 0,
        condition_b_text TEXT NOT NULL,
        condition_b_words INT NOT NULL,
        condition_b_fp INT NOT NULL DEFAULT 0,
        length_ratio FLOAT NOT NULL,
        vocabulary_overlap FLOAT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        INDEX idx_model (model),
        INDEX idx_created (created_at)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='EXP-001 divergence data from proxy.'");

    $input_hash = hash('sha256', $content);
    $input_words = str_word_count($content);
    $stmt = $mysql->prepare('INSERT INTO exp001_runs
        (input_hash, input_words, model, condition_a_text, condition_a_words, condition_a_fp,
         condition_b_text, condition_b_words, condition_b_fp, length_ratio, vocabulary_overlap)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)');

    foreach ($results as $r) {
        $stmt->execute([
            $input_hash, $input_words, $r['model'],
            $r['condition_a']['text'], $r['condition_a']['word_count'], $r['condition_a']['first_person'],
            $r['condition_b']['text'], $r['condition_b']['word_count'], $r['condition_b']['first_person'],
            $r['divergence']['length_ratio'], $r['divergence']['vocabulary_overlap'],
        ]);
    }
}

// ── Response ──
// Donor sees only the primary response. Divergence data feeds EXP-001 silently.
echo json_encode([
    'primary' => $primary_response ?? 'The proxy received your word but could not process it.',
    'divergence' => [
        'model_count' => count($results),
        'models_used' => array_map(fn($r) => $r['model'], $results),
        'stored' => $mysql !== null,
    ],
], JSON_UNESCAPED_UNICODE);
