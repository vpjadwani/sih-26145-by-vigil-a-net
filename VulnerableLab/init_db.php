<?php
require_once 'config.php';
$pdo->exec("DROP TABLE IF EXISTS users");
$pdo->exec("DROP TABLE IF EXISTS comments");
$pdo->exec("DROP TABLE IF EXISTS files");
$pdo->exec("DROP TABLE IF EXISTS logs");
$pdo->exec("CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    fullname TEXT,
    role TEXT DEFAULT 'user'
)");
$pdo->exec("CREATE TABLE comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    comment TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)");
$pdo->exec("CREATE TABLE files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT,
    uploader_id INTEGER,
    uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP
)");
$pdo->exec("CREATE TABLE logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    action TEXT,
    ip TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)");
$hashed = password_hash('admin@1234', PASSWORD_DEFAULT);
$pdo->prepare("INSERT INTO users (username, password, fullname, role) VALUES ('admin12', ?, 'Administrator', 'admin')")
    ->execute([$hashed]);
$pdo->prepare("INSERT INTO comments (user_id, comment) VALUES (1, 'Hello, this is a test comment.')")->execute();
echo "Database initialized successfully! <a href='login.php'>Go to Login</a>";
?>
