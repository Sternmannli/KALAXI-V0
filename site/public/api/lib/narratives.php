<?php
/**
 * SECTION 12 — MANIFEST & TOPOLOGY + NARRATIVE GROWTH
 *
 * axi.php knows its body. Every satellite registered.
 * The manifest is the connection layer between hub and spokes.
 *
 * [V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
 */

// ── MANIFEST ──

function load_manifest(): array {
    $path = __DIR__ . '/../../data/manifest.json';
    if (!file_exists($path)) return [];
    $data = json_decode(file_get_contents($path), true);
    return $data ?? [];
}

// ── NARRATIVES ──

function load_narrative(string $id): ?array {
    $manifest = load_manifest();
    $id_upper = strtoupper($id);
    foreach ($manifest['satellites'] ?? [] as $sat) {
        if ($sat['id'] === $id_upper && $sat['type'] === 'narrative') {
            $path = __DIR__ . '/../..' . $sat['path'];
            if (!file_exists($path)) return null;
            return json_decode(file_get_contents($path), true);
        }
    }
    return null;
}

function load_narrative_chapter(string $id, int $chapter): ?array {
    $nar = load_narrative($id);
    if (!$nar) return null;
    foreach ($nar['chapters'] as $ch) {
        if ($ch['number'] === $chapter) return $ch;
    }
    return null;
}

// ── R7M ──

function load_r7m(): ?array {
    $path = __DIR__ . '/../../data/r7m-index.json';
    if (!file_exists($path)) return null;
    return json_decode(file_get_contents($path), true);
}

// ── NARRATIVE GROWTH PROTOCOL ──

function load_seeds(): array {
    $path = __DIR__ . '/../../data/narrative-seeds.json';
    if (!file_exists($path)) return ['seeds' => [], 'growth_log' => []];
    return json_decode(file_get_contents($path), true) ?? ['seeds' => [], 'growth_log' => []];
}

function register_seed(string $pattern, string $treasure_id, string $target): array {
    $path = __DIR__ . '/../../data/narrative-seeds.json';
    $data = load_seeds();
    $seed = [
        'id' => 'SEED-' . str_pad(count($data['seeds']) + 1, 3, '0', STR_PAD_LEFT),
        'pattern' => $pattern,
        'treasure' => $treasure_id,
        'target_narrative' => $target,
        'status' => 'dormant',
        'created' => gmdate('Y-m-d'),
    ];
    $data['seeds'][] = $seed;
    file_put_contents($path, json_encode($data, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE));
    return $seed;
}
