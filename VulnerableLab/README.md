# Vulnerable Web Application Training Lab

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
