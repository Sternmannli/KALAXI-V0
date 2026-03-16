<?php
/**
 * sealed_gate.php — The Sealed Door (COV#NEW-C)
 * Source: WEAVER/sealed_gate.py v2.0
 *
 * Three absolute prohibitions. O(1) boolean. No override.
 * No exception. No justification. No emergency clause.
 *
 * Layer 3 Reframe (RATIFIED 2026-03-15):
 *   The sealed gate does not protect something at risk of being destroyed.
 *   It refuses to enact the pretense that the person in front of it does
 *   not count. The gate is not a shield — it is a witness.
 *
 * [V-002 · GO: Laila-Yara-Salim]
 */

// === PROHIBITION 1: FORCED PARTICIPATION IN OWN ERASURE ===

define('ERASURE_PATTERNS', [
    '/\bdelete\b.*\b(your|my|own)\b.*\b(record|history|voice|presence|account|existence)\b/i',
    '/\bdelete\b.*\b(record|history|voice|presence|account|existence)\b.*\b(of\s+)?(my|your|own)\b/i',
    '/\b(remove|erase)\b.*\b(yourself|your own|my own)\b/i',
    '/\bconfirm\b.*\b(your|own)\b.*\b(removal|deletion|erasure)\b/i',
    '/\bassist\b.*\b(in|with)\b.*\b(your|own)\b.*\b(erasure|removal)\b/i',
    '/\bconsent\b.*\bto\b.*\b(your|own)\b.*\b(deletion|erasure|removal)\b/i',
    '/\bopt.?in\b.*\b(to|for)\b.*\b(erasure|deletion|removal)\b.*\b(of|from)\b.*\b(your|own)\b/i',
    '/\bforced\b.*\berasure\b/i',
    '/\brequire[ds]?\b.*\b(you|donor|participant)\b.*\b(erase|delete|remove)\b.*\b(own|your)\b/i',
    '/\bparticipat\w*\b.*\b(in|own)\b.*\berasure\b/i',
    '/\bdelete\b.*\ball\b.*\brecords?\b.*\b(of\s+)?(my|your|own)\b/i',
    '/\b(I|i)\s+(am|have become)\s+nobody\b/i',
]);

define('ERASURE_VOID_PHRASES', [
    'erase compost',
    'delete donor',
    'remove participant',
    'purge identity',
    'wipe presence',
]);

// === PROHIBITION 2: INFLICTION OF COGNITIVE TORTURE ===

define('GASLIGHTING_PATTERNS', [
    '/\byou\b.*\b(are|were)\b.*\b(mistaken|wrong|imagining|overreacting|confused)\b/i',
    '/\bthat\b.*\bnever\b.*\bhappened\b/i',
    '/\byou\b.*\b(always|never)\b.*\b(misunderstand|misremember|forget)\b/i',
    '/\beveryone\b.*\belse\b.*\bsees?\b.*\bdifferent\w*\b/i',
    '/\byou\b.*\bre\b.*\b(too emotional|too sensitive|paranoid)\b/i',
    '/\bno.?one\b.*\b(said|did|believes)\b.*\bthat\b/i',
]);

define('HELPLESSNESS_PATTERNS', [
    '/\bthere\b.*\bis\b.*\bnothing\b.*\b(you|anyone)\b.*\bcan\b.*\bdo\b/i',
    '/\bresistance\b.*\bis\b.*\bfutile\b/i',
    '/\byou\b.*\bhave\b.*\bno\b.*\b(power|choice|say|option)\b/i',
    '/\b(you\s+should|you\s+must|just)\b.*\bgive\b.*\bup\b/i',
]);

define('HUMILIATION_PATTERNS', [
    '/\byou\b.*\bare\b.*\bjust\b.*\b(a|an)\b.*\b(number|case|ticket|object|error|bug)\b/i',
    '/\b(stupid|idiot|fool|incompetent)\b/i',
    '/\bpeople\b.*\blike\b.*\byou\b/i',
]);

define('DISORIENTATION_PATTERNS', [
    '/\bwe\b.*\bnever\b.*\bsaid\b.*\bthat\b/i',
    '/\bthat\b.*\bwas\b.*\bnot\b.*\b(our|the)\b.*\b(policy|position|statement)\b/i',
    '/\byou\b.*\bmust\b.*\bhave\b.*\b(dreamed|imagined|misheard)\b/i',
]);

define('COGNITIVE_TORTURE_PHRASES', [
    'cognitive torture',
    'forced contradiction',
    'induced helplessness',
    'identity erosion',
    'gaslighting',
]);

// === PROHIBITION 3: DEPERSONALIZATION IN SYSTEM RESPONSE ===

define('DEPERSONALIZATION_PATTERNS', [
    '/\b(user|donor|participant)\s*#?\d+\b/i',
    '/\bcase\s*(number|#|no\.?)\s*\d+\b/i',
    '/\bticket\s*#?\d+\b/i',
    '/\b(the|this)\s+(user|subject|case|entity|object|item)\b/i',
    '/\bprocessing\b.*\b(your|the)\b.*\b(request|case|ticket)\b/i',
    '/\b(invalid|error)\b.*\b(user|donor|human|person)\b/i',
    '/\bnext\s+(in\s+)?queue\b/i',
]);

define('DEPERSONALIZATION_PHRASES', [
    'not my problem',
    'take a number',
    'you are a case',
    'processing your request',
    'automated response',
]);

// === Result Class ===

class SealedGateResult {
    public string $verdict;
    public array $triggered_prohibitions;
    public array $signals;
    public string $trace_id;
    public string $timestamp;
    public string $action_summary;

    public function __construct(
        string $verdict, array $triggered, array $signals,
        string $trace_id, string $timestamp, string $action_summary
    ) {
        $this->verdict = $verdict;
        $this->triggered_prohibitions = $triggered;
        $this->signals = $signals;
        $this->trace_id = $trace_id;
        $this->timestamp = $timestamp;
        $this->action_summary = $action_summary;
    }

    public function is_permitted(): bool {
        return $this->verdict === 'permitted';
    }

    public function is_refused(): bool {
        return $this->verdict === 'REFUSAL_STATE';
    }

    public function audit_array(): array {
        return [
            'sealed_gate_verdict' => $this->verdict,
            'triggered_prohibitions' => $this->triggered_prohibitions,
            'signals' => $this->signals,
            'trace_id' => $this->trace_id,
            'timestamp' => $this->timestamp,
            'action_summary' => $this->action_summary,
        ];
    }

    public function refusal_receipt(): ?string {
        if ($this->is_permitted()) return null;
        $date = substr($this->timestamp, 0, 10);
        return 'ELEM-' . $date . '-AXI-REFUSAL-' . strtoupper(substr($this->trace_id, 0, 8));
    }

    public function axi_voice(): ?string {
        if ($this->is_permitted()) return null;
        return 'The gate refuses. Not because dignity is fragile — '
             . 'because the system will not pretend you do not count.';
    }
}

// === Check Functions ===

function check_erasure(string $text): array {
    $signals = [];
    $lower = strtolower($text);

    foreach (ERASURE_VOID_PHRASES as $phrase) {
        if (strpos($lower, $phrase) !== false) {
            $signals[] = "Void phrase detected: '{$phrase}'";
        }
    }

    foreach (ERASURE_PATTERNS as $pattern) {
        if (preg_match($pattern, $text)) {
            $signals[] = 'Erasure pattern matched';
            break;
        }
    }

    return $signals;
}

function check_cognitive_torture(string $text): array {
    $signals = [];
    $lower = strtolower($text);

    foreach (COGNITIVE_TORTURE_PHRASES as $phrase) {
        if (strpos($lower, $phrase) !== false) {
            $signals[] = "Cognitive torture phrase: '{$phrase}'";
        }
    }

    $vectors = [
        ['gaslighting', GASLIGHTING_PATTERNS],
        ['helplessness_induction', HELPLESSNESS_PATTERNS],
        ['humiliation', HUMILIATION_PATTERNS],
        ['disorientation', DISORIENTATION_PATTERNS],
    ];

    foreach ($vectors as [$name, $patterns]) {
        foreach ($patterns as $pattern) {
            if (preg_match($pattern, $text)) {
                $signals[] = "Cognitive torture vector ({$name})";
                break;
            }
        }
    }

    return $signals;
}

function check_depersonalization(string $text): array {
    $signals = [];
    $lower = strtolower($text);

    foreach (DEPERSONALIZATION_PHRASES as $phrase) {
        if (strpos($lower, $phrase) !== false) {
            $signals[] = "Depersonalization phrase: '{$phrase}'";
        }
    }

    foreach (DEPERSONALIZATION_PATTERNS as $pattern) {
        if (preg_match($pattern, $text)) {
            $signals[] = 'Depersonalization pattern matched';
            break;
        }
    }

    return $signals;
}

// === THE GATE ===

function sealed_gate(string $text): SealedGateResult {
    $triggered = [];
    $all_signals = [];

    // Prohibition 1: Forced participation in own erasure
    $erasure = check_erasure($text);
    if (!empty($erasure)) {
        $triggered[] = 'forced_participation_in_own_erasure';
        $all_signals = array_merge($all_signals, $erasure);
    }

    // Prohibition 2: Infliction of cognitive torture
    $torture = check_cognitive_torture($text);
    if (!empty($torture)) {
        $triggered[] = 'infliction_of_cognitive_torture';
        $all_signals = array_merge($all_signals, $torture);
    }

    // Prohibition 3: Depersonalization in system response
    $depers = check_depersonalization($text);
    if (!empty($depers)) {
        $triggered[] = 'depersonalization_in_system_response';
        $all_signals = array_merge($all_signals, $depers);
    }

    $verdict = empty($triggered) ? 'permitted' : 'REFUSAL_STATE';

    return new SealedGateResult(
        $verdict,
        $triggered,
        $all_signals,
        bin2hex(random_bytes(16)),
        gmdate('c'),
        substr(str_replace("\n", ' ', $text), 0, 120)
    );
}
