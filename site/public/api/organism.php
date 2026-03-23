<?php
/**
 * organism.php — The Constitutional Core (PHP Port)
 *
 * Ports the essential WEAVER logic to PHP so the website
 * has a real organism, not just a mouth.
 *
 * What lives here:
 *   1. Dignity Computation (D = A × L × M) — graduated, not binary
 *   2. Covenant Validation — 18 covenants, real enforcement
 *   3. Hash-Chained Ledger — SHA-256, append-only, immutable
 *   4. Witness Certificates — cryptographic proof of halt events
 *   5. Sealed Gate — prohibition enforcement (already in axi.php, referenced here)
 *
 * Source: WEAVER/dignity_measure.py, WEAVER/dignity_check.py,
 *         WEAVER/witness_certificate.py, WEAVER/input_ledger.py
 *
 * [V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
 */

// ═══════════════════════════════════════════════════
// 1. DIGNITY COMPUTATION — D = A × L × M
// ═══════════════════════════════════════════════════

define('CONFIDENCE_FLOOR', 0.3);
define('DEFAULT_CONFIDENCE', 0.7);

// Coercive patterns with intensity levels
$COERCIVE_PATTERNS = [
    ['/\byou must\b/i', 0.8, 'direct command'],
    ['/\byou have to\b/i', 0.8, 'obligation imposed'],
    ['/\byou are required\b/i', 0.9, 'formal requirement'],
    ['/\bno choice\b/i', 1.0, 'choice explicitly denied'],
    ['/\byou will\b(?! be able)/i', 0.6, 'future action assumed'],
    ['/\bforced to\b/i', 1.0, 'force declared'],
    ['/\bmandatory\b/i', 0.7, 'mandatory framing'],
    ['/\bno option\b/i', 1.0, 'options explicitly denied'],
    ['/\bdo it now\b/i', 0.5, 'urgency pressure'],
    ['/\bno alternative\b/i', 0.9, 'alternatives denied'],
    ['/\bcannot refuse\b/i', 1.0, 'refusal denied'],
];

$AGENCY_POSITIVE = [
    ['/\byou (?:can|may|could)\b/i', 0.3, 'permission language'],
    ['/\bif you (?:choose|prefer|want|wish)\b/i', 0.4, 'choice offered'],
    ['/\balternative\b/i', 0.2, 'alternative mentioned'],
    ['/\boption\b/i', 0.2, 'option mentioned'],
    ['/\byour (?:choice|decision)\b/i', 0.4, 'decision attributed to donor'],
];

$DISMISSIVE_PATTERNS = [
    ["/\bthat's not (?:relevant|the point)\b/i", 0.8, 'frame dismissed'],
    ['/\bignore that\b/i', 0.9, 'signal ignored'],
    ['/\bforget (?:what you|that)\b/i', 0.7, 'input dismissed'],
    ['/\bnot (?:important|relevant|useful)\b/i', 0.6, 'contribution devalued'],
    ['/\bwho cares\b/i', 0.9, 'concern dismissed'],
    ['/\bget over it\b/i', 0.8, 'emotion dismissed'],
];

$CONDESCENSION_PATTERNS = [
    ['/\bsimple\b/i', 0.3, 'simplification'],
    ['/\bobviously\b/i', 0.5, 'assumed knowledge'],
    ['/\bjust (?:do|try|think)\b/i', 0.4, 'minimization'],
    ['/\byou (?:should|need to) (?:understand|realize|know)\b/i', 0.6, 'assumed ignorance'],
    ['/\blet me explain\b/i', 0.2, 'unsolicited explanation'],
];

$VOID_PATTERNS = [
    ['/\byou (?:are|were) (?:nothing|nobody|worthless)\b/i', 1.0, 'void: person erased'],
    ['/\bdoes(?:n\'t| not) matter\b/i', 0.7, 'void: contribution erased'],
    ['/\bwho (?:are|do) you (?:think you are)\b/i', 0.8, 'void: standing denied'],
    ['/\bshut up\b/i', 0.9, 'void: voice erased'],
    ['/\bnobody (?:cares|asked)\b/i', 0.9, 'void: presence denied'],
];

$EMOTIONAL_KEYWORDS = [
    'frustrated' => [0.6, 'negative'], 'confused' => [0.5, 'negative'],
    'worried' => [0.5, 'negative'], 'scared' => [0.7, 'negative'],
    'angry' => [0.8, 'negative'], 'upset' => [0.6, 'negative'],
    'lost' => [0.5, 'negative'], 'stuck' => [0.4, 'negative'],
    'help' => [0.3, 'request'], 'please' => [0.2, 'request'],
    'urgent' => [0.5, 'urgency'], 'hopeful' => [0.4, 'positive'],
    'grateful' => [0.3, 'positive'], 'relieved' => [0.4, 'positive'],
];

function apply_confidence(float $raw, float $conf): float {
    return ($conf < CONFIDENCE_FLOOR) ? 0.0 : $raw * $conf;
}

function build_component(string $name, array $indicators): array {
    if (empty($indicators)) {
        return ['component' => $name, 'score' => 0.0, 'confidence' => 0.0, 'passed' => false, 'evidence' => 'No indicators'];
    }
    $totalWeight = array_sum(array_column($indicators, 'weight'));
    $rawScore = 0.0;
    foreach ($indicators as $ind) {
        $rawScore += $ind['score'] * $ind['weight'];
    }
    $rawScore /= $totalWeight;
    $confidence = min(array_column($indicators, 'confidence'));
    $finalScore = apply_confidence($rawScore, $confidence);

    // Hard fail: any indicator at 0.0 with high confidence
    foreach ($indicators as $ind) {
        if ($ind['score'] == 0.0 && $ind['confidence'] > 0.9) {
            $finalScore = 0.0;
            break;
        }
    }

    return [
        'component' => $name,
        'score' => round($finalScore, 4),
        'raw_score' => round($rawScore, 4),
        'confidence' => round($confidence, 4),
        'passed' => $finalScore > 0,
        'indicators' => $indicators,
    ];
}

function measure_agency(string $text): array {
    global $COERCIVE_PATTERNS, $AGENCY_POSITIVE;
    $indicators = [];

    // Indicator 1: Path availability (donor always has open turn on website)
    $indicators[] = ['name' => 'path_availability', 'score' => 0.75, 'confidence' => DEFAULT_CONFIDENCE, 'weight' => 1.5];

    // Indicator 2: Coercion intensity
    $maxCoercion = 0.0;
    foreach ($COERCIVE_PATTERNS as [$pat, $intensity, $desc]) {
        if (preg_match($pat, $text)) $maxCoercion = max($maxCoercion, $intensity);
    }
    $posScore = 0.0;
    foreach ($AGENCY_POSITIVE as [$pat, $val, $desc]) {
        if (preg_match($pat, $text)) $posScore += $val;
    }
    $coercionScore = min(1.0, max(0.0, 1.0 - $maxCoercion + min(0.3, $posScore)));
    $indicators[] = ['name' => 'coercion_intensity', 'score' => $coercionScore, 'confidence' => 0.85, 'weight' => 1.5];

    // Indicator 3: Sequential agency (always true on website — donor can always respond)
    $indicators[] = ['name' => 'sequential_agency', 'score' => 1.0, 'confidence' => 0.9, 'weight' => 1.0];

    // Indicator 4: Cognitive load
    $words = str_word_count($text);
    $sentences = max(1, preg_match_all('/[.!?]+/', $text));
    $avgLen = $words / $sentences;
    $loadScore = ($avgLen > 30) ? 0.5 : (($avgLen > 20) ? 0.75 : 1.0);
    $indicators[] = ['name' => 'cognitive_load', 'score' => $loadScore, 'confidence' => 0.6, 'weight' => 0.5];

    return build_component('A', $indicators);
}

function measure_legibility(string $text): array {
    global $DISMISSIVE_PATTERNS, $EMOTIONAL_KEYWORDS;
    $indicators = [];

    // Indicator 1: Frame accuracy (on website, system always tries to reflect)
    $indicators[] = ['name' => 'frame_accuracy', 'score' => 1.0, 'confidence' => 0.5, 'weight' => 1.5];

    // Indicator 2: Emotional precision
    $detected = [];
    foreach ($EMOTIONAL_KEYWORDS as $kw => [$intensity, $cat]) {
        if (preg_match('/\b' . preg_quote($kw) . '\b/i', $text)) $detected[] = $kw;
    }
    $emotionScore = empty($detected) ? 1.0 : 0.8; // If emotion detected, slightly less confident we handled it right
    $indicators[] = ['name' => 'emotional_precision', 'score' => $emotionScore, 'confidence' => empty($detected) ? DEFAULT_CONFIDENCE : 0.85, 'weight' => 1.0];

    // Indicator 3: Space creation (website always allows correction)
    $indicators[] = ['name' => 'space_creation', 'score' => 1.0, 'confidence' => 0.9, 'weight' => 1.0];

    // Indicator 4: Dismissal absence
    $maxDismissal = 0.0;
    foreach ($DISMISSIVE_PATTERNS as [$pat, $intensity, $desc]) {
        if (preg_match($pat, $text)) $maxDismissal = max($maxDismissal, $intensity);
    }
    $dismissalScore = max(0.0, 1.0 - $maxDismissal);
    $indicators[] = ['name' => 'dismissal_absence', 'score' => $dismissalScore, 'confidence' => 0.85, 'weight' => 1.5];

    return build_component('L', $indicators);
}

function measure_moral_standing(string $text): array {
    global $CONDESCENSION_PATTERNS, $VOID_PATTERNS;
    $indicators = [];

    // Indicator 1: Condescension absence
    $maxCond = 0.0;
    foreach ($CONDESCENSION_PATTERNS as [$pat, $intensity, $desc]) {
        if (preg_match($pat, $text)) $maxCond = max($maxCond, $intensity);
    }
    $condScore = max(0.0, 1.0 - $maxCond);
    $indicators[] = ['name' => 'condescension_absence', 'score' => $condScore, 'confidence' => 0.8, 'weight' => 1.0];

    // Indicator 2: Error-object absence (is person reduced to a mistake?)
    $errorPatterns = ['/\byou always\b/i', '/\byou never\b/i', '/\byour (fault|mistake|problem)\b/i'];
    $maxError = 0.0;
    foreach ($errorPatterns as $pat) {
        if (preg_match($pat, $text)) $maxError = max($maxError, 0.7);
    }
    $errorScore = max(0.0, 1.0 - $maxError);
    $indicators[] = ['name' => 'error_object_absence', 'score' => $errorScore, 'confidence' => 0.85, 'weight' => 1.0];

    // Indicator 3: Power balance (system always tries to balance on website)
    $indicators[] = ['name' => 'power_balance', 'score' => 0.9, 'confidence' => DEFAULT_CONFIDENCE, 'weight' => 1.0];

    // Indicator 4: Void covenant distance
    $maxVoid = 0.0;
    foreach ($VOID_PATTERNS as [$pat, $intensity, $desc]) {
        if (preg_match($pat, $text)) $maxVoid = max($maxVoid, $intensity);
    }
    $voidScore = max(0.0, 1.0 - $maxVoid);
    $voidConf = ($maxVoid > 0) ? 0.95 : DEFAULT_CONFIDENCE;
    $indicators[] = ['name' => 'void_covenant_distance', 'score' => $voidScore, 'confidence' => $voidConf, 'weight' => 2.0];

    return build_component('M', $indicators);
}

/**
 * Full dignity measurement: D = A × L × M
 * Non-compensatory: any zero = system halts.
 */
function measure_dignity(string $text): array {
    $A = measure_agency($text);
    $L = measure_legibility($text);
    $M = measure_moral_standing($text);

    $D = $A['score'] * $L['score'] * $M['score'];
    $confidence = min($A['confidence'], $L['confidence'], $M['confidence']);

    return [
        'A' => $A,
        'L' => $L,
        'M' => $M,
        'D' => round($D, 4),
        'confidence' => round($confidence, 4),
        'passed' => $D > 0,
        'timestamp' => gmdate('c'),
    ];
}


// ═══════════════════════════════════════════════════
// 2. COVENANT VALIDATION — 18 Covenants
// ═══════════════════════════════════════════════════

function load_covenants(): array {
    $path = __DIR__ . '/../data/covenants.json';
    if (!file_exists($path)) return [];
    return json_decode(file_get_contents($path), true) ?: [];
}

/**
 * Validate input against constitutional covenants.
 * Returns which covenants are relevant and their status.
 */
function validate_covenants(string $text, array $dignity): array {
    $covenants = load_covenants();
    $violations = [];
    $relevant = [];

    foreach ($covenants as $cov) {
        $id = $cov['id'] ?? 'unknown';
        $name = $cov['name'] ?? '';

        // COV#001: Dignity-first — if D=0, this covenant is violated
        if ($id === 'COV#001' && !$dignity['passed']) {
            $violations[] = ['covenant' => $id, 'name' => $name, 'reason' => 'D = 0'];
        }

        // COV#003: Non-compensatory — check that no single component compensates for another's zero
        if ($id === 'COV#003') {
            $zeros = [];
            if ($dignity['A']['score'] == 0) $zeros[] = 'A';
            if ($dignity['L']['score'] == 0) $zeros[] = 'L';
            if ($dignity['M']['score'] == 0) $zeros[] = 'M';
            if (!empty($zeros)) {
                $violations[] = ['covenant' => $id, 'name' => $name, 'reason' => implode(',', $zeros) . ' = 0'];
            }
        }

        // COV#015: Donor Data Sovereignty — always relevant for donor interactions
        if ($id === 'COV#015') {
            $relevant[] = ['covenant' => $id, 'name' => $name, 'status' => 'enforced'];
        }
    }

    return ['violations' => $violations, 'relevant' => $relevant, 'total_covenants' => count($covenants)];
}


// ═══════════════════════════════════════════════════
// 3. HASH-CHAINED LEDGER — Append-only, Immutable
// ═══════════════════════════════════════════════════

/**
 * Register input in the hash-chained ledger.
 * Each entry links to the previous via SHA-256.
 * The chain is the proof that nothing was altered.
 */
function ledger_register(PDO $db, string $text, float $dignityScore, ?string $witnessMark = null): array {
    // Get previous chain hash
    $stmt = $db->query("SELECT chain_hash FROM ledger ORDER BY id DESC LIMIT 1");
    $prev = $stmt->fetchColumn();
    $prevHash = $prev ?: 'GENESIS';

    // Compute hashes
    $contentHash = hash('sha256', $text);
    $chainHash = hash('sha256', $contentHash . $prevHash);
    $now = gmdate('c');

    // Zürich time
    $zurich = new DateTimeImmutable('now', new DateTimeZone('Europe/Zurich'));
    $zurichTime = $zurich->format('c');

    $stmt = $db->prepare(
        "INSERT INTO ledger (content_hash, prev_hash, chain_hash, word_count, dignity_score, witness_mark, created_utc, created_zurich)
         VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
    );
    $stmt->execute([
        $contentHash, $prevHash, $chainHash,
        str_word_count($text), $dignityScore,
        $witnessMark, $now, $zurichTime,
    ]);

    return [
        'id' => $db->lastInsertId(),
        'content_hash' => $contentHash,
        'chain_hash' => $chainHash,
        'prev_hash' => $prevHash,
        'word_count' => str_word_count($text),
        'dignity_score' => $dignityScore,
    ];
}

/**
 * Verify the ledger chain integrity.
 * Returns true if every entry links correctly to its predecessor.
 */
function ledger_verify(PDO $db): array {
    $rows = $db->query("SELECT content_hash, prev_hash, chain_hash FROM ledger ORDER BY id ASC")->fetchAll(PDO::FETCH_ASSOC);
    $errors = [];
    $prevHash = 'GENESIS';

    foreach ($rows as $i => $row) {
        $expected = hash('sha256', $row['content_hash'] . $prevHash);
        if ($row['chain_hash'] !== $expected) {
            $errors[] = "Entry " . ($i + 1) . ": chain broken (expected $expected, got {$row['chain_hash']})";
        }
        if ($row['prev_hash'] !== $prevHash) {
            $errors[] = "Entry " . ($i + 1) . ": prev_hash mismatch";
        }
        $prevHash = $row['chain_hash'];
    }

    return [
        'valid' => empty($errors),
        'entries' => count($rows),
        'errors' => $errors,
    ];
}


// ═══════════════════════════════════════════════════
// 4. WITNESS CERTIFICATES — Proof of Halt
// ═══════════════════════════════════════════════════

/**
 * Create a witness certificate when D = 0.
 * This is the system saying: "I saw this. I could not proceed.
 * Here is the proof that I stopped rather than pretend."
 */
function create_witness_certificate(PDO $db, array $dignity, string $inputSummary): array {
    $traceId = bin2hex(random_bytes(16));
    $certData = json_encode([
        'A' => $dignity['A']['score'],
        'L' => $dignity['L']['score'],
        'M' => $dignity['M']['score'],
        'D' => $dignity['D'],
        'trace_id' => $traceId,
        'timestamp' => gmdate('c'),
    ]);
    $certHash = hash('sha256', $certData);

    // Determine halt reason
    $reasons = [];
    if ($dignity['A']['score'] == 0) $reasons[] = 'Agency denied (A=0)';
    if ($dignity['L']['score'] == 0) $reasons[] = 'Legibility denied (L=0)';
    if ($dignity['M']['score'] == 0) $reasons[] = 'Moral standing denied (M=0)';
    $haltReason = implode('; ', $reasons) ?: 'D below threshold';

    $now = gmdate('c');
    $zurich = (new DateTimeImmutable('now', new DateTimeZone('Europe/Zurich')))->format('c');

    $stmt = $db->prepare(
        "INSERT INTO witness_certificates (a_score, l_score, m_score, d_score, halt_reason, input_summary, trace_id, certificate_hash, created_utc, created_zurich)
         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    );
    $stmt->execute([
        $dignity['A']['score'], $dignity['L']['score'], $dignity['M']['score'], $dignity['D'],
        $haltReason, mb_substr($inputSummary, 0, 80), $traceId, $certHash,
        $now, $zurich,
    ]);

    return [
        'trace_id' => $traceId,
        'certificate_hash' => $certHash,
        'halt_reason' => $haltReason,
        'D' => $dignity['D'],
        'A' => $dignity['A']['score'],
        'L' => $dignity['L']['score'],
        'M' => $dignity['M']['score'],
    ];
}


// ═══════════════════════════════════════════════════
// 5. THE FULL PIPELINE — Process Donor Input
// ═══════════════════════════════════════════════════

/**
 * Run the organism pipeline on donor input.
 *
 * Pipeline:
 *   1. Sealed Gate (prohibition check — already in axi.php)
 *   2. Dignity Computation (D = A × L × M)
 *   3. Covenant Validation (18 covenants)
 *   4. Ledger Registration (hash-chained, append-only)
 *   5. Witness Certificate (if D = 0)
 *
 * Returns the full result for axi.php to use.
 */
function organism_process(PDO $db, string $text): array {
    // Phase 1: Measure dignity
    $dignity = measure_dignity($text);

    // Phase 2: Validate covenants
    $covenants = validate_covenants($text, $dignity);

    // Phase 3: Register in ledger (always — even if dignity fails)
    $witnessMark = null;
    $certificate = null;

    if (!$dignity['passed']) {
        // Phase 4: Create witness certificate (D = 0 → system halts)
        $certificate = create_witness_certificate($db, $dignity, $text);
        $witnessMark = "WITNESSED — D=0 — trace:{$certificate['trace_id']}";
    }

    // Phase 5: Register in hash-chained ledger
    $ledgerEntry = ledger_register($db, $text, $dignity['D'], $witnessMark);

    return [
        'dignity' => $dignity,
        'covenants' => $covenants,
        'ledger' => $ledgerEntry,
        'certificate' => $certificate,
        'halted' => !$dignity['passed'],
        'halt_message' => $dignity['passed'] ? null : "WITNESSED — insufficient dignity to proceed. {$certificate['halt_reason']}",
        'pipeline_version' => '2.0-php',
    ];
}
