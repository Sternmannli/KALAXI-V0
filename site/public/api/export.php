<?php
/**
 * AXI Pattern Export — Anonymized statistics for the organism feedback loop.
 *
 * Returns: interaction counts, register distribution, proverb usage,
 * witness mark distribution. No personal data. No content.
 *
 * Auth: requires EXPORT_KEY secret in query string.
 * Usage: GET /api/export.php?key=<secret>
 *
 * [V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
 */

header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');

// --- Auth ---
$export_key = trim(getenv('EXPORT_KEY') ?: '');
if (empty($export_key)) {
    // Fallback: read from config file
    $config_path = __DIR__ . '/../data/.config';
    if (file_exists($config_path)) {
        foreach (file($config_path, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES) as $line) {
            $line = trim($line);
            if (str_starts_with($line, 'EXPORT_KEY=')) {
                $export_key = trim(substr($line, 11));
            }
        }
    }
}

$provided_key = $_GET['key'] ?? '';
if (empty($export_key) || !hash_equals($export_key, $provided_key)) {
    http_response_code(403);
    echo json_encode(['error' => 'Unauthorized']);
    exit;
}

// --- Read SQLite ---
$db_path = __DIR__ . '/../data/kalam.db';
if (!file_exists($db_path) || !class_exists('SQLite3')) {
    echo json_encode([
        'status' => 'no-data',
        'timestamp' => gmdate('c'),
        'message' => 'No database available yet.',
    ]);
    exit;
}

try {
    $db = new SQLite3($db_path, SQLITE3_OPEN_READONLY);
} catch (Exception $e) {
    echo json_encode(['status' => 'db-error', 'timestamp' => gmdate('c')]);
    exit;
}

// Total interactions
$total = (int) $db->querySingle('SELECT COUNT(*) FROM threshold');

// Ledger count (cumulative)
$ledger_count = (int) $db->querySingle('SELECT total_count FROM ledger_count ORDER BY id DESC LIMIT 1');

// Word count distribution
$word_buckets = ['1-3' => 0, '4-15' => 0, '16-50' => 0, '51+' => 0];
$result = $db->query('SELECT word_count FROM threshold');
while ($row = $result->fetchArray(SQLITE3_ASSOC)) {
    $w = (int) $row['word_count'];
    if ($w <= 3) $word_buckets['1-3']++;
    elseif ($w <= 15) $word_buckets['4-15']++;
    elseif ($w <= 50) $word_buckets['16-50']++;
    else $word_buckets['51+']++;
}

// Witness mark distribution
$mark_dist = [];
$result = $db->query('SELECT witness_mark, COUNT(*) as cnt FROM threshold GROUP BY witness_mark ORDER BY cnt DESC');
while ($row = $result->fetchArray(SQLITE3_ASSOC)) {
    $mark_dist[$row['witness_mark']] = (int) $row['cnt'];
}

// Daily activity (last 30 days)
$daily = [];
$result = $db->query("SELECT date(created_at) as day, COUNT(*) as cnt FROM threshold WHERE created_at >= date('now', '-30 days') GROUP BY day ORDER BY day");
while ($row = $result->fetchArray(SQLITE3_ASSOC)) {
    $daily[$row['day']] = (int) $row['cnt'];
}

// Dignity halts (D=0 events)
$halts = (int) $db->querySingle("SELECT COUNT(*) FROM threshold WHERE dignity_score = 0");

$db->close();

// --- Output ---
echo json_encode([
    'status' => 'ok',
    'timestamp' => gmdate('c'),
    'total_interactions' => $total,
    'ledger_count' => $ledger_count,
    'word_distribution' => $word_buckets,
    'witness_marks' => $mark_dist,
    'daily_activity_30d' => $daily,
    'dignity_halts' => $halts,
], JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
