<?php
/**
 * donor.php — Donor Account API
 *
 * Handles: registration, magic link auth, profile, history, data export.
 * Email + magic link token (no passwords). COV#015 Donor Data Sovereignty.
 *
 * Endpoints:
 *   POST /api/donor.php?action=register    { email, display_name? }
 *   POST /api/donor.php?action=verify      { token }
 *   GET  /api/donor.php?action=profile      (requires session)
 *   GET  /api/donor.php?action=history      (requires session)
 *   GET  /api/donor.php?action=export       (requires session — full data export)
 *   POST /api/donor.php?action=logout
 *
 * [V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
 */

header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') { http_response_code(204); exit; }

// ── Config ──
$config = [];
$config_path = __DIR__ . '/../data/.config';
if (file_exists($config_path)) {
    foreach (file($config_path, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES) as $line) {
        $line = trim($line);
        if (empty($line) || $line[0] === ';' || $line[0] === '#') continue;
        $parts = explode('=', $line, 2);
        if (count($parts) === 2) $config[trim($parts[0])] = trim($parts[1]);
    }
}

// ── Database ──
function getDB(array $config): ?PDO {
    if (empty($config['DB_HOST']) || empty($config['DB_NAME'])) return null;
    try {
        return new PDO(
            "mysql:host={$config['DB_HOST']};dbname={$config['DB_NAME']};charset=utf8mb4",
            $config['DB_USER'] ?? '', $config['DB_PASS'] ?? '',
            [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION, PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC]
        );
    } catch (PDOException $e) {
        return null;
    }
}

$db = getDB($config);
if (!$db) {
    http_response_code(503);
    echo json_encode(['error' => 'Database unavailable']);
    exit;
}

// ── Session ──
session_set_cookie_params([
    'lifetime' => 86400 * 30, // 30 days
    'path' => '/',
    'secure' => true,
    'httponly' => true,
    'samesite' => 'Lax',
]);
session_start();

$action = $_GET['action'] ?? '';

// ═══════════════════════════════════════
// REGISTER — create donor, send magic link
// ═══════════════════════════════════════
if ($action === 'register' && $_SERVER['REQUEST_METHOD'] === 'POST') {
    $body = json_decode(file_get_contents('php://input'), true) ?: [];
    $email = filter_var($body['email'] ?? '', FILTER_VALIDATE_EMAIL);
    $displayName = trim($body['display_name'] ?? '');

    if (!$email) {
        http_response_code(400);
        echo json_encode(['error' => 'Valid email required']);
        exit;
    }

    // Find or create donor
    $stmt = $db->prepare('SELECT id FROM donors WHERE email = ?');
    $stmt->execute([$email]);
    $donor = $stmt->fetch();

    if (!$donor) {
        $stmt = $db->prepare('INSERT INTO donors (email, display_name) VALUES (?, ?)');
        $stmt->execute([$email, $displayName ?: null]);
        $donorId = (int) $db->lastInsertId();
    } else {
        $donorId = (int) $donor['id'];
        if ($displayName) {
            $stmt = $db->prepare('UPDATE donors SET display_name = ? WHERE id = ?');
            $stmt->execute([$displayName, $donorId]);
        }
    }

    // Generate magic link token (64 hex chars, 15 min expiry)
    $token = bin2hex(random_bytes(32));
    $expiresAt = gmdate('Y-m-d H:i:s', time() + 900);

    $stmt = $db->prepare('INSERT INTO auth_tokens (donor_id, token, expires_at) VALUES (?, ?, ?)');
    $stmt->execute([$donorId, $token, $expiresAt]);

    // Send magic link email
    $link = "https://kalam.ch/api/donor.php?action=verify&token=$token";
    $sent = sendMagicLink($config, $email, $displayName ?: 'Donor', $link);

    echo json_encode([
        'status' => 'link_sent',
        'message' => 'A sign-in link has been sent to your email. It expires in 15 minutes.',
        'email_sent' => $sent,
    ]);
    exit;
}

// ═══════════════════════════════════════
// VERIFY — validate magic link token
// ═══════════════════════════════════════
if ($action === 'verify') {
    $token = $_GET['token'] ?? ($_POST['token'] ?? '');
    if (empty($token)) {
        http_response_code(400);
        echo json_encode(['error' => 'Token required']);
        exit;
    }

    $stmt = $db->prepare('SELECT t.id, t.donor_id, t.expires_at, t.used, d.email, d.display_name
                           FROM auth_tokens t JOIN donors d ON t.donor_id = d.id
                           WHERE t.token = ?');
    $stmt->execute([$token]);
    $row = $stmt->fetch();

    if (!$row) {
        http_response_code(404);
        echo json_encode(['error' => 'Invalid token']);
        exit;
    }

    if ($row['used']) {
        if ($_SERVER['REQUEST_METHOD'] === 'GET') {
            header('Location: /?auth_error=used');
            exit;
        }
        http_response_code(410);
        echo json_encode(['error' => 'Token already used']);
        exit;
    }

    if (strtotime($row['expires_at'] . ' UTC') < time()) {
        if ($_SERVER['REQUEST_METHOD'] === 'GET') {
            header('Location: /?auth_error=expired');
            exit;
        }
        http_response_code(410);
        echo json_encode(['error' => 'Token expired']);
        exit;
    }

    // Mark token used
    $stmt = $db->prepare('UPDATE auth_tokens SET used = 1 WHERE id = ?');
    $stmt->execute([$row['id']]);

    // Update last_seen
    $stmt = $db->prepare('UPDATE donors SET last_seen = CURRENT_TIMESTAMP WHERE id = ?');
    $stmt->execute([$row['donor_id']]);

    // Create session
    $_SESSION['donor_id'] = (int) $row['donor_id'];
    $_SESSION['donor_email'] = $row['email'];
    $_SESSION['donor_name'] = $row['display_name'];

    // If GET request (clicked link in email), redirect to home
    if ($_SERVER['REQUEST_METHOD'] === 'GET') {
        header('Location: /?authenticated=1');
        exit;
    }

    echo json_encode([
        'status' => 'authenticated',
        'donor' => [
            'id' => (int) $row['donor_id'],
            'email' => $row['email'],
            'display_name' => $row['display_name'],
        ],
    ]);
    exit;
}

// ═══════════════════════════════════════
// PROFILE — get donor profile (requires session)
// ═══════════════════════════════════════
if ($action === 'profile' && $_SERVER['REQUEST_METHOD'] === 'GET') {
    if (empty($_SESSION['donor_id'])) {
        http_response_code(401);
        echo json_encode(['error' => 'Not authenticated', 'authenticated' => false]);
        exit;
    }

    $donorId = (int) $_SESSION['donor_id'];
    $stmt = $db->prepare('SELECT id, email, display_name, created_at, last_seen, interaction_count, pattern_json FROM donors WHERE id = ?');
    $stmt->execute([$donorId]);
    $donor = $stmt->fetch();

    if (!$donor) {
        session_destroy();
        http_response_code(404);
        echo json_encode(['error' => 'Donor not found']);
        exit;
    }

    echo json_encode([
        'authenticated' => true,
        'donor' => [
            'id' => (int) $donor['id'],
            'email' => $donor['email'],
            'display_name' => $donor['display_name'],
            'created_at' => $donor['created_at'],
            'last_seen' => $donor['last_seen'],
            'interaction_count' => (int) $donor['interaction_count'],
            'pattern' => $donor['pattern_json'] ? json_decode($donor['pattern_json'], true) : null,
        ],
    ]);
    exit;
}

// ═══════════════════════════════════════
// HISTORY — get donor's interactions (requires session)
// ═══════════════════════════════════════
if ($action === 'history' && $_SERVER['REQUEST_METHOD'] === 'GET') {
    if (empty($_SESSION['donor_id'])) {
        http_response_code(401);
        echo json_encode(['error' => 'Not authenticated']);
        exit;
    }

    $donorId = (int) $_SESSION['donor_id'];
    $limit = min((int) ($_GET['limit'] ?? 50), 200);
    $offset = max((int) ($_GET['offset'] ?? 0), 0);

    $stmt = $db->prepare('SELECT input_text, axi_response, register, witness_mark, created_at
                           FROM interactions WHERE donor_id = ? ORDER BY created_at DESC LIMIT ? OFFSET ?');
    $stmt->execute([$donorId, $limit, $offset]);
    $rows = $stmt->fetchAll();

    $stmt = $db->prepare('SELECT COUNT(*) as total FROM interactions WHERE donor_id = ?');
    $stmt->execute([$donorId]);
    $total = (int) $stmt->fetch()['total'];

    echo json_encode([
        'total' => $total,
        'limit' => $limit,
        'offset' => $offset,
        'interactions' => $rows,
    ]);
    exit;
}

// ═══════════════════════════════════════
// EXPORT — full data export (COV#015 Donor Data Sovereignty)
// ═══════════════════════════════════════
if ($action === 'export' && $_SERVER['REQUEST_METHOD'] === 'GET') {
    if (empty($_SESSION['donor_id'])) {
        http_response_code(401);
        echo json_encode(['error' => 'Not authenticated']);
        exit;
    }

    $donorId = (int) $_SESSION['donor_id'];

    // Get profile
    $stmt = $db->prepare('SELECT id, email, display_name, created_at, last_seen, interaction_count, pattern_json FROM donors WHERE id = ?');
    $stmt->execute([$donorId]);
    $donor = $stmt->fetch();

    // Get ALL interactions
    $stmt = $db->prepare('SELECT input_text, axi_response, register, witness_mark, content_hash, created_at
                           FROM interactions WHERE donor_id = ? ORDER BY created_at ASC');
    $stmt->execute([$donorId]);
    $interactions = $stmt->fetchAll();

    // Build export
    $export = [
        'export_version' => '1.0',
        'exported_at' => gmdate('c'),
        'covenant' => 'COV#015 — Your data belongs to you. This is your complete record.',
        'donor' => [
            'email' => $donor['email'],
            'display_name' => $donor['display_name'],
            'member_since' => $donor['created_at'],
            'interaction_count' => (int) $donor['interaction_count'],
            'pattern' => $donor['pattern_json'] ? json_decode($donor['pattern_json'], true) : null,
        ],
        'interactions' => $interactions,
    ];

    // Set download headers
    header('Content-Disposition: attachment; filename="kalam-export-' . date('Y-m-d') . '.json"');
    echo json_encode($export, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
    exit;
}

// ═══════════════════════════════════════
// LOGOUT
// ═══════════════════════════════════════
if ($action === 'logout') {
    session_destroy();
    echo json_encode(['status' => 'logged_out']);
    exit;
}

// ═══════════════════════════════════════
// Unknown action
// ═══════════════════════════════════════
http_response_code(400);
echo json_encode(['error' => 'Unknown action. Valid: register, verify, profile, history, export, logout']);
exit;


// ═══════════════════════════════════════
// HELPERS
// ═══════════════════════════════════════

/**
 * Send magic link email via PHP mail() or SMTP if configured.
 */
function sendMagicLink(array $config, string $email, string $name, string $link): bool {
    $subject = 'Your sign-in link — kalam.ch';
    $body = <<<EOT
$name,

Here is your sign-in link for kalam.ch:

$link

This link expires in 15 minutes. Click it once. You will be signed in.

No password. No account to remember. Just your email and your word.

— AXI
EOT;

    $headers = [
        'From' => $config['SMTP_FROM'] ?? 'noreply@kalam.ch',
        'Reply-To' => $config['SMTP_FROM'] ?? 'noreply@kalam.ch',
        'Content-Type' => 'text/plain; charset=UTF-8',
        'X-Mailer' => 'kalam.ch',
    ];

    $headerStr = '';
    foreach ($headers as $k => $v) $headerStr .= "$k: $v\r\n";

    return @mail($email, $subject, $body, $headerStr);
}
