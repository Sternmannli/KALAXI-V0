<?php
/**
 * Sustain API — Donation/sustenance endpoint
 *
 * Phase 0: Record sustenance intent, return manual payment info
 * Phase 1: Stripe Checkout integration (when STRIPE_SECRET_KEY is set)
 *
 * [V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
 */

header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(204);
    exit;
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['error' => 'Method not allowed']);
    exit;
}

$raw = file_get_contents('php://input');
$input = json_decode($raw, true);

$amount = (int) ($input['amount'] ?? 10);
$frequency = $input['frequency'] ?? 'once';
$currency = strtolower($input['currency'] ?? 'chf');

// Validate
if ($amount < 1 || $amount > 10000) {
    http_response_code(400);
    echo json_encode(['error' => 'Amount must be between 1 and 10000']);
    exit;
}

if (!in_array($frequency, ['once', 'monthly'])) {
    http_response_code(400);
    echo json_encode(['error' => 'Frequency must be once or monthly']);
    exit;
}

// ── Phase 1: Stripe Checkout (when configured) ──
$stripe_key = getenv('STRIPE_SECRET_KEY') ?: ($_ENV['STRIPE_SECRET_KEY'] ?? '');

if ($stripe_key) {
    // Stripe Checkout session creation
    $amount_cents = $amount * 100;

    $line_item = [
        'price_data' => [
            'currency' => $currency,
            'product_data' => [
                'name' => 'Sustain kalam.ch',
                'description' => $frequency === 'monthly'
                    ? "Monthly sustenance — CHF {$amount}/month"
                    : "One-time sustenance — CHF {$amount}",
            ],
            'unit_amount' => $amount_cents,
        ],
        'quantity' => 1,
    ];

    if ($frequency === 'monthly') {
        $line_item['price_data']['recurring'] = ['interval' => 'month'];
    }

    $session_data = [
        'mode' => $frequency === 'monthly' ? 'subscription' : 'payment',
        'line_items' => [$line_item],
        'success_url' => 'https://kalam.ch/sustain?success=1',
        'cancel_url' => 'https://kalam.ch/sustain?cancelled=1',
    ];

    $ch = curl_init('https://api.stripe.com/v1/checkout/sessions');
    curl_setopt_array($ch, [
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_POST => true,
        CURLOPT_POSTFIELDS => http_build_query($session_data),
        CURLOPT_HTTPHEADER => [
            'Authorization: Bearer ' . $stripe_key,
            'Content-Type: application/x-www-form-urlencoded',
        ],
    ]);

    $response = curl_exec($ch);
    $http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);

    if ($http_code === 200) {
        $session = json_decode($response, true);
        echo json_encode([
            'checkout_url' => $session['url'],
            'session_id' => $session['id'],
        ]);
        exit;
    }

    // Stripe error — fall through to manual
}

// ── Phase 0: No Stripe configured — return manual payment info ──
echo json_encode([
    'manual' => true,
    'amount' => $amount,
    'frequency' => $frequency,
    'currency' => $currency,
    'methods' => [
        [
            'type' => 'paypal',
            'url' => 'https://paypal.me/MohamedFarag102/' . $amount,
            'label' => 'PayPal',
        ],
        [
            'type' => 'bank',
            'iban' => 'CH93 0070 0110 0000 0000 0',
            'recipient' => 'M. Farag, Zürich',
            'label' => 'Bank Transfer (IBAN)',
        ],
        [
            'type' => 'twint',
            'label' => 'TWINT',
        ],
    ],
    'message' => 'Stripe is not yet configured. Please use one of the alternative methods.',
]);
