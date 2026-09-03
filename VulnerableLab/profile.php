<?php
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
