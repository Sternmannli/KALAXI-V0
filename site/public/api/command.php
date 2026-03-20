<?php
/**
 * ╔══════════════════════════════════════════════════════════════════╗
 * ║  COMMAND CENTRE — V-002's Remote Hand                          ║
 * ║                                                                 ║
 * ║  Secured PHP endpoint on kalam.ch that V-002 controls via      ║
 * ║  GitHub Actions workflow. The website is the mouth AND the      ║
 * ║  brain. Mohamed's property. Mohamed's infrastructure.           ║
 * ║                                                                 ║
 * ║  Actions:                                                       ║
 * ║    health         — full system diagnostic                      ║
 * ║    together       — call Together AI (inference/chat)            ║
 * ║    store          — write system data to server storage          ║
 * ║    read           — read system data from server storage         ║
 * ║    list           — list stored system data files                ║
 * ║    db-query       — read-only MySQL query                        ║
 * ║    db-status      — database tables and counts                   ║
 * ║    ledger         — ledger status and verification               ║
 * ║    exp001         — EXP-001 experiment status                    ║
 * ║    train-upload   — upload JSONL to Together AI for fine-tuning  ║
 * ║    train-start    — create fine-tuning job on Together AI        ║
 * ║    train-status   — check fine-tuning job progress               ║
 * ║    train-list     — list all fine-tuning jobs                    ║
 * ║    train-cancel   — cancel a running fine-tuning job             ║
 * ║    train-activate — switch AXI voice to fine-tuned model         ║
 * ║                                                                 ║
 * ║  Auth: COMMAND_KEY in data/.config                               ║
 * ║                                                                 ║
 * ║  [V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]                       ║
 * ╚══════════════════════════════════════════════════════════════════╝
 */

header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type, Authorization');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') { http_response_code(204); exit; }
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['error' => 'POST only']);
    exit;
}

// ═══════════════════════════════════════════════════════════════════
// CONFIG
// ═══════════════════════════════════════════════════════════════════

function load_config(): array {
    static $config = null;
    if ($config !== null) return $config;
    $config = [];
    $path = __DIR__ . '/../data/.config';
    if (file_exists($path) && is_readable($path)) {
        foreach (file($path, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES) as $line) {
            $line = trim($line);
            if (empty($line) || $line[0] === '#' || $line[0] === ';') continue;
            $parts = explode('=', $line, 2);
            if (count($parts) === 2) $config[trim($parts[0])] = trim($parts[1]);
        }
    }
    return $config;
}

// ═══════════════════════════════════════════════════════════════════
// AUTH — COMMAND_KEY required
// ═══════════════════════════════════════════════════════════════════

$config = load_config();
$command_key = $config['COMMAND_KEY'] ?? null;

if (!$command_key || strlen($command_key) < 16) {
    http_response_code(503);
    echo json_encode(['error' => 'Command centre not configured. Set COMMAND_KEY in data/.config']);
    exit;
}

// Check Authorization header
$auth_header = $_SERVER['HTTP_AUTHORIZATION'] ?? '';
$provided_key = '';
if (preg_match('/^Bearer\s+(.+)$/i', $auth_header, $m)) {
    $provided_key = $m[1];
}

if (!hash_equals($command_key, $provided_key)) {
    http_response_code(403);
    echo json_encode(['error' => 'Unauthorized']);
    exit;
}

// ═══════════════════════════════════════════════════════════════════
// INPUT
// ═══════════════════════════════════════════════════════════════════

$body = json_decode(file_get_contents('php://input'), true) ?: [];
$action = trim($body['action'] ?? '');

if (empty($action)) {
    http_response_code(400);
    echo json_encode(['error' => 'Action required']);
    exit;
}

// ═══════════════════════════════════════════════════════════════════
// DATABASE HELPER
// ═══════════════════════════════════════════════════════════════════

function get_db(): ?PDO {
    $config = load_config();
    if (empty($config['DB_HOST']) || empty($config['DB_NAME'])) return null;
    try {
        return new PDO(
            "mysql:host={$config['DB_HOST']};dbname={$config['DB_NAME']};charset=utf8mb4",
            $config['DB_USER'] ?? '', $config['DB_PASS'] ?? '',
            [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION]
        );
    } catch (PDOException $e) {
        return null;
    }
}

// ═══════════════════════════════════════════════════════════════════
// STORAGE — server-side file store for system data
// Base: ~/www/kalam.ch/data/system/
// ═══════════════════════════════════════════════════════════════════

function storage_dir(): string {
    $dir = __DIR__ . '/../data/system';
    if (!is_dir($dir)) mkdir($dir, 0755, true);
    return realpath($dir);
}

function safe_path(string $filename): ?string {
    // Prevent directory traversal
    $clean = basename($filename);
    if ($clean !== $filename || empty($clean) || $clean === '.' || $clean === '..') return null;
    if (preg_match('/[^a-zA-Z0-9._\-]/', $clean)) return null;
    return storage_dir() . '/' . $clean;
}

// ═══════════════════════════════════════════════════════════════════
// ACTION ROUTER
// ═══════════════════════════════════════════════════════════════════

$result = null;

switch ($action) {

    // ─── HEALTH ───
    case 'health':
        $db = get_db();
        $ledger_count = 0;
        $db_status = 'disconnected';
        if ($db) {
            $db_status = 'connected';
            try { $ledger_count = (int) $db->query("SELECT COUNT(*) FROM ledger")->fetchColumn(); } catch (Exception $e) {}
        }
        $result = [
            'status' => 'alive',
            'php' => phpversion(),
            'curl' => function_exists('curl_init') ? 'yes' : 'no',
            'sqlite' => class_exists('SQLite3') ? 'yes' : 'no',
            'pdo_mysql' => extension_loaded('pdo_mysql') ? 'yes' : 'no',
            'database' => $db_status,
            'ledger_count' => $ledger_count,
            'together_key' => !empty($config['TOGETHER_API_KEY']) ? 'present' : 'missing',
            'groq_key' => !empty($config['GROQ_API_KEY']) ? 'present' : 'missing',
            'storage_dir' => is_dir(storage_dir()) ? 'exists' : 'missing',
            'storage_files' => is_dir(storage_dir()) ? count(glob(storage_dir() . '/*')) : 0,
            'disk_free' => disk_free_space(__DIR__) ? round(disk_free_space(__DIR__) / 1024 / 1024, 1) . ' MB' : 'unknown',
            'timestamp' => gmdate('c'),
        ];
        break;

    // ─── TOGETHER AI ───
    case 'together':
        $together_key = $config['TOGETHER_API_KEY'] ?? null;
        if (!$together_key) {
            $result = ['error' => 'TOGETHER_API_KEY not configured'];
            break;
        }

        $default_model = $config['AXI_MODEL'] ?? 'meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo';
        $model = $body['model'] ?? $default_model;
        $messages = $body['messages'] ?? [];
        $max_tokens = min((int) ($body['max_tokens'] ?? 1024), 4096);
        $temperature = (float) ($body['temperature'] ?? 0.7);

        if (empty($messages)) {
            // Simple prompt mode
            $prompt = $body['prompt'] ?? '';
            if (empty($prompt)) { $result = ['error' => 'messages or prompt required']; break; }
            $messages = [['role' => 'user', 'content' => $prompt]];
        }

        $payload = json_encode([
            'model' => $model,
            'messages' => $messages,
            'max_tokens' => $max_tokens,
            'temperature' => $temperature,
        ]);

        $ch = curl_init('https://api.together.xyz/v1/chat/completions');
        curl_setopt_array($ch, [
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_POST => true,
            CURLOPT_POSTFIELDS => $payload,
            CURLOPT_HTTPHEADER => [
                'Content-Type: application/json',
                'Authorization: Bearer ' . $together_key,
            ],
            CURLOPT_TIMEOUT => 30,
            CURLOPT_SSL_VERIFYPEER => true,
        ]);
        $response = curl_exec($ch);
        $http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        $curl_error = curl_error($ch);
        curl_close($ch);

        if ($http_code === 200 && $response) {
            $data = json_decode($response, true);
            $result = [
                'ok' => true,
                'model' => $model,
                'text' => $data['choices'][0]['message']['content'] ?? null,
                'usage' => $data['usage'] ?? null,
                'finish_reason' => $data['choices'][0]['finish_reason'] ?? null,
            ];
        } else {
            $result = [
                'error' => 'Together AI call failed',
                'http_code' => $http_code,
                'curl_error' => $curl_error,
                'response' => substr($response ?? '', 0, 500),
            ];
        }
        break;

    // ─── TOGETHER: LIST MODELS ───
    case 'together-models':
        $together_key = $config['TOGETHER_API_KEY'] ?? null;
        if (!$together_key) { $result = ['error' => 'TOGETHER_API_KEY not configured']; break; }

        $ch = curl_init('https://api.together.xyz/v1/models');
        curl_setopt_array($ch, [
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_HTTPHEADER => ['Authorization: Bearer ' . $together_key],
            CURLOPT_TIMEOUT => 15,
        ]);
        $response = curl_exec($ch);
        $http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        curl_close($ch);

        if ($http_code === 200 && $response) {
            $models = json_decode($response, true);
            // Return just model IDs and types for brevity
            $list = [];
            foreach (($models['data'] ?? $models) as $m) {
                if (is_array($m) && isset($m['id'])) {
                    $list[] = ['id' => $m['id'], 'type' => $m['type'] ?? 'unknown'];
                }
            }
            $result = ['ok' => true, 'count' => count($list), 'models' => $list];
        } else {
            $result = ['error' => 'Failed to list models', 'http_code' => $http_code];
        }
        break;

    // ─── STORE DATA ───
    case 'store':
        $filename = $body['filename'] ?? '';
        $content = $body['content'] ?? '';
        $path = safe_path($filename);
        if (!$path) { $result = ['error' => 'Invalid filename']; break; }
        if (empty($content)) { $result = ['error' => 'Content required']; break; }
        if (strlen($content) > 10 * 1024 * 1024) { $result = ['error' => 'Content too large (max 10MB)']; break; }

        $bytes = file_put_contents($path, $content, LOCK_EX);
        $result = [
            'ok' => true,
            'filename' => basename($path),
            'bytes' => $bytes,
            'hash' => hash('sha256', $content),
            'timestamp' => gmdate('c'),
        ];
        break;

    // ─── READ DATA ───
    case 'read':
        $filename = $body['filename'] ?? '';
        $path = safe_path($filename);
        if (!$path || !file_exists($path)) { $result = ['error' => 'File not found']; break; }

        $content = file_get_contents($path);
        $result = [
            'ok' => true,
            'filename' => basename($path),
            'bytes' => strlen($content),
            'hash' => hash('sha256', $content),
            'content' => $content,
        ];
        break;

    // ─── LIST DATA ───
    case 'list':
        $dir = storage_dir();
        $files = [];
        foreach (glob($dir . '/*') as $f) {
            $files[] = [
                'name' => basename($f),
                'bytes' => filesize($f),
                'modified' => gmdate('c', filemtime($f)),
            ];
        }
        usort($files, fn($a, $b) => strcmp($b['modified'], $a['modified']));
        $result = ['ok' => true, 'files' => $files, 'count' => count($files)];
        break;

    // ─── DB STATUS ───
    case 'db-status':
        $db = get_db();
        if (!$db) { $result = ['error' => 'Database not connected']; break; }

        $tables = [];
        $stmt = $db->query("SHOW TABLES");
        while ($row = $stmt->fetch(PDO::FETCH_NUM)) {
            $table = $row[0];
            $count = (int) $db->query("SELECT COUNT(*) FROM `{$table}`")->fetchColumn();
            $tables[$table] = $count;
        }
        $result = ['ok' => true, 'tables' => $tables, 'timestamp' => gmdate('c')];
        break;

    // ─── DB QUERY (read-only) ───
    case 'db-query':
        $db = get_db();
        if (!$db) { $result = ['error' => 'Database not connected']; break; }

        $sql = trim($body['sql'] ?? '');
        if (empty($sql)) { $result = ['error' => 'SQL required']; break; }

        // Only allow SELECT queries
        if (!preg_match('/^\s*SELECT\b/i', $sql)) {
            $result = ['error' => 'Only SELECT queries allowed'];
            break;
        }
        // Block dangerous patterns
        if (preg_match('/\b(DROP|DELETE|UPDATE|INSERT|ALTER|CREATE|TRUNCATE|GRANT|REVOKE)\b/i', $sql)) {
            $result = ['error' => 'Query contains forbidden keywords'];
            break;
        }

        try {
            $stmt = $db->query($sql . ' LIMIT 100');
            $rows = $stmt->fetchAll(PDO::FETCH_ASSOC);
            $result = ['ok' => true, 'rows' => $rows, 'count' => count($rows)];
        } catch (PDOException $e) {
            $result = ['error' => 'Query failed: ' . $e->getMessage()];
        }
        break;

    // ─── LEDGER STATUS ───
    case 'ledger':
        $db = get_db();
        if (!$db) { $result = ['error' => 'Database not connected']; break; }

        $count = (int) $db->query("SELECT COUNT(*) FROM ledger")->fetchColumn();
        $last = $db->query("SELECT id, chain_hash, created_utc FROM ledger ORDER BY id DESC LIMIT 1")->fetch(PDO::FETCH_ASSOC);

        // Verify chain
        $rows = $db->query("SELECT id, content_hash, prev_hash, chain_hash FROM ledger ORDER BY id ASC")->fetchAll(PDO::FETCH_ASSOC);
        $errors = [];
        $expected_prev = 'GENESIS';
        foreach ($rows as $row) {
            if ($row['prev_hash'] !== $expected_prev) {
                $errors[] = "Entry #{$row['id']}: prev_hash mismatch";
            }
            $computed = hash('sha256', $row['content_hash'] . $row['prev_hash']);
            if ($computed !== $row['chain_hash']) {
                $errors[] = "Entry #{$row['id']}: chain_hash mismatch";
            }
            $expected_prev = $row['chain_hash'];
        }

        $result = [
            'ok' => true,
            'count' => $count,
            'chain_valid' => empty($errors),
            'chain_errors' => $errors,
            'last_entry' => $last,
            'timestamp' => gmdate('c'),
        ];
        break;

    // ─── EXP-001 STATUS ───
    case 'exp001':
        $db = get_db();
        if (!$db) { $result = ['error' => 'Database not connected']; break; }

        try {
            $total = (int) $db->query("SELECT COUNT(*) FROM exp001_runs")->fetchColumn();
            $by_model = $db->query("SELECT model, COUNT(*) as runs, ROUND(AVG(vocabulary_overlap), 3) as avg_overlap, ROUND(AVG(length_ratio), 3) as avg_length_ratio FROM exp001_runs GROUP BY model")->fetchAll(PDO::FETCH_ASSOC);
            $recent = $db->query("SELECT model, ROUND(vocabulary_overlap, 3) as overlap, created_at FROM exp001_runs ORDER BY created_at DESC LIMIT 5")->fetchAll(PDO::FETCH_ASSOC);
            $result = [
                'ok' => true,
                'total_runs' => $total,
                'by_model' => $by_model,
                'recent' => $recent,
            ];
        } catch (PDOException $e) {
            $result = ['error' => 'exp001_runs table may not exist yet: ' . $e->getMessage()];
        }
        break;

    // ─── CORPUS STATUS ───
    case 'corpus-status':
        $training_dir = __DIR__ . '/../data/training';
        $files = [];
        if (is_dir($training_dir)) {
            foreach (['zakaka/ZAKAKA_CPT.jsonl', 'zakaka/ZAKAKA_SFT.jsonl', 'zakaka/MANIFEST.json',
                       'organ/GOLDEN_CPT.jsonl', 'organ/GOLDEN_SFT.jsonl', 'organ/GOLDEN_DPO.jsonl',
                       'organ/phase1/cpt_corpus.jsonl', 'organ/phase2/sft_corpus.jsonl', 'organ/phase3/dpo_corpus.jsonl',
                       'manifest.json'] as $f) {
                $path = "$training_dir/$f";
                if (file_exists($path)) {
                    $files[$f] = [
                        'bytes' => filesize($path),
                        'modified' => gmdate('c', filemtime($path)),
                        'sha256' => hash_file('sha256', $path),
                    ];
                } else {
                    $files[$f] = ['status' => 'missing'];
                }
            }
        } else {
            $files['_error'] = 'Training directory not found. Deploy needed.';
        }
        $result = ['ok' => true, 'training_dir' => $training_dir, 'files' => $files, 'timestamp' => gmdate('c')];
        break;

    // ═══════════════════════════════════════════════════════════════
    // TOGETHER AI FINE-TUNING — Train AXI's own voice
    // ═══════════════════════════════════════════════════════════════

    // ─── TRAIN: Upload corpus to Together AI ───
    case 'train-upload':
        $together_key = $config['TOGETHER_API_KEY'] ?? null;
        if (!$together_key) { $result = ['error' => 'TOGETHER_API_KEY not configured']; break; }

        $corpus = $body['corpus'] ?? 'zakaka_sft';
        $corpus_map = [
            'zakaka_sft' => 'training/zakaka/ZAKAKA_SFT.jsonl',
            'zakaka_cpt' => 'training/zakaka/ZAKAKA_CPT.jsonl',
            'organ_sft'  => 'training/organ/GOLDEN_SFT.jsonl',
            'organ_cpt'  => 'training/organ/GOLDEN_CPT.jsonl',
            'organ_dpo'  => 'training/organ/GOLDEN_DPO.jsonl',
        ];

        if (!isset($corpus_map[$corpus])) {
            $result = ['error' => 'Unknown corpus: ' . $corpus, 'valid' => array_keys($corpus_map)];
            break;
        }

        $file_path = __DIR__ . '/../data/' . $corpus_map[$corpus];
        if (!file_exists($file_path)) {
            $result = ['error' => 'Corpus file not found on server. Deploy needed.', 'path' => $corpus_map[$corpus]];
            break;
        }

        $file_size = filesize($file_path);
        $file_hash = hash_file('sha256', $file_path);

        // Upload to Together AI files endpoint
        $ch = curl_init('https://api.together.xyz/v1/files');
        $cfile = new CURLFile($file_path, 'application/jsonl', basename($file_path));
        curl_setopt_array($ch, [
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_POST => true,
            CURLOPT_POSTFIELDS => ['file' => $cfile, 'purpose' => 'fine-tune'],
            CURLOPT_HTTPHEADER => ['Authorization: Bearer ' . $together_key],
            CURLOPT_TIMEOUT => 120,
        ]);
        $response = curl_exec($ch);
        $http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        $curl_error = curl_error($ch);
        curl_close($ch);

        if ($http_code >= 200 && $http_code < 300 && $response) {
            $data = json_decode($response, true);
            $file_id = $data['id'] ?? null;

            // Save state
            $state_path = storage_dir() . '/training-state.json';
            $state = file_exists($state_path) ? json_decode(file_get_contents($state_path), true) : [];
            $state['last_upload'] = [
                'file_id' => $file_id,
                'corpus' => $corpus,
                'bytes' => $file_size,
                'sha256' => $file_hash,
                'timestamp' => gmdate('c'),
            ];
            file_put_contents($state_path, json_encode($state, JSON_PRETTY_PRINT), LOCK_EX);

            // Log to MySQL if available
            $db = get_db();
            if ($db) {
                $db->exec("CREATE TABLE IF NOT EXISTS training_jobs (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    job_id VARCHAR(255),
                    file_id VARCHAR(255),
                    corpus VARCHAR(100),
                    base_model VARCHAR(255),
                    output_model VARCHAR(255),
                    status VARCHAR(50) DEFAULT 'uploaded',
                    n_epochs INT,
                    learning_rate FLOAT,
                    started_at DATETIME,
                    completed_at DATETIME,
                    events TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4");
                $stmt = $db->prepare("INSERT INTO training_jobs (file_id, corpus, status) VALUES (?, ?, 'uploaded')");
                $stmt->execute([$file_id, $corpus]);
            }

            $result = [
                'ok' => true,
                'file_id' => $file_id,
                'corpus' => $corpus,
                'bytes' => $file_size,
                'sha256' => $file_hash,
                'together_response' => $data,
            ];
        } else {
            $result = [
                'error' => 'Together AI file upload failed',
                'http_code' => $http_code,
                'curl_error' => $curl_error,
                'response' => substr($response ?? '', 0, 500),
            ];
        }
        break;

    // ─── TRAIN: Start fine-tuning job ───
    case 'train-start':
        $together_key = $config['TOGETHER_API_KEY'] ?? null;
        if (!$together_key) { $result = ['error' => 'TOGETHER_API_KEY not configured']; break; }

        $file_id = $body['file_id'] ?? null;
        if (!$file_id) {
            // Try to use last uploaded file
            $state_path = storage_dir() . '/training-state.json';
            if (file_exists($state_path)) {
                $state = json_decode(file_get_contents($state_path), true);
                $file_id = $state['last_upload']['file_id'] ?? null;
            }
        }
        if (!$file_id) { $result = ['error' => 'file_id required. Upload a corpus first.']; break; }

        $model = $body['model'] ?? 'meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo';
        $n_epochs = max(1, min(20, (int) ($body['n_epochs'] ?? 3)));
        $learning_rate = (float) ($body['learning_rate'] ?? 1e-5);
        $suffix = $body['suffix'] ?? 'axi-voice';
        // Sanitize suffix: alphanumeric, hyphens, underscores only, max 40 chars
        $suffix = substr(preg_replace('/[^a-zA-Z0-9_\-]/', '', $suffix), 0, 40);

        $payload = [
            'model' => $model,
            'training_file' => $file_id,
            'n_epochs' => $n_epochs,
            'learning_rate' => $learning_rate,
            'suffix' => $suffix,
            'train_on_inputs' => 'auto',
        ];

        // Optional validation file
        if (!empty($body['validation_file_id'])) {
            $payload['validation_file'] = $body['validation_file_id'];
            $payload['n_evals'] = max(1, min(100, (int) ($body['n_evals'] ?? 5)));
        }

        $ch = curl_init('https://api.together.xyz/v1/fine-tunes');
        curl_setopt_array($ch, [
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_POST => true,
            CURLOPT_POSTFIELDS => json_encode($payload),
            CURLOPT_HTTPHEADER => [
                'Content-Type: application/json',
                'Authorization: Bearer ' . $together_key,
            ],
            CURLOPT_TIMEOUT => 30,
        ]);
        $response = curl_exec($ch);
        $http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        $curl_error = curl_error($ch);
        curl_close($ch);

        if ($http_code >= 200 && $http_code < 300 && $response) {
            $data = json_decode($response, true);
            $job_id = $data['id'] ?? null;

            // Save state
            $state_path = storage_dir() . '/training-state.json';
            $state = file_exists($state_path) ? json_decode(file_get_contents($state_path), true) : [];
            $state['active_job'] = [
                'job_id' => $job_id,
                'model' => $model,
                'file_id' => $file_id,
                'n_epochs' => $n_epochs,
                'suffix' => $suffix,
                'status' => $data['status'] ?? 'queued',
                'started' => gmdate('c'),
            ];
            if (!isset($state['history'])) $state['history'] = [];
            $state['history'][] = $state['active_job'];
            file_put_contents($state_path, json_encode($state, JSON_PRETTY_PRINT), LOCK_EX);

            // Log to MySQL
            $db = get_db();
            if ($db) {
                try {
                    $stmt = $db->prepare("INSERT INTO training_jobs (job_id, file_id, corpus, base_model, status, n_epochs, learning_rate, started_at)
                        VALUES (?, ?, ?, ?, ?, ?, ?, NOW())");
                    $corpus = $state['last_upload']['corpus'] ?? 'unknown';
                    $stmt->execute([$job_id, $file_id, $corpus, $model, $data['status'] ?? 'queued', $n_epochs, $learning_rate]);
                } catch (Exception $e) { /* table may not exist yet */ }
            }

            $result = [
                'ok' => true,
                'job_id' => $job_id,
                'model' => $model,
                'file_id' => $file_id,
                'n_epochs' => $n_epochs,
                'learning_rate' => $learning_rate,
                'suffix' => $suffix,
                'status' => $data['status'] ?? 'queued',
                'together_response' => $data,
            ];
        } else {
            $result = [
                'error' => 'Together AI fine-tuning job creation failed',
                'http_code' => $http_code,
                'curl_error' => $curl_error,
                'response' => substr($response ?? '', 0, 500),
            ];
        }
        break;

    // ─── TRAIN: Check job status ───
    case 'train-status':
        $together_key = $config['TOGETHER_API_KEY'] ?? null;
        if (!$together_key) { $result = ['error' => 'TOGETHER_API_KEY not configured']; break; }

        $job_id = $body['job_id'] ?? null;
        if (!$job_id) {
            $state_path = storage_dir() . '/training-state.json';
            if (file_exists($state_path)) {
                $state = json_decode(file_get_contents($state_path), true);
                $job_id = $state['active_job']['job_id'] ?? null;
            }
        }
        if (!$job_id) { $result = ['error' => 'job_id required. Start a training job first.']; break; }

        $ch = curl_init('https://api.together.xyz/v1/fine-tunes/' . urlencode($job_id));
        curl_setopt_array($ch, [
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_HTTPHEADER => ['Authorization: Bearer ' . $together_key],
            CURLOPT_TIMEOUT => 15,
        ]);
        $response = curl_exec($ch);
        $http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        curl_close($ch);

        if ($http_code === 200 && $response) {
            $data = json_decode($response, true);
            $status = $data['status'] ?? 'unknown';
            $output_model = $data['output_name'] ?? $data['fine_tuned_model'] ?? null;

            // Update state
            $state_path = storage_dir() . '/training-state.json';
            $state = file_exists($state_path) ? json_decode(file_get_contents($state_path), true) : [];
            if (isset($state['active_job']) && $state['active_job']['job_id'] === $job_id) {
                $state['active_job']['status'] = $status;
                if ($output_model) $state['active_job']['output_model'] = $output_model;
                if ($status === 'completed') $state['active_job']['completed'] = gmdate('c');
            }
            file_put_contents($state_path, json_encode($state, JSON_PRETTY_PRINT), LOCK_EX);

            // Update MySQL
            $db = get_db();
            if ($db) {
                try {
                    $stmt = $db->prepare("UPDATE training_jobs SET status = ?, output_model = ?, completed_at = IF(? = 'completed', NOW(), NULL) WHERE job_id = ?");
                    $stmt->execute([$status, $output_model, $status, $job_id]);
                } catch (Exception $e) {}
            }

            $result = [
                'ok' => true,
                'job_id' => $job_id,
                'status' => $status,
                'output_model' => $output_model,
                'events' => $data['events'] ?? [],
                'training_file' => $data['training_file'] ?? null,
                'model' => $data['model'] ?? null,
                'n_epochs' => $data['n_epochs'] ?? null,
                'together_response' => $data,
            ];
        } else {
            $result = ['error' => 'Failed to get job status', 'http_code' => $http_code];
        }
        break;

    // ─── TRAIN: List all fine-tuning jobs ───
    case 'train-list':
        $together_key = $config['TOGETHER_API_KEY'] ?? null;
        if (!$together_key) { $result = ['error' => 'TOGETHER_API_KEY not configured']; break; }

        $ch = curl_init('https://api.together.xyz/v1/fine-tunes');
        curl_setopt_array($ch, [
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_HTTPHEADER => ['Authorization: Bearer ' . $together_key],
            CURLOPT_TIMEOUT => 15,
        ]);
        $response = curl_exec($ch);
        $http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        curl_close($ch);

        if ($http_code === 200 && $response) {
            $data = json_decode($response, true);
            $jobs = $data['data'] ?? $data;
            $summary = [];
            if (is_array($jobs)) {
                foreach ($jobs as $job) {
                    $summary[] = [
                        'id' => $job['id'] ?? null,
                        'status' => $job['status'] ?? null,
                        'model' => $job['model'] ?? null,
                        'output_name' => $job['output_name'] ?? $job['fine_tuned_model'] ?? null,
                        'n_epochs' => $job['n_epochs'] ?? null,
                        'created_at' => $job['created_at'] ?? null,
                    ];
                }
            }
            $result = ['ok' => true, 'count' => count($summary), 'jobs' => $summary];
        } else {
            $result = ['error' => 'Failed to list jobs', 'http_code' => $http_code];
        }
        break;

    // ─── TRAIN: Cancel a running job ───
    case 'train-cancel':
        $together_key = $config['TOGETHER_API_KEY'] ?? null;
        if (!$together_key) { $result = ['error' => 'TOGETHER_API_KEY not configured']; break; }

        $job_id = $body['job_id'] ?? null;
        if (!$job_id) { $result = ['error' => 'job_id required']; break; }

        $ch = curl_init('https://api.together.xyz/v1/fine-tunes/' . urlencode($job_id) . '/cancel');
        curl_setopt_array($ch, [
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_POST => true,
            CURLOPT_POSTFIELDS => '',
            CURLOPT_HTTPHEADER => [
                'Content-Type: application/json',
                'Authorization: Bearer ' . $together_key,
            ],
            CURLOPT_TIMEOUT => 15,
        ]);
        $response = curl_exec($ch);
        $http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        curl_close($ch);

        if ($http_code >= 200 && $http_code < 300) {
            $data = json_decode($response, true) ?: [];
            $result = ['ok' => true, 'job_id' => $job_id, 'status' => 'cancelled', 'together_response' => $data];
        } else {
            $result = ['error' => 'Failed to cancel job', 'http_code' => $http_code, 'response' => substr($response ?? '', 0, 500)];
        }
        break;

    // ─── TRAIN: Activate fine-tuned model as AXI voice ───
    case 'train-activate':
        $model_id = $body['model_id'] ?? null;

        if (!$model_id) {
            // Try to get from last completed job
            $state_path = storage_dir() . '/training-state.json';
            if (file_exists($state_path)) {
                $state = json_decode(file_get_contents($state_path), true);
                $model_id = $state['active_job']['output_model'] ?? null;
            }
        }
        if (!$model_id) {
            $result = ['error' => 'model_id required. Complete a training job first.'];
            break;
        }

        // Write AXI_MODEL to .config
        $config_path = __DIR__ . '/../data/.config';
        $config_content = file_exists($config_path) ? file_get_contents($config_path) : '';

        // Remove existing AXI_MODEL line if present
        $config_content = preg_replace('/^AXI_MODEL=.*\n?/m', '', $config_content);
        // Append new line
        $config_content = rtrim($config_content) . "\nAXI_MODEL=" . $model_id . "\n";
        file_put_contents($config_path, $config_content, LOCK_EX);

        // Update state
        $state_path = storage_dir() . '/training-state.json';
        $state = file_exists($state_path) ? json_decode(file_get_contents($state_path), true) : [];
        $state['active_model'] = $model_id;
        $state['activated_at'] = gmdate('c');
        file_put_contents($state_path, json_encode($state, JSON_PRETTY_PRINT), LOCK_EX);

        $result = [
            'ok' => true,
            'active_model' => $model_id,
            'message' => 'AXI voice now uses: ' . $model_id,
            'timestamp' => gmdate('c'),
        ];
        break;

    // ─── TRAIN: Get training state ───
    case 'train-state':
        $state_path = storage_dir() . '/training-state.json';
        if (file_exists($state_path)) {
            $state = json_decode(file_get_contents($state_path), true);
            $state['ok'] = true;

            // Also read current AXI_MODEL from config
            $axi_model = $config['AXI_MODEL'] ?? null;
            $state['config_model'] = $axi_model ?: 'meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo (default)';

            $result = $state;
        } else {
            $result = [
                'ok' => true,
                'message' => 'No training state yet. Upload a corpus to begin.',
                'config_model' => $config['AXI_MODEL'] ?? 'meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo (default)',
            ];
        }
        break;

    // ─── CORPUS SUMMARY (quick count) ───
    case 'corpus-summary':
        $training_dir = __DIR__ . '/../data/training';
        $manifest_path = "$training_dir/manifest.json";
        if (file_exists($manifest_path)) {
            $manifest = json_decode(file_get_contents($manifest_path), true);
            $total_entries = 0;
            $total_bytes = 0;
            foreach (($manifest['corpora'] ?? []) as $info) {
                $total_entries += $info['entries'] ?? 0;
                $total_bytes += $info['bytes'] ?? 0;
            }
            $result = [
                'ok' => true,
                'generated' => $manifest['generated'] ?? 'unknown',
                'corpora_count' => count($manifest['corpora'] ?? []),
                'total_entries' => $total_entries,
                'total_bytes' => $total_bytes,
                'corpora' => $manifest['corpora'] ?? [],
            ];
        } else {
            $result = ['error' => 'No training manifest found. Deploy needed.'];
        }
        break;

    default:
        $result = ['error' => "Unknown action: {$action}"];
        break;
}

echo json_encode($result, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
