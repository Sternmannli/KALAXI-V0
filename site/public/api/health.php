<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');

echo json_encode([
    'status' => 'ok',
    'timestamp' => gmdate('c'),
    'php' => phpversion(),
    'sqlite' => class_exists('SQLite3') ? 'yes' : 'no',
    'pdo_mysql' => extension_loaded('pdo_mysql') ? 'yes' : 'no',
]);
