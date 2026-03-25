<?php
/**
 * stripe.php — Payment endpoint for kalam.ch
 *
 * Creates Stripe Checkout Sessions for one-time and monthly payments.
 * No credit card form on our site — redirects to Stripe's hosted page.
 *
 * Requires: STRIPE_SECRET_KEY in config.php or environment.
 *
 * Usage:
 *   POST /api/stripe.php
 *   Body: { "amount": 10, "currency": "chf", "frequency": "once"|"monthly" }
 *   Returns: { "url": "https://checkout.stripe.com/..." }
 */

header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: https://kalam.ch');
header('Access-Control-Allow-Methods: POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(204);
    exit;
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['error' => 'POST only']);
    exit;
}

// Load config
function get_stripe_key(): ?string {
    // Check environment first
    $key = getenv('STRIPE_SECRET_KEY');
    if ($key && strlen($key) > 10) return $key;

    // Check config file
    $config_file = __DIR__ . '/../config.php';
    if (file_exists($config_file)) {
        $config = include $config_file;
        if (isset($config['STRIPE_SECRET_KEY']) && strlen($config['STRIPE_SECRET_KEY']) > 10) {
            return $config['STRIPE_SECRET_KEY'];
        }
    }

    return null;
}

$stripe_key = get_stripe_key();
if (!$stripe_key) {
    http_response_code(503);
    echo json_encode(['error' => 'Payment not configured yet. Use PayPal or TWINT.']);
    exit;
}

// Parse request
$raw = file_get_contents('php://input');
$input = json_decode($raw, true);

$amount = (int) ($input['amount'] ?? 0);
$currency = strtolower($input['currency'] ?? 'chf');
$frequency = $input['frequency'] ?? 'once';

// Validate
if ($amount < 1 || $amount > 10000) {
    http_response_code(400);
    echo json_encode(['error' => 'Amount must be between 1 and 10000']);
    exit;
}

if (!in_array($currency, ['chf', 'eur', 'usd'])) {
    http_response_code(400);
    echo json_encode(['error' => 'Currency must be chf, eur, or usd']);
    exit;
}

if (!in_array($frequency, ['once', 'monthly'])) {
    http_response_code(400);
    echo json_encode(['error' => 'Frequency must be once or monthly']);
    exit;
}

// Stripe API — create Checkout Session
$stripe_amount = $amount * 100; // Stripe uses cents
$success_url = 'https://kalam.ch/sustain?thanks=1';
$cancel_url = 'https://kalam.ch/sustain';

$line_item = [
    'price_data' => [
        'currency' => $currency,
        'product_data' => [
            'name' => 'Sustain kalam.ch',
            'description' => ($frequency === 'monthly' ? 'Monthly' : 'One-time') . ' contribution',
        ],
        'unit_amount' => $stripe_amount,
    ],
    'quantity' => 1,
];

if ($frequency === 'monthly') {
    $line_item['price_data']['recurring'] = ['interval' => 'month'];
}

$session_data = [
    'payment_method_types' => ['card'],
    'line_items' => [$line_item],
    'mode' => $frequency === 'monthly' ? 'subscription' : 'payment',
    'success_url' => $success_url,
    'cancel_url' => $cancel_url,
];

// Call Stripe API
$ch = curl_init('https://api.stripe.com/v1/checkout/sessions');
curl_setopt_array($ch, [
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_POST => true,
    CURLOPT_HTTPHEADER => [
        'Authorization: Bearer ' . $stripe_key,
        'Content-Type: application/x-www-form-urlencoded',
    ],
    CURLOPT_POSTFIELDS => http_build_query($session_data),
    CURLOPT_TIMEOUT => 15,
]);

$response = curl_exec($ch);
$http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
curl_close($ch);

if ($http_code !== 200 || !$response) {
    $error = json_decode($response, true);
    http_response_code(502);
    echo json_encode(['error' => $error['error']['message'] ?? 'Payment service unavailable']);
    exit;
}

$session = json_decode($response, true);
$url = $session['url'] ?? null;

if (!$url) {
    http_response_code(502);
    echo json_encode(['error' => 'Could not create payment session']);
    exit;
}

echo json_encode(['url' => $url]);
