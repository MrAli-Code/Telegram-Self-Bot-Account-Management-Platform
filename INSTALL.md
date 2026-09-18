# Telegram Self-Bot - Installation Guide

This guide covers everything you need to get the **Telegram Self-Bot / Account Management Platform** up and running on your machine or server.

The platform is a professional, modular, production-ready Telegram client and account management system. It includes a web dashboard, REST API, automation engine, AI integrations, and a full plugin system.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Getting Telegram API Credentials](#getting-telegram-api-credentials)
3. [Installation Methods](#installation-methods)
   - [Linux / macOS](#linux--macos)
   - [Windows](#windows)
   - [Manual Installation (all platforms)](#manual-installation-all-platforms)
   - [Docker](#docker)
4. [Environment Configuration (.env)](#environment-configuration-env)
5. [Database Setup](#database-setup)
6. [Building the Frontend](#building-the-frontend)
7. [First Run and Admin Setup](#first-run-and-admin-setup)
8. [Connecting Your Telegram Account](#connecting-your-telegram-account)
9. [Running as a Production Service](#running-as-a-production-service)
10. [Common Installation Issues](#common-installation-issues)

---

## Prerequisites

Before you begin, make sure your system has the following installed:

| Requirement | Version/Notes |
|---|---|
| **Python** | 3.11 or newer (3.12/3.13 recommended) |
| **FFmpeg** | Latest stable (for media conversion, voice/audio processing) |
| **Redis** | 6.x or newer (for task queue, caching, Celery broker) |
| **Node.js** (optional) | 18+ if you want to build the frontend separately |
| **Git** | Latest (for cloning and version control) |
| **Docker** (optional) | For containerized deployment |

### Verify on Linux/macOS

```bash
python3 --version    # Python 3.11+
ffmpeg -version      # FFmpeg present
redis-server --version  # Redis present
```

### Verify on Windows (PowerShell)

```powershell
python --version
ffmpeg -version
redis-server --version
```

### Installing FFmpeg

**Ubuntu / Debian:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**CentOS / RHEL / Fedora:**
```bash
sudo dnf install ffmpeg
```

**macOS (Homebrew):**
```bash
brew install ffmpeg
```

**Windows:**
1. Download the latest FFmpeg build from https://ffmpeg.org/download.html
2. Extract the archive to `C:\ffmpeg`
3. Add `C:\ffmpeg\bin` to your system `PATH`:
   - Open **System Properties > Environment Variables**
   - Under *System variables*, select `Path` and click **Edit**
   - Click **New** and add `C:\ffmpeg\bin`
   - Click **OK** on all windows
4. Open a new terminal and run `ffmpeg -version` to confirm

### Installing Redis

**Ubuntu / Debian:**
```bash
sudo apt update
sudo apt install redis-server
sudo systemctl enable redis-server
sudo systemctl start redis-server
```

**macOS (Homebrew):**
```bash
brew install redis
brew services start redis
```

**Windows:**
1. Download the Redis Windows port from the official memurai/redis-windows releases (https://github.com/tporadowski/redis/releases) or install Memurai
2. Extract and run `redis-server.exe`
   > **Note:** For production on Windows, running the whole stack with **Docker** is strongly recommended.

> **No Redis?** The core dashboard works without Redis, but scheduled tasks, broadcasts, the repeater, and background worker processing will not function. For full functionality Redis is required.

---

## Getting Telegram API Credentials

The platform uses Telegram's **MTProto** protocol, so you need an **API ID** and **API Hash**:

1. Sign in to **https://my.telegram.org** with your Telegram account
2. Click **API development tools**
3. Fill in the form:
   - **App title:** e.g. `SelfBot Manager`
   - **Short name:** e.g. `selfbot_mgr`
   - **Platform:** `Desktop`
   - **Description:** anything
4. Click **Create application**
5. Copy the **api_id** (a number) and **api_hash** (a 32-character string)

> ⚠️ **Security warning:** Treat your `api_hash` like a password. Never commit it to version control or share it with anyone. The `.env` file is excluded from git via `.gitignore`.

---

## Installation Methods

### Linux / macOS

The simplest way is the bundled installer script:

```bash
# 1. Clone or copy the project into place
git clone <repository-url> telegram-self-bot
cd telegram-self-bot

# 2. Make the installer executable and run it
chmod +x install.sh
./install.sh
```

The script will:
- Detect your Python interpreter
- Upgrade `pip`
- Install the project with dev, AI, and media extras: `pip install -e ".[dev,ai,media]"`
- Warn if FFmpeg is missing
- Create `.env` from `.env.example` (only if not present)
- Create the `storage/media`, `storage/backups`, and `storage/logs` directories
- Attempt to run database migrations and create the default admin

When it finishes, start the server:

```bash
python3 -m backend.app.main serve --reload
```

### Windows

#### Using the PowerShell installer

```powershell
# Run from the project root
.\install.ps1
```

> If you get an execution policy error, run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` first, or run the commands manually (see below).

#### Manual Windows installation (also works if the script fails)

```powershell
# From the project root
python -m pip install --upgrade pip
python -m pip install -e ".[dev,ai,media]"

# Create the .env file if it doesn't exist
if (-not (Test-Path ".env")) { Copy-Item ".env.example" ".env" }

# Create storage directories
New-Item -ItemType Directory -Path "storage\media" -Force
New-Item -ItemType Directory -Path "storage\backups" -Force
New-Item -ItemType Directory -Path "storage\logs" -Force

# Start the server
python -m backend.app.main serve --reload
```

### Manual Installation (all platforms)

If you prefer full control:

```bash
# 1. (Recommended) Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate        # Linux/macOS
# .venv\Scripts\activate         # Windows PowerShell

# 2. Upgrade pip and install the project with extras
python -m pip install --upgrade pip
python -m pip install -e ".[dev,ai,media]"

# 3. Configure .env
cp .env.example .env             # Linux/macOS
# Copy-Item ".env.example" ".env"  # Windows PowerShell

# 4. Prepare storage directories
mkdir -p storage/media storage/backups storage/logs

# 5. Run migrations (creates the database schema)
python -m backend.app.main migrate

# 6. Create the admin user (default: admin / admin123)
python -m backend.app.main init-admin

# 7. Start the server
python -m backend.app.main serve --reload
```

### Docker

Docker Compose runs the **app**, **Celery worker**, **Celery beat** scheduler, and **Redis** in isolated containers. This is the recommended production approach.

```bash
# 1. Create the .env file
cp .env.example .env

# 2. Edit .env with your Telegram API credentials and secrets (see next section)

# 3. Build and start all services
docker-compose up -d

# 4. Follow the logs
docker-compose logs -f app

# 5. Check the status of containers
docker-compose ps
```

The compose file defines these services:

| Service | Container | Purpose |
|---|---|---|
| `app` | `telegram-bot-app` | FastAPI + Uvicorn web server and dashboard, exposed on port `8000` |
| `worker` | `telegram-bot-worker` | Celery worker processing background jobs (`-c 2`) |
| `beat` | `telegram-bot-beat` | Celery beat — periodic task scheduler |
| `redis` | `telegram-bot-redis` | Redis 7 cache / broker on port `6379` |

The `app` service includes a healthcheck that calls `/health` every 30 seconds, and `redis` has a `redis-cli ping` healthcheck.

**Common Docker commands:**

```bash
# Run the initial admin creation (first time only)
docker-compose exec app python -m backend.app.main init-admin

# Run migrations inside the container
docker-compose exec app python -m backend.app.main migrate

# Stop everything
docker-compose down

# Wipe the database volume too (destructive!)
docker-compose down -v

# Rebuild after code changes
docker-compose up -d --build
```

> **Note:** The `storage` directory is bind-mounted to `./storage`, so media files and backups persist on the host.

---

## Environment Configuration (.env)

Copy `.env.example` to `.env` and fill in the values. The most important keys are the **Telegram credentials** and the **security secrets**.

### Critical values you MUST change

```env
# Telegram API — from https://my.telegram.org
TELEGRAM_API_ID=123456                # numeric
TELEGRAM_API_HASH=your_api_hash       # 32-character string

# Security secrets — generate random long strings
APP_SECRET_KEY=generate-a-random-64-char-string
JWT_SECRET_KEY=generate-a-random-64-char-string
ENCRYPTION_KEY=generate-a-random-64-char-string
CSRF_SECRET_KEY=generate-a-random-64-char-string
```

You can generate secure random values with:

```bash
# Linux/macOS
openssl rand -hex 32

# Windows PowerShell
-join ((48..57) + (97..102) | Get-Random -Count 64 | ForEach-Object { [char]$_ })
```

### Full reference table

| Variable | Default | Description |
|---|---|---|
| `APP_NAME` | `Telegram Self-Bot` | Display name |
| `APP_ENV` | `production` | `development` or `production` |
| `APP_DEBUG` | `false` | Enable debug mode |
| `APP_HOST` | `0.0.0.0` | Bind address |
| `APP_PORT` | `8000` | HTTP port |
| `APP_WORKERS` | `4` | Uvicorn worker count (prod) |
| `APP_LOG_LEVEL` | `INFO` | Log verbosity |
| `DATABASE_URL` | `sqlite:///./storage/database.db` | SQLite/PostgreSQL/MySQL DSN |
| `REDIS_URL` | `redis://localhost:6379/0` | Redis connection |
| `TELEGRAM_API_ID` | — | **Required** — from my.telegram.org |
| `TELEGRAM_API_HASH` | — | **Required** — from my.telegram.org |
| `TELEGRAM_SESSION_STRING` | empty | Optional pre-made session string |
| `TELEGRAM_PHONE` | empty | e.g. `+1234567890` |
| `JWT_SECRET_KEY` | placeholder | **Change it** — signs auth tokens |
| `ENCRYPTION_KEY` | placeholder | **Change it** — encrypts sessions/data at rest |
| `CSRF_SECRET_KEY` | placeholder | **Change it** — CSRF protection |
| `ALLOWED_ORIGINS` | localhost:3000,5173 | CORS allowed origins |
| `AI_PROVIDER` | `openai` | `openai`, `gemini`, `deepseek`, `local` |
| `OPENAI_API_KEY` | empty | OpenAI key (AI features) |
| `OPENAI_MODEL` | `gpt-3.5-turbo` | OpenAI model |
| `GEMINI_API_KEY` / `GEMINI_MODEL` | empty / `gemini-pro` | Google Gemini |
| `DEEPSEEK_API_KEY` / `DEEPSEEK_MODEL` | empty / `deepseek-chat` | DeepSeek |
| `OPENROUTER_API_KEY` | empty | OpenRouter aggregator |
| `LOCAL_LLM_URL` | empty | Local LLM (e.g. Ollama) endpoint |
| `MEDIA_STORAGE_PATH` | `storage/media` | Media archive location |
| `BACKUP_STORAGE_PATH` | `storage/backups` | Backup file location |
| `FFMPEG_PATH` | `ffmpeg` | FFmpeg binary path |
| `FFPROBE_PATH` | `ffprobe` | FFprobe binary path |
| `RATE_LIMIT_ENABLED` | `true` | Global API rate limiting |
| `CELERY_BROKER_URL` | `redis://localhost:6379/1` | Celery broker |
| `CELERY_RESULT_BACKEND` | `redis://localhost:6379/2` | Celery results |
| `SCHEDULER_ENABLED` / `SCHEDULER_TIMEZONE` | `true` / `UTC` | Scheduler and timezone |
| `BACKUP_ENCRYPTION_ENABLED` | `true` | Encrypt backups |
| `WEBSOCKET_ENABLED` / `WEBSOCKET_PATH` | `true` / `/ws` | Real-time updates |
| `HEALTH_CHECK_ENABLED` / `HEALTH_CHECK_PATH` | `true` / `/health` | Health endpoint |

> **Warning:** Never use the placeholder secret values in production. Anyone who knows the defaults could forge JWT tokens or decrypt data.

---

## Database Setup

### SQLite (default — quick start)

No setup required. SQLite works out of the box and stores everything in a single file (`storage/database.db`). Ideal for personal / single-user use.

### PostgreSQL (recommended for production)

1. Create a database and user:

```bash
sudo -u postgres psql
CREATE USER telegram_bot WITH PASSWORD 'a-strong-password';
CREATE DATABASE telegram_bot OWNER telegram_bot;
\q
```

2. Set the DSN in `.env`:

```env
DATABASE_URL=postgresql://telegram_bot:a-strong-password@localhost:5432/telegram_bot
```

3. The project already requires `asyncpg`, so no extra driver is needed.

### MySQL / MariaDB

```env
DATABASE_URL=mysql+pymysql://telegram_bot:a-strong-password@localhost:3306/telegram_bot
```

The `pymysql` driver is already a core dependency.

### Running migrations

After configuring the database, create/upgrade the schema:

```bash
python -m backend.app.main migrate
```

This runs Alembic migrations to `head`. You can also generate a new migration after model changes:

```bash
python -m backend.app.main makemigration -m "description of change"
```

> Migrations are **idempotent** — safe to run repeatedly.

---

## Building the Frontend

The project ships a pre-built Vue 3 frontend that is served automatically at `/` (the backend mounts `frontend/dist` if it exists). If `frontend/dist` does **not** exist, the API endpoints are still fully usable, but the dashboard won't render.

To build the frontend:

```bash
cd frontend
npm install
npm run build
cd ..
```

Then restart the server. The dashboard will be served at `http://localhost:8000`.

---

## First Run and Admin Setup

1. **Start the server:**
   ```bash
   python -m backend.app.main serve --reload
   ```

   You should see log output similar to:
   ```
   Uvicorn running on http://0.0.0.0:8000
   Application started successfully
   ```

2. **Create the admin user** (if the installer didn't do it automatically):
   ```bash
   python -m backend.app.main init-admin
   # -> "Admin user created (username: admin, password: admin123)"
   ```

3. **Log in to the dashboard** at `http://localhost:8000`:
   - **Username:** `admin`
   - **Password:** `admin123`

4. **Change the default password immediately.** Use the Settings page (or the user API) to set a strong password.

5. **Open the API documentation** at `http://localhost:8000/api/docs` (Swagger UI) and `http://localhost:8000/api/redoc`.

> ⚠️ **Security:** The default admin credentials (`admin` / `admin123`) are widely known. Never leave them in place on an internet-exposed deployment.

---

## Connecting Your Telegram Account

1. On the dashboard, go to **Settings**.
2. Enter your:
   - **API ID**
   - **API Hash**
   - **Phone number** (international format, e.g. `+1234567890`)
3. Click **Save & Connect**.
4. If a code is sent to your phone, enter it when prompted.
5. The connection status (bottom of the sidebar) should turn green (**Connected**).

You will only need to enter the code once — the session is stored (encrypted at rest) and reused next time.

> **Tip:** `TELEGRAM_SESSION_STRING` in `.env` lets you inject a pre-existing session string (e.g. produced by Telethon's `StringSession`) — useful when connecting accounts non-interactively.

---

## Running as a Production Service

### Option A: Docker (recommended)

See the [Docker section](#docker) — Compose gives you app + worker + beat + Redis with automatic restarts.

### Option B: systemd (Linux)

Create `/etc/systemd/system/telegram-bot.service`:

```ini
[Unit]
Description=Telegram Self-Bot
After=network.target redis-server.service

[Service]
User=telegram
WorkingDirectory=/opt/telegram-self-bot
ExecStart=/opt/telegram-self-bot/.venv/bin/python -m backend.app.main serve
Restart=always
RestartSec=5
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
```

Then:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now telegram-bot
sudo systemctl status telegram-bot
```

Create a similar unit for the Celery worker if you rely on background jobs:

```ini
[Unit]
Description=Telegram Self-Bot Worker
After=network.target redis-server.service

[Service]
User=telegram
WorkingDirectory=/opt/telegram-self-bot
ExecStart=/opt/telegram-self-bot/.venv/bin/celery -A worker.tasks.celery_app worker -l info -c 2
Restart=always

[Install]
WantedBy=multi-user.target
```

### Option C: Reverse proxy with Nginx + TLS

```nginx
server {
    listen 80;
    server_name bot.example.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name bot.example.com;

    ssl_certificate     /etc/letsencrypt/live/bot.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/bot.example.com/privkey.pem;

    client_max_body_size 100M;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /ws {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

---

## Common Installation Issues

### 1. `Python not found`
Install Python 3.11+ and ensure it is on your `PATH`. On Debian/Ubuntu you may need `sudo apt install python3 python3-pip python3-venv`.

### 2. `pip install` fails with compilation errors
Some wheels (e.g. `cryptography`) need build tools:
```bash
# Ubuntu/Debian
sudo apt install build-essential python3-dev libffi-dev

# Fedora
sudo dnf install gcc python3-devel libffi-devel
```

### 3. FFmpeg warning during install / converter errors
Install FFmpeg (see [Prerequisites](#prerequisites)). The platform still runs without it but **Media Converter** features are limited.

### 4. Redis connection refused
- Confirm Redis is running: `redis-cli ping` should return `PONG`.
- On Windows it must be running as a service or `redis-server.exe` process.
- With Docker, ensure Redis is not already using port 6379 on the host.

### 5. Port 8000 already in use
```bash
# Linux/macOS
sudo lsof -i :8000
# Windows
netstat -ano | findstr :8000
```
Change the port in `.env` (`APP_PORT=8001`) or stop the conflicting process.

### 6. Dashboard shows blank page / API works but no UI
The frontend hasn't been built. Run `cd frontend && npm install && npm run build` (see [Building the Frontend](#building-the-frontend)).

### 7. `ERROR: .env not found` or settings not applied
The config loader reads `.env` from the project root. Make sure you ran the server from the project root and that `.env` exists (copy from `.env.example`). Check that values are on their own lines and un-commented.

### 8. `ModuleNotFoundError: No module named 'backend'`
You started Python from a different directory, or the package isn't installed in editable mode. Run `pip install -e ".[dev,ai,media]"` from the project root, and start the server from the project root.

### 9. Database migration fails ("no such table" / alembic errors)
- Make sure `storage/` exists (the installer creates it).
- For a fresh install, don't mix an old SQLite file with new migrations — back up and remove `storage/database.db`, then re-run `python -m backend.app.main migrate`.

### 10. `Invalid auth scheme` or authentication fails
The API credentials were mistyped, or the account uses 2FA. Ensure API ID is numeric and API Hash is the exact 32-character value from my.telegram.org. If your account has two-step verification enabled, you may be prompted for a password during connection.

### 11. Docker build is slow
First builds download the Python base image and pip packages. Use `docker-compose build --no-cache` only when necessary; subsequent builds reuse the layer cache. Consider a mirror for pip if you have regional network issues.

### 12. Celery tasks never run
- Confirm Redis is reachable and `CELERY_BROKER_URL` matches.
- In Docker, confirm the `worker` and `beat` containers are up (`docker-compose ps`).
- Manually check a worker heartbeat: `celery -A worker.tasks.celery_app inspect ping`.

---

## Next Steps

- Read the **[User Guide](USER_GUIDE.md)** for a tour of every dashboard section.
- Read **[Troubleshooting](TROUBLESHOOTING.md)** when something misbehaves.
- See **[docs/FEATURES.md](docs/FEATURES.md)** for a complete feature reference.
- Open the interactive **API docs** at `http://localhost:8000/api/docs`.