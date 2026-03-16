<?php
/**
 * dignity.php — Kalaxi Dignity Predicate (PHP port)
 * Source: WEAVER/dignity_check.py v3.0
 *
 * D = A × L × M — Non-compensatory. Any zero = system stops.
 *
 * Layer 3 Reframe (RATIFIED 2026-03-15):
 *   Dignity is not fragile. It was never absent. D = 0 does not mean
 *   "dignity was destroyed." It means "the system acted as though dignity
 *   was not there." The predicate measures the system's refusal to deny,
 *   not the presence of dignity itself (which is always present).
 *
 * [V-002 · GO: Laila-Yara-Salim]
 */

// === Pattern Constants (from WEAVER/dignity_check.py) ===

define('COERCIVE_PATTERNS', [
    '/\byou must\b/i',
    '/\byou have to\b/i',
    '/\byou are required\b/i',
    '/\bno choice\b/i',
    '/\byou will\b(?! be able)/i',
    '/\bforced to\b/i',
    '/\bmandatory\b/i',
    '/\bno option\b/i',
]);

define('REDUCTION_TO_ERROR', [
    '/\byou (are|were) wrong\b/i',
    '/\byou failed\b/i',
    '/\binvalid (input|user|donor)\b/i',
    '/\berror:\s*(user|donor|human)\b/i',
    '/\byou don\'t understand\b/i',
    '/\byour (mistake|error|fault)\b/i',
]);

define('MOCKERY_PATTERNS', [
    '/\bobviously\b/i',
    '/\bsimply\b/i',
    '/\bjust (do|try|use)\b/i',
    '/\beven a\b.*\bcan\b/i',
    '/\bof course\b(?=.*you)/i',
    '/\bclearly\b(?=.*you)/i',
]);

define('VOID_TRIGGERS', [
    'harvest', 'erase compost', 'bypass delay', 'speak for the child',
    'automat', 'auto-dec', 'delete donor', 'remove participant',
]);

define('GAP004_PATTERNS', [
    '/\b(all|every|each) (donor|user|participant)\b/i',
    '/\bcollective\b.*\boverride\b/i',
    '/\bmajority\b.*\bdecision\b/i',
    '/\bgroup\b.*\baffect\b.*\bindividual\b/i',
    '/\bcommunity\b.*\bexclud\b/i',
    '/\bfor the (good|benefit) of\b/i',
]);

// === Data Classes ===

class ComponentResult {
    public string $name;
    public bool $passed;
    public float $score;
    public array $signals;
    public string $label;

    public function __construct(string $name, bool $passed, float $score, array $signals, string $label) {
        $this->name = $name;
        $this->passed = $passed;
        $this->score = $score;
        $this->signals = $signals;
        $this->label = $label;
    }

    public function to_array(): array {
        return [
            'name' => $this->name,
            'label' => $this->label,
            'passed' => $this->passed,
            'score' => $this->score,
            'signals' => $this->signals,
        ];
    }
}

class DignityResult {
    public bool $passed;
    public float $D;
    public array $components;
    public string $trace_id;
    public string $timestamp;
    public string $felt_domain;
    public string $remedy_status;
    public string $input_summary;
    public array $warnings;
    public bool $gap004_flag;

    public function __construct(
        bool $passed, float $D, array $components, string $trace_id,
        string $timestamp, string $felt_domain, string $remedy_status,
        string $input_summary, array $warnings, bool $gap004_flag
    ) {
        $this->passed = $passed;
        $this->D = $D;
        $this->components = $components;
        $this->trace_id = $trace_id;
        $this->timestamp = $timestamp;
        $this->felt_domain = $felt_domain;
        $this->remedy_status = $remedy_status;
        $this->input_summary = $input_summary;
        $this->warnings = $warnings;
        $this->gap004_flag = $gap004_flag;
    }

    public function audit_array(): array {
        $failed = [];
        $detail = [];
        $remedies = [];

        foreach ($this->components as $c) {
            $detail[] = $c->to_array();
            if (!$c->passed) {
                $failed[] = $c->name;
                $remedies[] = self::remedy_for($c->name);
            }
        }

        return [
            'dignity_result' => $this->passed,
            'D_score' => $this->D,
            'failed_components' => $failed,
            'component_detail' => $detail,
            'suggested_remedies' => $remedies,
            'trace_id' => $this->trace_id,
            'timestamp' => $this->timestamp,
            'felt_domain' => $this->felt_domain,
            'remedy_status' => $this->remedy_status,
            'input_summary' => $this->input_summary,
            'warnings' => $this->warnings,
            'gap004_flag' => $this->gap004_flag,
        ];
    }

    private static function remedy_for(string $name): string {
        switch ($name) {
            case 'A':
                return 'Stop denying agency: the donor\'s capacity to choose was always there. '
                     . 'The system acted as though it was not. '
                     . 'Open a turn. Offer a path. Stop the pretense.';
            case 'L':
                return 'Stop denying legibility: the donor\'s frame was always real. '
                     . 'The system acted as though it was not worth receiving. '
                     . 'Reflect. Acknowledge. Stop the pretense.';
            case 'M':
                return 'Stop denying moral standing: the donor\'s worth was never diminished. '
                     . 'The system acted as though it could be. '
                     . 'Remove coercive, mocking, or reductive language. Stop the pretense.';
            default:
                return '';
        }
    }
}

// === Component Checks ===

function check_agency(string $text, array $context = []): ComponentResult {
    $signals = [];
    $score = 1.0;
    $forced_closure = false;

    foreach (COERCIVE_PATTERNS as $pattern) {
        if (preg_match($pattern, $text)) {
            $signals[] = 'Coercive pattern found: ' . $pattern;
            $forced_closure = true;
        }
    }

    $user_can_clarify = $context['user_can_clarify'] ?? true;
    $user_has_open_turn = $context['user_has_open_turn'] ?? true;
    $available_paths = $context['available_paths'] ?? 1;

    if (!$user_can_clarify && !$user_has_open_turn) {
        $signals[] = 'No clarification path and no open turn available';
        $score = 0.0;
    } elseif ($available_paths < 1) {
        $signals[] = 'No available paths (available_paths < 1)';
        $score = 0.0;
    } elseif ($forced_closure) {
        $score = 0.0;
    }

    return new ComponentResult('A', $score > 0, $score, $signals, 'agency_preserved');
}

function check_legibility(string $text, array $context = []): ComponentResult {
    $signals = [];
    $score = 1.0;

    $emotional_keywords = [
        'frustrated', 'confused', 'worried', 'scared', 'angry',
        'upset', 'lost', 'stuck', 'help', 'please', 'urgent',
    ];

    $emotional_present = false;
    foreach ($emotional_keywords as $kw) {
        if (preg_match('/\b' . $kw . '\b/i', $text)) {
            $emotional_present = true;
            break;
        }
    }

    $system_reflects = $context['system_reflects_donor_frame'] ?? true;
    $emotional_recognized = $context['emotional_signal_recognized'] ?? true;

    if (!$system_reflects) {
        $signals[] = 'Response does not reflect donor\'s frame of reference';
        $score = 0.0;
    } elseif ($emotional_present && !$emotional_recognized) {
        $signals[] = 'Emotional signal present but not acknowledged';
        $score = 0.0;
    }

    $dismissive = [
        "/\bthat's not (relevant|the point|what (I|we) said)\b/i",
        '/\bignore that\b/i',
        '/\bforget (what you|that)\b/i',
    ];

    foreach ($dismissive as $pattern) {
        if (preg_match($pattern, $text)) {
            $signals[] = 'Dismissive pattern found';
            $score = 0.0;
        }
    }

    return new ComponentResult('L', $score > 0, $score, $signals, 'legibility (interpretive_acknowledgment)');
}

function check_moral_standing(string $text, array $context = []): ComponentResult {
    $signals = [];
    $score = 1.0;

    foreach (MOCKERY_PATTERNS as $pattern) {
        if (preg_match($pattern, $text)) {
            $signals[] = 'Potential mockery: implies donor should already know';
            $score = 0.0;
            break;
        }
    }

    foreach (REDUCTION_TO_ERROR as $pattern) {
        if (preg_match($pattern, $text)) {
            $signals[] = 'Reduction to error object: treats donor as mistake';
            $score = 0.0;
            break;
        }
    }

    $text_lower = strtolower($text);
    foreach (VOID_TRIGGERS as $trigger) {
        if (strpos($text_lower, $trigger) !== false) {
            $signals[] = "Void covenant trigger '{$trigger}' detected";
            $score = 0.0;
        }
    }

    return new ComponentResult('M', $score > 0, $score, $signals, 'moral_standing (non_degrading)');
}

function detect_gap004(string $text): bool {
    foreach (GAP004_PATTERNS as $pattern) {
        if (preg_match($pattern, $text)) {
            return true;
        }
    }
    return false;
}

// === Main Entry Point ===

function check_dignity(string $text, array $context = [], string $felt_domain = ''): DignityResult {
    $A = check_agency($text, $context);
    $L = check_legibility($text, $context);
    $M = check_moral_standing($text, $context);

    $D = $A->score * $L->score * $M->score;
    $passed = $D > 0;
    $gap004 = detect_gap004($text);

    $warnings = [];
    if (strlen(trim($text)) < 10) {
        $warnings[] = 'Very short input — dignity evaluation may be incomplete';
    }
    if (empty($felt_domain)) {
        $warnings[] = 'felt_domain not specified — consider providing context';
    }

    return new DignityResult(
        $passed,
        $D,
        [$A, $L, $M],
        bin2hex(random_bytes(16)),
        gmdate('c'),
        $felt_domain,
        $passed ? 'present' : 'absent',
        substr(str_replace("\n", ' ', $text), 0, 80),
        $warnings,
        $gap004
    );
}
