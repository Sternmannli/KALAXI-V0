<?php
/**
 * connect.php — Donor Connection Endpoint
 * Handles: newsletter signup, feedback messages, collaboration inquiries
 *
 * Stores in MySQL (faragmoh_ty30) with dignity-first approach.
 * No tracking. No analytics. Just connection.
 *
 * [V-002 · GO: Laila-Yara-Salim]
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
    echo json_encode(['error' => 'POST only']);
    exit;
}

// Read config
$config = [];
$config_path = __DIR__ . '/../data/.config';
if (file_exists($config_path)) {
    foreach (file($config_path, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES) as $line) {
        $line = trim($line);
        if (empty($line) || $line[0] === '#') continue;
        $parts = explode('=', $line, 2);
        if (count($parts) === 2) {
            $config[trim($parts[0])] = trim($parts[1]);
        }
    }
}

// Parse input
$raw = file_get_contents('php://input');
$data = json_decode($raw, true);
if (!$data) {
    // Try form-encoded
    $data = $_POST;
}

$type = $data['type'] ?? '';
$email = trim($data['email'] ?? '');

// Validate email
if (empty($email) || !filter_var($email, FILTER_VALIDATE_EMAIL)) {
    http_response_code(400);
    echo json_encode(['error' => 'Valid email required']);
    exit;
}

// Rate limit: max 5 submissions per email per hour (stored in file)
$rate_dir = sys_get_temp_dir() . '/kalam_rate';
if (!is_dir($rate_dir)) @mkdir($rate_dir, 0700, true);
$rate_file = $rate_dir . '/' . md5($email) . '.json';
$rate_data = file_exists($rate_file) ? json_decode(file_get_contents($rate_file), true) : [];
$now = time();
$rate_data = array_filter($rate_data ?? [], fn($t) => ($now - $t) < 3600);
if (count($rate_data) >= 5) {
    http_response_code(429);
    echo json_encode(['error' => 'Too many submissions. Please try again later.']);
    exit;
}
$rate_data[] = $now;
file_put_contents($rate_file, json_encode($rate_data));

// Connect to MySQL
$db = null;
if (!empty($config['DB_HOST']) && !empty($config['DB_NAME'])) {
    try {
        $db = new PDO(
            "mysql:host={$config['DB_HOST']};dbname={$config['DB_NAME']};charset=utf8mb4",
            $config['DB_USER'] ?? '',
            $config['DB_PASS'] ?? '',
            [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION]
        );

        // Ensure table exists
        $db->exec("CREATE TABLE IF NOT EXISTS connections (
            id INT AUTO_INCREMENT PRIMARY KEY,
            type ENUM('newsletter', 'feedback', 'collaboration') NOT NULL,
            email VARCHAR(255) NOT NULL,
            name VARCHAR(255) DEFAULT NULL,
            message TEXT DEFAULT NULL,
            expertise VARCHAR(500) DEFAULT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            INDEX idx_type (type),
            INDEX idx_email (email)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4");
    } catch (PDOException $e) {
        // Fall back to file storage
        $db = null;
    }
}

// Process by type
switch ($type) {
    case 'newsletter':
        $result = store_connection($db, 'newsletter', $email);
        if ($result) {
            echo json_encode([
                'ok' => true,
                'message' => 'Witnessed. You will hear from us.'
            ]);
        }
        break;

    case 'feedback':
        $message = trim($data['message'] ?? '');
        if (empty($message)) {
            http_response_code(400);
            echo json_encode(['error' => 'Message required']);
            exit;
        }
        if (strlen($message) > 5000) {
            http_response_code(400);
            echo json_encode(['error' => 'Message too long (max 5000 characters)']);
            exit;
        }
        $result = store_connection($db, 'feedback', $email, $data['name'] ?? null, $message);
        if ($result) {
            echo json_encode([
                'ok' => true,
                'message' => 'Received. Your word has weight here.'
            ]);
        }
        break;

    case 'collaboration':
        $name = trim($data['name'] ?? '');
        $message = trim($data['message'] ?? '');
        $expertise = trim($data['expertise'] ?? '');
        if (empty($name) || empty($message)) {
            http_response_code(400);
            echo json_encode(['error' => 'Name and message required']);
            exit;
        }
        $result = store_connection($db, 'collaboration', $email, $name, $message, $expertise);
        if ($result) {
            echo json_encode([
                'ok' => true,
                'message' => 'Your proposal is witnessed. We will reach out.'
            ]);
        }
        break;

    default:
        http_response_code(400);
        echo json_encode(['error' => 'Unknown type. Use: newsletter, feedback, or collaboration']);
        exit;
}

// --- Storage ---

function store_connection(?PDO $db, string $type, string $email, ?string $name = null, ?string $message = null, ?string $expertise = null): bool {
    if ($db) {
        try {
            $stmt = $db->prepare("INSERT INTO connections (type, email, name, message, expertise) VALUES (?, ?, ?, ?, ?)");
            $stmt->execute([$type, $email, $name, $message, $expertise]);
            return true;
        } catch (PDOException $e) {
            // Fall through to file storage
        }
    }

    // File fallback
    $file = __DIR__ . '/../data/connections.jsonl';
    $dir = dirname($file);
    if (!is_dir($dir)) @mkdir($dir, 0755, true);
    $entry = json_encode([
        'type' => $type,
        'email' => $email,
        'name' => $name,
        'message' => $message,
        'expertise' => $expertise,
        'timestamp' => gmdate('c'),
    ]) . "\n";
    file_put_contents($file, $entry, FILE_APPEND | LOCK_EX);
    return true;
}
