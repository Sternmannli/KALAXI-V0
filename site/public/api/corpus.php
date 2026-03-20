<?php
/**
 * ╔══════════════════════════════════════════════════════════════════╗
 * ║  CORPUS API — Training Data Command Centre                     ║
 * ║                                                                 ║
 * ║  Read-only API for ZAKAKA (essence³) and Organ (full body)     ║
 * ║  training corpora. All writes go through Git pipeline.          ║
 * ║                                                                 ║
 * ║  Public:  ?summary (counts only, no content)                    ║
 * ║  Auth:    ?zakaka=cpt|sft, ?organ=cpt|sft|dpo                  ║
 * ║           ?search=<term>, ?sample=<type>&n=<count>              ║
 * ║           ?manifest (full hashes + metadata)                    ║
 * ║                                                                 ║
 * ║  Auth: Bearer COMMAND_KEY for content access                    ║
 * ║                                                                 ║
 * ║  [V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]                       ║
 * ╚══════════════════════════════════════════════════════════════════╝
 */

// CORS — restricted to kalam.ch origin
$origin = $_SERVER['HTTP_ORIGIN'] ?? '';
$allowed = ['https://kalam.ch', 'https://www.kalam.ch'];
if (in_array($origin, $allowed)) {
    header("Access-Control-Allow-Origin: $origin");
} else {
    header('Access-Control-Allow-Origin: https://kalam.ch');
}
header('Access-Control-Allow-Methods: GET, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type, Authorization');
header('Content-Type: application/json; charset=utf-8');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') { http_response_code(204); exit; }
if ($_SERVER['REQUEST_METHOD'] !== 'GET') {
    http_response_code(405);
    echo json_encode(['error' => 'GET only']);
    exit;
}

// ═══════════════════════════════════════════════════════════════════
// CONFIG + AUTH
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

function is_authed(): bool {
    $config = load_config();
    $command_key = $config['COMMAND_KEY'] ?? null;
    if (!$command_key || strlen($command_key) < 16) return false;
    $auth = $_SERVER['HTTP_AUTHORIZATION'] ?? '';
    if (preg_match('/^Bearer\s+(.+)$/i', $auth, $m)) {
        return hash_equals($command_key, $m[1]);
    }
    return false;
}

// ═══════════════════════════════════════════════════════════════════
// CORPUS PATHS
// ═══════════════════════════════════════════════════════════════════

$base = __DIR__ . '/../data/training';

$corpus_map = [
    'zakaka_cpt' => "$base/zakaka/ZAKAKA_CPT.jsonl",
    'zakaka_sft' => "$base/zakaka/ZAKAKA_SFT.jsonl",
    'organ_cpt'  => "$base/organ/GOLDEN_CPT.jsonl",
    'organ_sft'  => "$base/organ/GOLDEN_SFT.jsonl",
    'organ_dpo'  => "$base/organ/GOLDEN_DPO.jsonl",
    'phase1_cpt' => "$base/organ/phase1/cpt_corpus.jsonl",
    'phase2_sft' => "$base/organ/phase2/sft_corpus.jsonl",
    'phase3_dpo' => "$base/organ/phase3/dpo_corpus.jsonl",
];

function count_lines(string $path): int {
    if (!file_exists($path)) return 0;
    $count = 0;
    $fh = fopen($path, 'r');
    if (!$fh) return 0;
    while (($line = fgets($fh)) !== false) {
        if (trim($line) !== '') $count++;
    }
    fclose($fh);
    return $count;
}

function read_jsonl(string $path, int $limit = 0, int $offset = 0): array {
    if (!file_exists($path)) return [];
    $lines = [];
    $fh = fopen($path, 'r');
    if (!$fh) return [];
    $i = 0;
    while (($line = fgets($fh)) !== false) {
        $line = trim($line);
        if ($line === '') continue;
        if ($i < $offset) { $i++; continue; }
        $decoded = json_decode($line, true);
        if ($decoded !== null) $lines[] = $decoded;
        $i++;
        if ($limit > 0 && count($lines) >= $limit) break;
    }
    fclose($fh);
    return $lines;
}

function search_corpus(string $path, string $term, int $limit = 20): array {
    if (!file_exists($path)) return [];
    $results = [];
    $term_lower = mb_strtolower($term);
    $fh = fopen($path, 'r');
    if (!$fh) return [];
    $i = 0;
    while (($line = fgets($fh)) !== false) {
        $line = trim($line);
        if ($line === '') continue;
        if (mb_stripos($line, $term) !== false) {
            $decoded = json_decode($line, true);
            if ($decoded !== null) {
                $decoded['_line'] = $i;
                $results[] = $decoded;
            }
            if (count($results) >= $limit) break;
        }
        $i++;
    }
    fclose($fh);
    return $results;
}

function sample_corpus(string $path, int $n = 5): array {
    if (!file_exists($path)) return [];
    // Reservoir sampling for random entries without loading full file
    $reservoir = [];
    $fh = fopen($path, 'r');
    if (!$fh) return [];
    $i = 0;
    while (($line = fgets($fh)) !== false) {
        $line = trim($line);
        if ($line === '') continue;
        $decoded = json_decode($line, true);
        if ($decoded === null) continue;
        if ($i < $n) {
            $reservoir[$i] = $decoded;
        } else {
            $j = random_int(0, $i);
            if ($j < $n) $reservoir[$j] = $decoded;
        }
        $i++;
    }
    fclose($fh);
    return array_values($reservoir);
}

// ═══════════════════════════════════════════════════════════════════
// ROUTING
// ═══════════════════════════════════════════════════════════════════

$query = $_GET;

// ─── PUBLIC: Summary (counts only) ───
if (isset($query['summary'])) {
    $summary = [
        'status' => 'alive',
        'zakaka' => [
            'cpt' => ['entries' => count_lines($corpus_map['zakaka_cpt']), 'bytes' => @filesize($corpus_map['zakaka_cpt']) ?: 0],
            'sft' => ['entries' => count_lines($corpus_map['zakaka_sft']), 'bytes' => @filesize($corpus_map['zakaka_sft']) ?: 0],
        ],
        'organ' => [
            'golden_cpt' => ['entries' => count_lines($corpus_map['organ_cpt']), 'bytes' => @filesize($corpus_map['organ_cpt']) ?: 0],
            'golden_sft' => ['entries' => count_lines($corpus_map['organ_sft']), 'bytes' => @filesize($corpus_map['organ_sft']) ?: 0],
            'golden_dpo' => ['entries' => count_lines($corpus_map['organ_dpo']), 'bytes' => @filesize($corpus_map['organ_dpo']) ?: 0],
            'phase1_cpt' => ['entries' => count_lines($corpus_map['phase1_cpt']), 'bytes' => @filesize($corpus_map['phase1_cpt']) ?: 0],
            'phase2_sft' => ['entries' => count_lines($corpus_map['phase2_sft']), 'bytes' => @filesize($corpus_map['phase2_sft']) ?: 0],
            'phase3_dpo' => ['entries' => count_lines($corpus_map['phase3_dpo']), 'bytes' => @filesize($corpus_map['phase3_dpo']) ?: 0],
        ],
        'timestamp' => gmdate('c'),
    ];

    // Add totals
    $zakaka_total = $summary['zakaka']['cpt']['entries'] + $summary['zakaka']['sft']['entries'];
    $organ_total = 0;
    foreach ($summary['organ'] as $v) $organ_total += $v['entries'];
    $summary['totals'] = [
        'zakaka_entries' => $zakaka_total,
        'organ_entries' => $organ_total,
        'all_entries' => $zakaka_total + $organ_total,
    ];

    echo json_encode($summary, JSON_PRETTY_PRINT);
    exit;
}

// ─── Everything below requires auth ───
if (!is_authed()) {
    http_response_code(403);
    echo json_encode(['error' => 'Unauthorized. Bearer COMMAND_KEY required.']);
    exit;
}

// ─── Manifest (full hashes) ───
if (isset($query['manifest'])) {
    $manifest_path = "$base/manifest.json";
    if (file_exists($manifest_path)) {
        echo file_get_contents($manifest_path);
    } else {
        echo json_encode(['error' => 'Manifest not found. Run deploy to generate.']);
    }
    exit;
}

// ─── ZAKAKA corpus ───
if (isset($query['zakaka'])) {
    $type = $query['zakaka'];
    $key = "zakaka_$type";
    if (!isset($corpus_map[$key])) {
        echo json_encode(['error' => "Unknown ZAKAKA type: $type. Use cpt or sft."]);
        exit;
    }
    $limit = min((int)($query['limit'] ?? 50), 500);
    $offset = max((int)($query['offset'] ?? 0), 0);
    $entries = read_jsonl($corpus_map[$key], $limit, $offset);
    echo json_encode([
        'ok' => true, 'type' => "zakaka_$type",
        'entries' => $entries, 'count' => count($entries),
        'total' => count_lines($corpus_map[$key]),
        'offset' => $offset, 'limit' => $limit,
    ], JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
    exit;
}

// ─── Organ corpus ───
if (isset($query['organ'])) {
    $type = $query['organ'];
    $key = "organ_$type";
    if (!isset($corpus_map[$key])) {
        // Try phase variants
        $phase_keys = ['phase1_cpt' => 'phase1', 'phase2_sft' => 'phase2', 'phase3_dpo' => 'phase3'];
        $found = false;
        foreach ($phase_keys as $pk => $pv) {
            if ($type === $pv) { $key = $pk; $found = true; break; }
        }
        if (!$found) {
            echo json_encode(['error' => "Unknown Organ type: $type. Use cpt, sft, dpo, phase1, phase2, phase3."]);
            exit;
        }
    }
    $limit = min((int)($query['limit'] ?? 50), 500);
    $offset = max((int)($query['offset'] ?? 0), 0);
    $entries = read_jsonl($corpus_map[$key], $limit, $offset);
    echo json_encode([
        'ok' => true, 'type' => $key,
        'entries' => $entries, 'count' => count($entries),
        'total' => count_lines($corpus_map[$key]),
        'offset' => $offset, 'limit' => $limit,
    ], JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
    exit;
}

// ─── Search across all corpora ───
if (isset($query['search'])) {
    $term = trim($query['search']);
    if (strlen($term) < 2) {
        echo json_encode(['error' => 'Search term must be at least 2 characters.']);
        exit;
    }
    $limit = min((int)($query['limit'] ?? 20), 100);
    $results = [];
    foreach ($corpus_map as $name => $path) {
        $found = search_corpus($path, $term, $limit);
        foreach ($found as $entry) {
            $entry['_corpus'] = $name;
            $results[] = $entry;
        }
        if (count($results) >= $limit) break;
    }
    $results = array_slice($results, 0, $limit);
    echo json_encode([
        'ok' => true, 'term' => $term,
        'results' => $results, 'count' => count($results),
    ], JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
    exit;
}

// ─── Random sample ───
if (isset($query['sample'])) {
    $type = $query['sample'];
    $n = min((int)($query['n'] ?? 5), 50);

    // Map type to corpus key
    $key = null;
    if ($type === 'zakaka') $key = 'zakaka_sft';
    elseif ($type === 'zakaka_cpt') $key = 'zakaka_cpt';
    elseif ($type === 'organ' || $type === 'organ_sft') $key = 'organ_sft';
    elseif ($type === 'organ_cpt') $key = 'organ_cpt';
    elseif ($type === 'organ_dpo') $key = 'organ_dpo';
    else {
        echo json_encode(['error' => "Unknown sample type: $type. Use zakaka, organ, zakaka_cpt, organ_cpt, organ_sft, organ_dpo."]);
        exit;
    }

    $entries = sample_corpus($corpus_map[$key], $n);
    echo json_encode([
        'ok' => true, 'type' => $key,
        'sample' => $entries, 'count' => count($entries),
    ], JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
    exit;
}

// ─── Default: help ───
echo json_encode([
    'corpus_api' => 'ZAKAKA + Organ Command Centre',
    'endpoints' => [
        '?summary' => 'Public: counts and sizes (no auth needed)',
        '?manifest' => 'Full hashes and metadata',
        '?zakaka=cpt|sft' => 'Read ZAKAKA corpus entries',
        '?organ=cpt|sft|dpo|phase1|phase2|phase3' => 'Read Organ corpus entries',
        '?search=<term>' => 'Search across all corpora',
        '?sample=<type>&n=<count>' => 'Random sample from corpus',
    ],
    'params' => [
        'limit' => 'Max entries to return (default 50, max 500)',
        'offset' => 'Skip first N entries (pagination)',
        'n' => 'Sample size (default 5, max 50)',
    ],
    'auth' => 'Bearer COMMAND_KEY required for all except ?summary',
], JSON_PRETTY_PRINT);
