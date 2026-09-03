<?php
session_start();
$db_file = __DIR__ . '/db/lab.db';
try {
    $pdo = new PDO("sqlite:$db_file");
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch (PDOException $e) {
    die("Database error: " . $e->getMessage());
}
define('BASE_URL', 'http://localhost:8080/');
function isLoggedIn() {
    return isset($_SESSION['user_id']);
}
function redirect($url) {
    header("Location: $url");
    exit;
}
?>
