<?php
/**
 * migrate.php — AXI Database Setup
 *
 * Creates all tables needed by axi.php.
 * Token-protected: GET /api/migrate.php?token=YOUR_TOKEN
 *
 * [V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
 */

header('Content-Type: application/json');

// Token check
$config = [];
$config_path = __DIR__ . '/../data/.config';
if (file_exists($config_path)) {
    foreach (file($config_path, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES) as $line) {
        $line = trim($line);
        if (empty($line) || $line[0] === '#') continue;
        $parts = explode('=', $line, 2);
        if (count($parts) === 2) $config[trim($parts[0])] = trim($parts[1]);
    }
}

$token = $config['MIGRATE_TOKEN'] ?? 'kalam-setup-2026';
if (($_GET['token'] ?? '') !== $token) {
    http_response_code(403);
    echo json_encode(['error' => 'Invalid token']);
    exit;
}

// Connect MySQL
if (empty($config['DB_HOST']) || empty($config['DB_NAME'])) {
    echo json_encode(['error' => 'Database not configured in .config']);
    exit;
}

try {
    $db = new PDO(
        "mysql:host={$config['DB_HOST']};dbname={$config['DB_NAME']};charset=utf8mb4",
        $config['DB_USER'] ?? '', $config['DB_PASS'] ?? '',
        [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION]
    );
} catch (PDOException $e) {
    echo json_encode(['error' => 'Connection failed: ' . $e->getMessage()]);
    exit;
}

$results = [];

// Table 1: Hash-chained ledger (no raw text — privacy by architecture)
try {
    $db->exec("CREATE TABLE IF NOT EXISTS ledger (
        id INT AUTO_INCREMENT PRIMARY KEY,
        content_hash VARCHAR(64) NOT NULL COMMENT 'SHA-256 of raw text',
        prev_hash VARCHAR(64) NOT NULL COMMENT 'Previous chain_hash or GENESIS',
        chain_hash VARCHAR(64) NOT NULL COMMENT 'SHA-256(content_hash + prev_hash)',
        word_count INT NOT NULL,
        dignity_score FLOAT NOT NULL DEFAULT 1.0,
        witness_mark TEXT DEFAULT NULL,
        created_utc VARCHAR(30) NOT NULL,
        created_zurich VARCHAR(30) NOT NULL,
        INDEX idx_chain (chain_hash),
        INDEX idx_created (created_utc)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Hash-chained append-only ledger. No raw text stored.'");
    $results[] = 'ledger: OK';
} catch (PDOException $e) {
    $results[] = 'ledger: ' . $e->getMessage();
}

// Table 2: Witness certificates (D=0 events)
try {
    $db->exec("CREATE TABLE IF NOT EXISTS witness_certificates (
        id INT AUTO_INCREMENT PRIMARY KEY,
        a_score FLOAT NOT NULL,
        l_score FLOAT NOT NULL,
        m_score FLOAT NOT NULL,
        d_score FLOAT NOT NULL,
        halt_reason TEXT NOT NULL,
        input_summary VARCHAR(80) NOT NULL COMMENT 'Truncated, not full text',
        trace_id VARCHAR(32) NOT NULL,
        certificate_hash VARCHAR(64) NOT NULL,
        created_utc VARCHAR(30) NOT NULL,
        created_zurich VARCHAR(30) NOT NULL,
        INDEX idx_hash (certificate_hash),
        INDEX idx_created (created_utc)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Witness certificates for dignity halt events.'");
    $results[] = 'witness_certificates: OK';
} catch (PDOException $e) {
    $results[] = 'witness_certificates: ' . $e->getMessage();
}

// Table 3: Connections (newsletter, feedback, collaboration)
try {
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
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Donor connection forms.'");
    $results[] = 'connections: OK';
} catch (PDOException $e) {
    $results[] = 'connections: ' . $e->getMessage();
}

echo json_encode([
    'status' => 'migration complete',
    'tables' => $results,
    'database' => $config['DB_NAME'],
    'timestamp' => gmdate('c'),
], JSON_PRETTY_PRINT);
