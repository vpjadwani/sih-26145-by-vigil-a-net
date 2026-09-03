<?php
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
