#!/usr/bin/env python3
import os
import zipfile

# ----------------------------------------------------------------------
#  File contents, keyed by relative path
# ----------------------------------------------------------------------
files = {

    # ========== ROOT ==========
    "README.md": """# Vulnerable Web Application Training Lab

This is a **local educational environment** for learning web application security and penetration testing.

⚠️ **IMPORTANT**: Use only on your own machine. Never expose this to the public internet.

## Features
- SQL Injection (login bypass, search, union)
- Cross‑Site Scripting (reflected, stored, DOM)
- Broken Authentication & IDOR
- Directory Traversal
- Insecure File Upload
- CSRF
- Secure counterparts for comparison
- Learning mode with OWASP explanations

## Installation
1. Clone or extract this folder.
2. Run `php -S localhost:8080` from the project root.
3. Visit `http://localhost:8080/init_db.php` once to create the SQLite database.
4. Log in with `admin12` / `admin@1234`.

## Directory Structure
- `/vulnerable/` – vulnerable modules
- `/secure/` – secure versions of the same modules
- `/admin/` – admin panel
- `/assets/` – CSS & JS
- `/db/` – SQLite database (created automatically)

## License
For educational use only.
""",

    "config.php": """<?php
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
""",

    "init_db.php": """<?php
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
""",

    "index.php": """<?php header("Location: login.php"); exit; ?>
""",

    "login.php": """<?php
require_once 'config.php';
if (isLoggedIn()) redirect('dashboard.php');
$error = '';
$mode = $_GET['mode'] ?? 'vulnerable';
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $username = $_POST['username'] ?? '';
    $password = $_POST['password'] ?? '';
    $mode = $_POST['mode'] ?? 'vulnerable';
    if ($mode === 'secure') {
        $stmt = $pdo->prepare("SELECT * FROM users WHERE username = ?");
        $stmt->execute([$username]);
        $user = $stmt->fetch(PDO::FETCH_ASSOC);
        if ($user && password_verify($password, $user['password'])) {
            $_SESSION['user_id'] = $user['id'];
            $_SESSION['username'] = $user['username'];
            redirect('dashboard.php');
        } else {
            $error = 'Invalid credentials.';
        }
    } else {
        // VULNERABLE: SQL injection possible
        $query = "SELECT * FROM users WHERE username = '$username' AND password = '$password'";
        $result = $pdo->query($query);
        $user = $result->fetch(PDO::FETCH_ASSOC);
        if ($user) {
            $_SESSION['user_id'] = $user['id'];
            $_SESSION['username'] = $user['username'];
            redirect('dashboard.php');
        } else {
            $error = 'Invalid credentials.';
        }
    }
}
?>
<!DOCTYPE html>
<html>
<head>
    <title>Login - Vulnerable Lab</title>
    <link rel="stylesheet" href="assets/css/style.css">
</head>
<body>
    <div class="login-container">
        <h1>🔐 Security Training Lab</h1>
        <div class="mode-switch">
            <a href="?mode=vulnerable" class="<?= $mode=='vulnerable'?'active':'' ?>">Vulnerable</a>
            <a href="?mode=secure" class="<?= $mode=='secure'?'active':'' ?>">Secure</a>
        </div>
        <form method="POST">
            <input type="hidden" name="mode" value="<?= htmlspecialchars($mode) ?>">
            <div class="form-group">
                <label>Username</label>
                <input type="text" name="username" value="admin12">
            </div>
            <div class="form-group">
                <label>Password</label>
                <input type="password" name="password" value="admin@1234">
            </div>
            <button type="submit">Login</button>
            <div class="error"><?= $error ?></div>
        </form>
        <div class="info">
            <?php if ($mode === 'vulnerable'): ?>
                <p><strong>Vulnerable Mode:</strong> Try <code>' OR '1'='1</code> as password or username.</p>
            <?php else: ?>
                <p><strong>Secure Mode:</strong> Uses prepared statements – no SQL injection.</p>
            <?php endif; ?>
        </div>
    </div>
</body>
</html>
""",

    "logout.php": """<?php
session_start();
session_destroy();
header("Location: login.php");
exit;
?>
""",

    "dashboard.php": """<?php
require_once 'config.php';
if (!isLoggedIn()) redirect('login.php');
$user_id = $_SESSION['user_id'];
$username = $_SESSION['username'];
?>
<!DOCTYPE html>
<html>
<head>
    <title>Dashboard</title>
    <link rel="stylesheet" href="assets/css/style.css">
</head>
<body>
    <div class="sidebar">
        <h2>🔒 Lab</h2>
        <ul>
            <li><a href="dashboard.php">Dashboard</a></li>
            <li><a href="profile.php">Profile</a></li>
            <li><a href="reports.php">Reports</a></li>
            <li><a href="vulnerable/">Vulnerable Modules</a></li>
            <li><a href="secure/">Secure Modules</a></li>
            <li><a href="admin/users.php">Admin</a></li>
            <li><a href="logout.php">Logout</a></li>
        </ul>
    </div>
    <div class="main-content">
        <h1>Welcome, <?= htmlspecialchars($username) ?></h1>
        <div class="stats">
            <div class="card">Users: 5</div>
            <div class="card">Files: 12</div>
            <div class="card">Comments: 8</div>
        </div>
        <div class="learning-mode">
            <h3>📘 Learning Mode</h3>
            <p>Click on any vulnerable module to see the weakness and how to exploit/fix it.</p>
        </div>
        <h2>Recent Activity</h2>
        <table>
            <tr><th>User</th><th>Action</th><th>Time</th></tr>
            <?php
            $logs = $pdo->query("SELECT * FROM logs ORDER BY timestamp DESC LIMIT 5");
            while($row = $logs->fetch(PDO::FETCH_ASSOC)) {
                echo "<tr><td>{$row['user_id']}</td><td>{$row['action']}</td><td>{$row['timestamp']}</td></tr>";
            }
            ?>
        </table>
    </div>
</body>
</html>
""",

    "profile.php": """<?php
require_once 'config.php';
if (!isLoggedIn()) redirect('login.php');
$user_id = $_GET['id'] ?? $_SESSION['user_id'];
$stmt = $pdo->prepare("SELECT * FROM users WHERE id = ?");
$stmt->execute([$user_id]);
$user = $stmt->fetch(PDO::FETCH_ASSOC);
?>
<!DOCTYPE html>
<html>
<head>
    <title>Profile</title>
    <link rel="stylesheet" href="assets/css/style.css">
</head>
<body>
    <div class="sidebar">... (sidebar same as dashboard) ...</div>
    <div class="main-content">
        <h1>Profile</h1>
        <p><strong>ID:</strong> <?= $user['id'] ?></p>
        <p><strong>Username:</strong> <?= htmlspecialchars($user['username']) ?></p>
        <p><strong>Full Name:</strong> <?= htmlspecialchars($user['fullname']) ?></p>
        <p><strong>Role:</strong> <?= htmlspecialchars($user['role']) ?></p>
        <p><em>Try changing the <code>id</code> parameter in the URL to view other users (IDOR).</em></p>
    </div>
</body>
</html>
""",

    "reports.php": """<?php
require_once 'config.php';
if (!isLoggedIn()) redirect('login.php');
?>
<!DOCTYPE html>
<html>
<head><title>Reports</title><link rel="stylesheet" href="assets/css/style.css"></head>
<body>
    <div class="sidebar">... (sidebar) ...</div>
    <div class="main-content">
        <h1>Reports</h1>
        <p>Placeholder for reports – you can extend this page.</p>
    </div>
</body>
</html>
""",

    # ========== ASSETS ==========
    "assets/css/style.css": """/* Dark theme, glassmorphism, responsive */
* { margin:0; padding:0; box-sizing:border-box; }
body { font-family: 'Inter', sans-serif; background: #0a0a0a; color: #e0e0e0; display:flex; justify-content:center; align-items:center; min-height:100vh; }
.login-container { background: rgba(20,20,20,0.8); backdrop-filter:blur(10px); border-radius:20px; padding:2rem; width:100%; max-width:400px; box-shadow:0 8px 32px rgba(0,0,0,0.5); border:1px solid rgba(255,255,255,0.05); }
.login-container h1 { text-align:center; margin-bottom:1.5rem; }
.mode-switch { display:flex; justify-content:center; gap:1rem; margin-bottom:1.5rem; }
.mode-switch a { padding:0.5rem 1rem; border-radius:30px; text-decoration:none; background:#2a2a2a; color:#aaa; transition:0.3s; }
.mode-switch a.active { background:#4a6cf7; color:#fff; }
.form-group { margin-bottom:1rem; }
.form-group label { display:block; margin-bottom:0.3rem; font-size:0.9rem; }
.form-group input { width:100%; padding:0.7rem; border-radius:8px; border:1px solid #333; background:#1a1a1a; color:#fff; }
button { width:100%; padding:0.8rem; border:none; border-radius:8px; background:#4a6cf7; color:#fff; font-weight:bold; cursor:pointer; transition:0.3s; }
button:hover { background:#3651d4; }
.error { color:#ff4d4d; margin-top:0.5rem; text-align:center; }
.info { margin-top:1.5rem; font-size:0.9rem; background:#1a1a1a; padding:0.8rem; border-radius:8px; }
.info code { background:#2a2a2a; padding:0.2rem 0.5rem; border-radius:4px; }
.sidebar { position:fixed; top:0; left:0; width:220px; height:100%; background:#141414; padding:1.5rem; border-right:1px solid #2a2a2a; }
.sidebar h2 { margin-bottom:2rem; }
.sidebar ul { list-style:none; }
.sidebar ul li { margin-bottom:0.8rem; }
.sidebar ul li a { color:#ccc; text-decoration:none; transition:0.3s; display:block; padding:0.4rem; border-radius:6px; }
.sidebar ul li a:hover { background:#2a2a2a; color:#fff; }
.main-content { margin-left:240px; padding:2rem; width:calc(100% - 240px); }
.stats { display:flex; gap:1.5rem; flex-wrap:wrap; margin:1.5rem 0; }
.card { background:#1a1a1a; padding:1rem 2rem; border-radius:12px; border:1px solid #2a2a2a; flex:1; min-width:120px; }
table { width:100%; border-collapse:collapse; margin-top:1rem; }
th, td { padding:0.8rem; border-bottom:1px solid #2a2a2a; text-align:left; }
@media (max-width:768px) { .sidebar { width:100%; height:auto; position:relative; } .main-content { margin-left:0; width:100%; } }
""",

    "assets/js/main.js": """// UI helpers, toggle mode, etc.
console.log('Vulnerable Lab loaded.');
// You can add more interactivity here if needed.
""",

    # ========== VULNERABLE MODULES ==========
    "vulnerable/login.php": """<?php
// Vulnerable login – SQL injection possible
session_start();
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $username = $_POST['username'];
    $password = $_POST['password'];
    $db = new SQLite3('../db/lab.db');
    $query = "SELECT * FROM users WHERE username = '$username' AND password = '$password'";
    $result = $db->query($query);
    if ($row = $result->fetchArray()) {
        $_SESSION['user_id'] = $row['id'];
        $_SESSION['username'] = $row['username'];
        header("Location: ../dashboard.php");
        exit;
    } else {
        $error = "Invalid login!";
    }
}
?>
<!DOCTYPE html>
<html>
<head><title>Vulnerable Login</title><link rel="stylesheet" href="../assets/css/style.css"></head>
<body>
<div class="login-container">
    <h2>Vulnerable Login (SQLi)</h2>
    <form method="POST">
        <div class="form-group"><label>Username</label><input type="text" name="username"></div>
        <div class="form-group"><label>Password</label><input type="password" name="password"></div>
        <button type="submit">Login</button>
        <div class="error"><?= $error ?? '' ?></div>
    </form>
    <div class="info">
        <h4>Learning Mode</h4>
        <p><strong>OWASP:</strong> A03:2021 – Injection</p>
        <p><strong>Risk:</strong> High</p>
        <p><strong>How it works:</strong> The app concatenates user input directly into the SQL query.</p>
        <p><strong>Exploit:</strong> Enter <code>' OR '1'='1</code> as password.</p>
        <p><strong>Fix:</strong> Use prepared statements (see <a href=\"../secure/login.php\">secure version</a>).</p>
    </div>
</div>
</body>
</html>
""",

    "vulnerable/search.php": """<?php
session_start();
if (!isset($_SESSION['user_id'])) die("Unauthorized");
$db = new SQLite3('../db/lab.db');
$search = $_GET['q'] ?? '';
$query = "SELECT * FROM users WHERE username LIKE '%$search%'";
$result = $db->query($query);
?>
<!DOCTYPE html>
<html>
<head><title>Vulnerable Search</title><link rel="stylesheet" href="../assets/css/style.css"></head>
<body>
<div class="main-content" style="margin:2rem;">
    <h1>Search Users</h1>
    <form><input type="text" name="q" value="<?= htmlspecialchars($search) ?>"><button>Search</button></form>
    <table>
        <tr><th>ID</th><th>Username</th></tr>
        <?php while($row = $result->fetchArray()): ?>
        <tr><td><?= $row['id'] ?></td><td><?= $row['username'] ?></td></tr>
        <?php endwhile; ?>
    </table>
    <div class="info">
        <h4>Learning Mode</h4>
        <p><strong>OWASP:</strong> A03:2021 – Injection</p>
        <p><strong>Risk:</strong> High</p>
        <p><strong>Exploit:</strong> Use <code>' UNION SELECT null, username, password FROM users --</code> in the search box.</p>
        <p><strong>Fix:</strong> Use prepared statements.</p>
    </div>
</div>
</body>
</html>
""",

    "vulnerable/upload.php": """<?php
session_start();
if (!isset($_SESSION['user_id'])) die("Unauthorized");
$msg = '';
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $target = 'uploads/' . $_FILES['file']['name'];
    move_uploaded_file($_FILES['file']['tmp_name'], $target);
    $msg = "File uploaded!";
}
?>
<!DOCTYPE html>
<html>
<head><title>Vulnerable Upload</title><link rel="stylesheet" href="../assets/css/style.css"></head>
<body>
<div class="main-content" style="margin:2rem;">
    <h1>Unsafe File Upload</h1>
    <form method="POST" enctype="multipart/form-data">
        <input type="file" name="file"><br><br>
        <button>Upload</button>
    </form>
    <p><?= $msg ?></p>
    <div class="info">
        <h4>Learning Mode</h4>
        <p><strong>OWASP:</strong> A05:2021 – Security Misconfiguration</p>
        <p><strong>Risk:</strong> High</p>
        <p><strong>Exploit:</strong> Upload a PHP shell (e.g., <code>shell.php</code>) and access it.</p>
        <p><strong>Fix:</strong> Validate file type, rename, restrict execution.</p>
    </div>
</div>
</body>
</html>
""",

    "vulnerable/xss.php": """<?php
$name = $_GET['name'] ?? 'Guest';
?>
<!DOCTYPE html>
<html>
<head><title>Reflected XSS</title><link rel="stylesheet" href="../assets/css/style.css"></head>
<body>
<div class="main-content" style="margin:2rem;">
    <h1>Hello, <?= $name ?></h1>
    <p>This page is vulnerable to Reflected XSS.</p>
    <p>Try: <code>?name=<script>alert('XSS')</script></code></p>
    <div class="info">
        <h4>Learning Mode</h4>
        <p><strong>OWASP:</strong> A03:2021 – Injection</p>
        <p><strong>Risk:</strong> Medium</p>
        <p><strong>Exploit:</strong> Inject a script in the <code>name</code> parameter.</p>
        <p><strong>Fix:</strong> Use <code>htmlspecialchars()</code> (see secure version).</p>
    </div>
</div>
</body>
</html>
""",

    "vulnerable/xss_stored.php": """<?php
session_start();
require_once '../config.php';
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['comment'])) {
    $comment = $_POST['comment'];
    $pdo->exec("INSERT INTO comments (user_id, comment) VALUES ({$_SESSION['user_id']}, '$comment')");
}
$comments = $pdo->query("SELECT * FROM comments ORDER BY id DESC")->fetchAll(PDO::FETCH_ASSOC);
?>
<!DOCTYPE html>
<html>
<head><title>Stored XSS</title><link rel="stylesheet" href="../assets/css/style.css"></head>
<body>
<div class="main-content" style="margin:2rem;">
    <h1>Comment Section (Stored XSS)</h1>
    <form method="POST">
        <textarea name="comment" placeholder="Your comment"></textarea><br>
        <button>Post</button>
    </form>
    <h2>Comments</h2>
    <?php foreach($comments as $c): ?>
        <div style="border-bottom:1px solid #333; padding:0.5rem;">
            <?= $c['comment'] ?>
        </div>
    <?php endforeach; ?>
    <div class="info">
        <h4>Learning Mode</h4>
        <p><strong>OWASP:</strong> A03:2021 – Injection</p>
        <p><strong>Risk:</strong> High</p>
        <p><strong>Exploit:</strong> Post <code><script>alert('stored')</script></code>.</p>
        <p><strong>Fix:</strong> Escape output with <code>htmlspecialchars()</code>.</p>
    </div>
</div>
</body>
</html>
""",

    "vulnerable/dom_xss.php": """<!DOCTYPE html>
<html>
<head><title>DOM XSS</title><link rel="stylesheet" href="../assets/css/style.css"></head>
<body>
<div class="main-content" style="margin:2rem;">
    <h1>DOM XSS Example</h1>
    <p>Your name: <span id="nameDisplay"></span></p>
    <script>
        // Vulnerable: uses innerHTML with unsanitized input
        var name = new URLSearchParams(window.location.search).get('name') || 'Guest';
        document.getElementById('nameDisplay').innerHTML = name;
    </script>
    <div class="info">
        <h4>Learning Mode</h4>
        <p><strong>OWASP:</strong> A03:2021 – Injection</p>
        <p><strong>Risk:</strong> Medium</p>
        <p><strong>Exploit:</strong> Use <code>?name=<img src=x onerror=alert(1)></code></p>
        <p><strong>Fix:</strong> Use <code>textContent</code> instead of <code>innerHTML</code>.</p>
    </div>
</div>
</body>
</html>
""",

    "vulnerable/idor.php": """<?php
session_start();
$user_id = $_GET['id'] ?? 1;
$db = new SQLite3('../db/lab.db');
$query = "SELECT * FROM users WHERE id = $user_id";
$result = $db->query($query);
$profile = $result->fetchArray();
?>
<!DOCTYPE html>
<html>
<head><title>IDOR Example</title><link rel="stylesheet" href="../assets/css/style.css"></head>
<body>
<div class="main-content" style="margin:2rem;">
    <h1>User Profile</h1>
    <p><strong>ID:</strong> <?= $profile['id'] ?></p>
    <p><strong>Username:</strong> <?= $profile['username'] ?></p>
    <p><strong>Full Name:</strong> <?= $profile['fullname'] ?></p>
    <p><strong>Role:</strong> <?= $profile['role'] ?></p>
    <div class="info">
        <h4>Learning Mode</h4>
        <p><strong>OWASP:</strong> A01:2021 – Broken Access Control</p>
        <p><strong>Risk:</strong> High</p>
        <p><strong>Exploit:</strong> Change the <code>id</code> parameter to view other users.</p>
        <p><strong>Fix:</strong> Check if the logged-in user is authorized to view that profile.</p>
    </div>
</div>
</body>
</html>
""",

    "vulnerable/dir_traversal.php": """<?php
$file = $_GET['file'] ?? 'readme.txt';
$content = file_get_contents($file);
?>
<!DOCTYPE html>
<html>
<head><title>Directory Traversal</title><link rel="stylesheet" href="../assets/css/style.css"></head>
<body>
<div class="main-content" style="margin:2rem;">
    <h1>File Viewer</h1>
    <pre><?= $content ?></pre>
    <div class="info">
        <h4>Learning Mode</h4>
        <p><strong>OWASP:</strong> A01:2021 – Broken Access Control</p>
        <p><strong>Risk:</strong> Medium</p>
        <p><strong>Exploit:</strong> Use <code>?file=../../config.php</code> to read sensitive files.</p>
        <p><strong>Fix:</strong> Use <code>basename()</code> and restrict to a specific directory.</p>
    </div>
</div>
</body>
</html>
""",

    "vulnerable/csrf.php": """<?php
session_start();
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['new_password'])) {
    // Change password without token
    $db = new SQLite3('../db/lab.db');
    $new = $_POST['new_password'];
    $db->exec("UPDATE users SET password = '$new' WHERE id = {$_SESSION['user_id']}");
    echo "<p>Password changed!</p>";
}
?>
<!DOCTYPE html>
<html>
<head><title>CSRF Vulnerable</title><link rel="stylesheet" href="../assets/css/style.css"></head>
<body>
<div class="main-content" style="margin:2rem;">
    <h1>Change Password (CSRF vulnerable)</h1>
    <form method="POST">
        <input type="password" name="new_password" placeholder="New password">
        <button>Change</button>
    </form>
    <div class="info">
        <h4>Learning Mode</h4>
        <p><strong>OWASP:</strong> A01:2021 – Broken Access Control</p>
        <p><strong>Risk:</strong> Medium</p>
        <p><strong>Exploit:</strong> An attacker can make a user submit this form unknowingly.</p>
        <p><strong>Fix:</strong> Add a CSRF token.</p>
    </div>
</div>
</body>
</html>
""",

    # ========== SECURE VERSIONS ==========
    "secure/login.php": """<?php
// Secure login using prepared statements
require_once '../config.php';
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $username = $_POST['username'];
    $password = $_POST['password'];
    $stmt = $pdo->prepare("SELECT * FROM users WHERE username = ?");
    $stmt->execute([$username]);
    $user = $stmt->fetch(PDO::FETCH_ASSOC);
    if ($user && password_verify($password, $user['password'])) {
        $_SESSION['user_id'] = $user['id'];
        $_SESSION['username'] = $user['username'];
        header("Location: ../dashboard.php");
        exit;
    } else {
        $error = "Invalid credentials.";
    }
}
?>
<!DOCTYPE html>
<html>
<head><title>Secure Login</title><link rel="stylesheet" href="../assets/css/style.css"></head>
<body>
<div class="login-container">
    <h2>Secure Login (Prepared Statements)</h2>
    <form method="POST">
        <div class="form-group"><label>Username</label><input type="text" name="username"></div>
        <div class="form-group"><label>Password</label><input type="password" name="password"></div>
        <button type="submit">Login</button>
        <div class="error"><?= $error ?? '' ?></div>
    </form>
    <div class="info"><p>This version is not vulnerable to SQL injection.</p></div>
</div>
</body>
</html>
""",

    "secure/search.php": """<?php
// Secure search using prepared statements
require_once '../config.php';
session_start();
if (!isset($_SESSION['user_id'])) die("Unauthorized");
$search = $_GET['q'] ?? '';
$stmt = $pdo->prepare("SELECT * FROM users WHERE username LIKE ?");
$stmt->execute(["%$search%"]);
$results = $stmt->fetchAll(PDO::FETCH_ASSOC);
?>
<!DOCTYPE html>
<html>
<head><title>Secure Search</title><link rel="stylesheet" href="../assets/css/style.css"></head>
<body>
<div class="main-content" style="margin:2rem;">
    <h1>Search Users (Secure)</h1>
    <form><input type="text" name="q" value="<?= htmlspecialchars($search) ?>"><button>Search</button></form>
    <table>
        <tr><th>ID</th><th>Username</th></tr>
        <?php foreach($results as $row): ?>
        <tr><td><?= $row['id'] ?></td><td><?= htmlspecialchars($row['username']) ?></td></tr>
        <?php endforeach; ?>
    </table>
</div>
</body>
</html>
""",

    "secure/upload.php": """<?php
// Secure upload with validation
session_start();
if (!isset($_SESSION['user_id'])) die("Unauthorized");
$msg = '';
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $allowed = ['image/jpeg', 'image/png', 'application/pdf'];
    $file = $_FILES['file'];
    if (in_array($file['type'], $allowed) && $file['size'] < 1024*1024) {
        $name = basename($file['name']);
        move_uploaded_file($file['tmp_name'], 'uploads/' . $name);
        $msg = "File uploaded successfully.";
    } else {
        $msg = "Invalid file type or size.";
    }
}
?>
<!DOCTYPE html>
<html>
<head><title>Secure Upload</title><link rel="stylesheet" href="../assets/css/style.css"></head>
<body>
<div class="main-content" style="margin:2rem;">
    <h1>Secure File Upload</h1>
    <form method="POST" enctype="multipart/form-data">
        <input type="file" name="file"><br><br>
        <button>Upload</button>
    </form>
    <p><?= $msg ?></p>
</div>
</body>
</html>
""",

    "secure/xss.php": """<?php
$name = $_GET['name'] ?? 'Guest';
?>
<!DOCTYPE html>
<html>
<head><title>Secure XSS</title><link rel="stylesheet" href="../assets/css/style.css"></head>
<body>
<div class="main-content" style="margin:2rem;">
    <h1>Hello, <?= htmlspecialchars($name) ?></h1>
    <p>This page is safe from XSS.</p>
</div>
</body>
</html>
""",

    "secure/xss_stored.php": """<?php
// Secure stored XSS with escaping
require_once '../config.php';
session_start();
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['comment'])) {
    $comment = htmlspecialchars($_POST['comment']);
    $stmt = $pdo->prepare("INSERT INTO comments (user_id, comment) VALUES (?, ?)");
    $stmt->execute([$_SESSION['user_id'], $comment]);
}
$comments = $pdo->query("SELECT * FROM comments ORDER BY id DESC")->fetchAll(PDO::FETCH_ASSOC);
?>
<!DOCTYPE html>
<html>
<head><title>Secure Stored XSS</title><link rel="stylesheet" href="../assets/css/style.css"></head>
<body>
<div class="main-content" style="margin:2rem;">
    <h1>Comment Section (Secure)</h1>
    <form method="POST">
        <textarea name="comment" placeholder="Your comment"></textarea><br>
        <button>Post</button>
    </form>
    <h2>Comments</h2>
    <?php foreach($comments as $c): ?>
        <div style="border-bottom:1px solid #333; padding:0.5rem;">
            <?= htmlspecialchars($c['comment']) ?>
        </div>
    <?php endforeach; ?>
</div>
</body>
</html>
""",

    "secure/dom_xss.php": """<!DOCTYPE html>
<html>
<head><title>Secure DOM XSS</title><link rel="stylesheet" href="../assets/css/style.css"></head>
<body>
<div class="main-content" style="margin:2rem;">
    <h1>DOM XSS (Secure)</h1>
    <p>Your name: <span id="nameDisplay"></span></p>
    <script>
        var name = new URLSearchParams(window.location.search).get('name') || 'Guest';
        document.getElementById('nameDisplay').textContent = name; // safe
    </script>
</div>
</body>
</html>
""",

    "secure/idor.php": """<?php
// Secure IDOR with access control
require_once '../config.php';
session_start();
if (!isset($_SESSION['user_id'])) die("Unauthorized");
$user_id = $_GET['id'] ?? $_SESSION['user_id'];
// Only allow viewing own profile or admin
if ($user_id != $_SESSION['user_id'] && $_SESSION['role'] != 'admin') {
    die("Access denied.");
}
$stmt = $pdo->prepare("SELECT * FROM users WHERE id = ?");
$stmt->execute([$user_id]);
$profile = $stmt->fetch(PDO::FETCH_ASSOC);
?>
<!DOCTYPE html>
<html>
<head><title>Secure IDOR</title><link rel="stylesheet" href="../assets/css/style.css"></head>
<body>
<div class="main-content" style="margin:2rem;">
    <h1>User Profile</h1>
    <p><strong>ID:</strong> <?= $profile['id'] ?></p>
    <p><strong>Username:</strong> <?= htmlspecialchars($profile['username']) ?></p>
    <p><strong>Full Name:</strong> <?= htmlspecialchars($profile['fullname']) ?></p>
</div>
</body>
</html>
""",

    "secure/dir_traversal.php": """<?php
$file = $_GET['file'] ?? 'readme.txt';
$base = __DIR__ . '/../uploads/';
$file = basename($file); // strip path
$path = $base . $file;
if (file_exists($path)) {
    $content = file_get_contents($path);
} else {
    $content = "File not found.";
}
?>
<!DOCTYPE html>
<html>
<head><title>Secure File Viewer</title><link rel="stylesheet" href="../assets/css/style.css"></head>
<body>
<div class="main-content" style="margin:2rem;">
    <h1>File Viewer (Secure)</h1>
    <pre><?= htmlspecialchars($content) ?></pre>
</div>
</body>
</html>
""",

    "secure/csrf.php": """<?php
// Secure CSRF with token
session_start();
if (empty($_SESSION['csrf_token'])) {
    $_SESSION['csrf_token'] = bin2hex(random_bytes(32));
}
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if (!isset($_POST['csrf_token']) || $_POST['csrf_token'] !== $_SESSION['csrf_token']) {
        die("CSRF token validation failed.");
    }
    // Change password...
    echo "Password changed securely.";
}
?>
<!DOCTYPE html>
<html>
<head><title>Secure CSRF</title><link rel="stylesheet" href="../assets/css/style.css"></head>
<body>
<div class="main-content" style="margin:2rem;">
    <h1>Change Password (CSRF protected)</h1>
    <form method="POST">
        <input type="hidden" name="csrf_token" value="<?= $_SESSION['csrf_token'] ?>">
        <input type="password" name="new_password" placeholder="New password">
        <button>Change</button>
    </form>
</div>
</body>
</html>
""",

    # ========== ADMIN PANEL ==========
    "admin/users.php": """<?php
require_once '../config.php';
if (!isLoggedIn() || $_SESSION['role'] != 'admin') die("Access denied.");
$users = $pdo->query("SELECT * FROM users")->fetchAll(PDO::FETCH_ASSOC);
?>
<!DOCTYPE html>
<html>
<head><title>Manage Users</title><link rel="stylesheet" href="../assets/css/style.css"></head>
<body>
<div class="sidebar">... (sidebar) ...</div>
<div class="main-content">
    <h1>User Management</h1>
    <table>
        <tr><th>ID</th><th>Username</th><th>Full Name</th><th>Role</th></tr>
        <?php foreach($users as $u): ?>
        <tr><td><?= $u['id'] ?></td><td><?= htmlspecialchars($u['username']) ?></td><td><?= htmlspecialchars($u['fullname']) ?></td><td><?= htmlspecialchars($u['role']) ?></td></tr>
        <?php endforeach; ?>
    </table>
</div>
</body>
</html>
""",

    "admin/logs.php": """<?php
require_once '../config.php';
if (!isLoggedIn() || $_SESSION['role'] != 'admin') die("Access denied.");
$logs = $pdo->query("SELECT * FROM logs ORDER BY timestamp DESC")->fetchAll(PDO::FETCH_ASSOC);
?>
<!DOCTYPE html>
<html>
<head><title>Activity Logs</title><link rel="stylesheet" href="../assets/css/style.css"></head>
<body>
<div class="sidebar">... (sidebar) ...</div>
<div class="main-content">
    <h1>Activity Logs</h1>
    <table>
        <tr><th>User ID</th><th>Action</th><th>IP</th><th>Timestamp</th></tr>
        <?php foreach($logs as $l): ?>
        <tr><td><?= $l['user_id'] ?></td><td><?= htmlspecialchars($l['action']) ?></td><td><?= $l['ip'] ?></td><td><?= $l['timestamp'] ?></td></tr>
        <?php endforeach; ?>
    </table>
</div>
</body>
</html>
""",

    "admin/files.php": """<?php
require_once '../config.php';
if (!isLoggedIn() || $_SESSION['role'] != 'admin') die("Access denied.");
$files = $pdo->query("SELECT * FROM files ORDER BY uploaded_at DESC")->fetchAll(PDO::FETCH_ASSOC);
?>
<!DOCTYPE html>
<html>
<head><title>Uploaded Files</title><link rel="stylesheet" href="../assets/css/style.css"></head>
<body>
<div class="sidebar">... (sidebar) ...</div>
<div class="main-content">
    <h1>Uploaded Files</h1>
    <table>
        <tr><th>Filename</th><th>Uploader ID</th><th>Date</th></tr>
        <?php foreach($files as $f): ?>
        <tr><td><?= htmlspecialchars($f['filename']) ?></td><td><?= $f['uploader_id'] ?></td><td><?= $f['uploaded_at'] ?></td></tr>
        <?php endforeach; ?>
    </table>
</div>
</body>
</html>
""",
}

# ----------------------------------------------------------------------
#  Write all files to disk
# ----------------------------------------------------------------------
def create_project():
    for path, content in files.items():
        dirname = os.path.dirname(path)
        if dirname:
            os.makedirs(dirname, exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
    print("✅ All files created.")

# ----------------------------------------------------------------------
#  Create the ZIP archive
# ----------------------------------------------------------------------
def zip_project():
    zip_name = "vulnerable-lab.zip"
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, filenames in os.walk('.'):
            for fname in filenames:
                if fname == zip_name or fname == os.path.basename(__file__):
                    continue
                file_path = os.path.join(root, fname)
                arcname = os.path.relpath(file_path, '.')
                zipf.write(file_path, arcname)
    print(f"✅ ZIP created: {zip_name}")

# ----------------------------------------------------------------------
#  Main
# ----------------------------------------------------------------------
if __name__ == "__main__":
    create_project()
    zip_project()
    print("🎉 Done! You can now extract and run the lab.")