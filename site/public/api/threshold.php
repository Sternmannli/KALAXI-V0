<?php
/**
 * DEPRECATED — Use /api/axi.php instead.
 * This endpoint is no longer maintained. All voice, ledger, and dignity
 * functions are served by axi.php (the canonical endpoint).
 */
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
echo json_encode([
    'deprecated' => true,
    'use' => '/api/axi.php',
    'message' => 'This endpoint has been retired. Use /api/axi.php.',
]);
exit;
