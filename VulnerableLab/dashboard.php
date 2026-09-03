<?php
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
