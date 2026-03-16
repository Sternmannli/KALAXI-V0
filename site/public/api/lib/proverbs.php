<?php
/**
 * proverbs.php — Canonical Proverb Selection
 * Source: R7M/WISDOM_CANON.md (166 proverbs)
 *
 * Selects a contextually appropriate proverb from the canon.
 * The proverb is immutable. The frame adapts.
 *
 * [V-002 · GO: Laila-Yara-Salim]
 */

function load_proverbs(): array {
    static $proverbs = null;
    if ($proverbs === null) {
        $path = __DIR__ . '/../../data/proverbs.json';
        if (file_exists($path)) {
            $proverbs = json_decode(file_get_contents($path), true) ?? [];
        } else {
            $proverbs = [];
        }
    }
    return $proverbs;
}

/**
 * Detect register from donor input.
 * Returns: greeting, grief, anger, fear, seeking, work, story, code, reflection, general
 */
function detect_register(string $text): string {
    $lower = strtolower($text);
    $words = str_word_count($text);

    // Greetings
    if (preg_match('/^(hi|hello|hey|greetings|good (morning|evening|afternoon)|salam|ahlan|marhaba)\b/i', $lower)) {
        return 'greeting';
    }

    // Grief / loss
    if (preg_match('/\b(grief|grieve|mourn|loss|died|death|miss (you|them|her|him)|gone forever|passed away)\b/i', $lower)) {
        return 'grief';
    }

    // Anger
    if (preg_match('/\b(angry|furious|rage|outraged|hate|unfair|injustice|disgusted)\b/i', $lower)) {
        return 'anger';
    }

    // Fear
    if (preg_match('/\b(afraid|scared|terrified|anxious|panic|dread|fear|worried|nightmare)\b/i', $lower)) {
        return 'fear';
    }

    // Seeking / questions
    if (preg_match('/\b(how|what|why|where|when|who|can you|tell me|explain|help me|I need)\b/i', $lower)) {
        return 'seeking';
    }

    // Work / practical
    if (preg_match('/\b(build|create|make|fix|solve|implement|design|plan|project|task|code|function|error|bug)\b/i', $lower)) {
        return 'work';
    }

    // Story request
    if (preg_match('/\b(story|tale|once upon|write me|tell me a)\b/i', $lower)) {
        return 'story';
    }

    // Reflection / deep
    if ($words > 30 || preg_match('/\b(think|wonder|realize|understand|feel like|seems like|meaning|purpose|life)\b/i', $lower)) {
        return 'reflection';
    }

    return 'general';
}

/**
 * Select a proverb appropriate for the detected register.
 * Uses content hash for deterministic-but-varied selection.
 */
function select_proverb(string $text, string $register = ''): ?array {
    $proverbs = load_proverbs();
    if (empty($proverbs)) return null;

    if (empty($register)) {
        $register = detect_register($text);
    }

    // Register-to-proverb-range mapping (curated from canon structure)
    // P#0001-0004: beginnings, P#0005-0008: attention, P#0009-0012: fear/courage
    // P#0013-0020: craft/error, P#0021-0024: speech, P#0025-0028: patience
    // P#0029-0032: teamwork, P#0033-0040: risk/systems, P#0041-0048: leadership/care
    // P#0049-0100: dignity/identity, P#0100+: wisdom/depth
    $register_ranges = [
        'greeting' => [0, 4],
        'fear' => [8, 12],
        'work' => [12, 20],
        'anger' => [44, 52],
        'grief' => [44, 52],
        'seeking' => [0, 30],
        'story' => [44, 60],
        'reflection' => [60, min(count($proverbs), 100)],
        'general' => [0, min(count($proverbs), 50)],
    ];

    $range = $register_ranges[$register] ?? $register_ranges['general'];
    $start = $range[0];
    $end = min($range[1], count($proverbs));

    if ($start >= $end) {
        $start = 0;
        $end = count($proverbs);
    }

    // Use hash of input for deterministic selection within range
    $hash = crc32($text);
    $index = $start + abs($hash) % ($end - $start);

    return $proverbs[$index] ?? $proverbs[0];
}
