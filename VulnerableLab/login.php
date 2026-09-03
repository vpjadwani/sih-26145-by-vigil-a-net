<?php
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
    } 
    else 
        {
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
