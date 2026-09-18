# Telegram Self-Bot — Troubleshooting Guide

When something goes wrong, work through this guide top to bottom. It covers common errors, connection problems, database issues, Telegram API limits, performance tuning, log analysis, and data recovery.

---

## Table of Contents

1. [Quick Diagnostic Checklist](#1-quick-diagnostic-checklist)
2. [Where the Logs Live](#2-where-the-logs-live)
3. [Common Errors and Solutions](#3-common-errors-and-solutions)
4. [Connection Issues](#4-connection-issues)
5. [Database Problems](#5-database-problems)
6. [Telegram API Limits (FloodWait)](#6-telegram-api-limits-floodwait)
7. [AI Provider Problems](#7-ai-provider-problems)
8. [Performance Optimization](#8-performance-optimization)
9. [Log Analysis](#9-log-analysis)
10. [Recovery Procedures](#10-recovery-procedures)

---

## 1. Quick Diagnostic Checklist

Run through these before anything else:

- [ ] Is the server running? → `curl http://localhost:8000/health`
- [ ] Is Redis up? → `redis-cli ping` (expect `PONG`)
- [ ] Is the dashboard reachable? → open `http://localhost:8000`
- [ ] Is the Telegram client **Connected**? → green dot at the bottom of the sidebar
- [ ] Is disk space available? → system health page / `df -h`
- [ ] Are secrets/keys set to real random values (not placeholders)?
- [ ] Was the frontend built? → check `frontend/dist` exists
- [ ] Any `ERROR` lines in the log? → `storage/logs/app.log`

> **Golden rule:** read the last 50 lines of the log first. 90% of issues print a clear error before anything "fails silently".

---

## 2. Where the Logs Live

| Source | Location |
|---|---|
| App log (file) | `storage/logs/app.log` (config: `APP_LOG_FILE`) |
| App log (dashboard) | **Logs** section in the UI |
| Celery worker | Console output / `docker-compose logs worker` |
| Celery beat | `docker-compose logs beat` |
| Uvicorn access log | Terminal / `docker-compose logs app` |

**Handy commands:**

```bash
# Tail the app log live (Linux/macOS)
tail -f storage/logs/app.log

# Search for errors
grep -i error storage/logs/app.log | tail -n 50

# Docker: all service logs
docker-compose logs --tail=100 -f
```

---

## 3. Common Errors and Solutions

### 3.1 `ConnectionRefusedError` for Redis

**Symptoms:** rate limiting, scheduler, broadcasts, and worker tasks stop working; logs mention `ConnectionRefusedError` or `redis.exceptions.ConnectionError`.

**Fix:**
```bash
redis-cli ping          # must return PONG
redis-cli -h <host> -p <port> ping   # for remote/container redis
```
- On Windows: start `redis-server.exe` or install Redis as a service.
- Check `REDIS_URL` in `.env` matches the running Redis (host/port/db).
- In Docker: ensure `redis` service is healthy (`docker-compose ps`).

### 3.2 `OperationalError: no such table: users` (or any table)

**Symptoms:** fresh install, tables missing.

**Fix:**
```bash
python -m backend.app.main migrate
```
If that fails, ensure the storage directory exists and re-run:
```bash
mkdir -p storage/media storage/backups storage/logs
python -m backend.app.main migrate
```

### 3.3 `ModuleNotFoundError: No module named 'backend'`

**Symptoms:** `python -m backend.app.main` fails from anywhere.

**Fix:**
```bash
# From the project root
python -m pip install -e ".[dev,ai,media]"
python -m backend.app.main serve
```
Always run from the project root.

### 3.4 `ValueError` / `SettingsValidationError` on startup

**Symptoms:** app won't boot; pydantic complains about a setting.

**Fix:**
- `.env` contains syntax errors (missing `=`, broken quoting).
- `TELEGRAM_API_ID` must be an **integer** (remove quotes).
- A custom `DATABASE_URL` driver isn't installed — fall back to SQLite for a quick check:
  ```env
  DATABASE_URL=sqlite+aiosqlite:///./storage/database.db
  ```

### 3.5 `401 Unauthorized` on every API call

**Symptoms:** dashboard works but custom API calls fail.

**Fix:**
- You forgot the `Authorization: Bearer <token>` header.
- Token expired — access tokens last **30 minutes** by default; use the `/api/auth/refresh` endpoint (refresh tokens last 7 days).
- `JWT_SECRET_KEY` changed after tokens were issued → re-login.

### 3.6 `403 Forbidden` / CORS errors from the browser

**Symptoms:** API works in curl but the browser blocks requests.

**Fix:**
- Ensure your dashboard origin is in `ALLOWED_ORIGINS` in `.env`:
  ```env
  ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
  ```
- If the frontend is served by the backend itself (from `frontend/dist`), the request is same-origin and this is rarely an issue.

### 3.7 `429` Too Many Requests (API rate limit)

**Symptom:** API calls start returning 429 after a burst.

**Fix:**
- Default: 30 requests / 60 s per IP (`RATE_LIMIT_REQUESTS`, `RATE_LIMIT_WINDOW`).
- Increase the limit or disable with `RATE_LIMIT_ENABLED=false` (not recommended in production).
- Slow down clients / add backoff in scripts.

### 3.8 Frontend shows blank / old content after deploy

**Fix:**
```bash
cd frontend && npm install && npm run build && cd ..
```
Clear the browser cache (Ctrl+Shift+R) — the backend serves the built `dist` folder.

### 3.9 `Address already in use` on port 8000

```bash
# Linux/macOS
sudo lsof -i :8000
sudo kill <pid>
# Windows
netstat -ano | findstr :8000
taskkill /PID <pid> /F
```
…or change `APP_PORT` in `.env`.

### 3.10 Worker tasks stay `PENDING` forever

- Redis down → see [3.1](#31-connectionrefusederror-for-redis).
- Worker not started → 
  ```bash
  celery -A worker.tasks.celery_app worker -l info -c 2
  # Docker:
  docker-compose up -d worker beat
  ```
- Broker URL mismatch → align `CELERY_BROKER_URL`.

---

## 4. Connection Issues

### 4.1 Telegram client shows **Disconnected**

**Steps:**
1. Check **Settings → Telegram Connection** — are API ID/Hash correct?
2. Re-save the session:
   ```bash
   # API route used by the dashboard
   POST /api/account/session      → set api_id/api_hash/phone
   POST /api/account/session/connect
   ```
3. Verify network connectivity to Telegram (some regions block MTProto):
   ```bash
   curl -s https://my.telegram.org | head
   ```
4. Check log for connection errors (`Error` / `AuthKeyError` / `ConnectionReset`).
5. Restart the server so the manager reconnects.

### 4.2 `LoginCode required` / "code sent" but no code arrives

- Telegram throttles SMS/call codes — wait 60–120 s.
- If using a bot-scoped/new number, ensure the phone is entered in international format (`+...`).
- 2FA enabled? Provide the account password when prompted.

### 4.3 Keep disconnecting / `EOFError` on reconnect

- Telegram rejects parasite/userbot sessions that are *too new* or created with the wrong API app type. Create the app as **Desktop** at my.telegram.org.
- Your IP may have changed and the session is now recognized from a new location — this can trigger a re-auth.

### 4.4 WebSocket notifications don't arrive

- Set `WEBSOCKET_ENABLED=true` (default).
- Connect to `ws://<host>/ws` (relative path configurable via `WEBSOCKET_PATH`).
- If behind nginx, the `/ws` route needs upgrade headers (see [INSTALL.md](INSTALL.md)).
- Try `wscat -c ws://localhost:8000/ws` to test raw WebSocket connectivity.

### 4.5 `Failed to authenticate` (401) from Telegram API

The API credentials are wrong or the account was restricted:
- Re-check api_id (number) and api_hash (32 chars).
- Visit https://my.telegram.org → API development tools and confirm.
- If the account itself was flagged, wait for restrictions to lift before spamming.

---

## 5. Database Problems

### 5.1 SQLite: `database is locked`

Happens when multiple processes access the same SQLite file (rare in this stack, but possible if two app instances run).

**Fix:**
- Run a single app instance (`--workers` is ignored in dev/reload mode; in production prefer PostgreSQL).
- Use PostgreSQL for anything concurrent (see [INSTALL.md](INSTALL.md)).

### 5.2 Migrations out of sync

**Symptoms:** `Error` during `migrate`, "target database is not up to date", or new tables missing.

**Fix:**
```bash
# Show current revision
python -m backend.app.main migrate --help   # (migrate only goes to head)

# Inspect alembic state
alembic current
alembic history
alembic upgrade head --sql   # preview the SQL
```
If your DB is irrecoverably out of sync with **no data you care about**, delete `storage/database.db` and re-migrate.

### 5.3 PostgreSQL: `password authentication failed`

- Double-check `DATABASE_URL` credentials.
- PostgreSQL 15+ uses `scram-sha-256`; ensure the user has a password set:
  ```sql
  ALTER USER telegram_bot WITH PASSWORD '...';
  ```
- Confirm the database exists and host/port are reachable.

### 5.4 Connection pool exhaustion

**Symptoms:** intermittent `TimeoutError` on DB operations under load.

**Fix (.env):**
```env
DATABASE_POOL_SIZE=20
DATABASE_MAX_OVERFLOW=40
DATABASE_POOL_RECYCLE=3600
```

### 5.5 Disk full / storage quota

- Media grows under `storage/media`, backups under `storage/backups`.
- Check `STORAGE_MAX_SIZE` (default 10 GB) and `MAX_UPLOAD_SIZE`.
- Prune: delete old backups, move media to external storage.

---

## 6. Telegram API Limits (FloodWait)

Telegram aggressively limits self-bots/userbots that act too fast. The platform handles `FloodWaitError` with automatic backoff when `TELEGRAM_FLOOD_WAIT_ENABLED=true` (default).

### What FloodWait means

`A wait of X seconds is required` — Telegram pauses your account for X seconds. Typical triggers:
- Multiple logins from same IP/app in short order
- Spamming messages/broadcasts with short delays
- Joining many groups in a short time
- Warming/automation running against daily caps

### Symptoms
- Logs show `FloodWaitError (wait X)`
- Percentage counters in Broadcast/Repeater stall
- Actions randomly "do nothing"

### Prevention (most important)

| Practice | Why |
|---|---|
| Broadcast delay ≥ 3–5 s between sends | `Broadcast.delay_seconds` |
| Account Warming from `beginner` | Let Telegram learn your account is human |
| Respect daily caps in Chat Automation | `max_responses_per_day` |
| Keep rate limiters enabled | `RATE_LIMIT_ENABLED=true` |
| Don't run many automation modules simultaneously on a fresh account | Concentrated load = flags |
| Avoid mass `join` operations on new accounts | Joins are the most scrutinized action |

### If you're already flooded

1. **Stop everything immediately** — use the **Emergency Stop** button (Security Center) or `POST /api/system/emergency-stop`.
2. **Wait out the penalty.** FloodWait durations can be minutes to hours (rarely days for repeated abuse).
3. Don't restart the server in a frenzy — the backoff persists in memory and restarting just delays recovery.
4. Reduce configure levels: lower `max_responses_per_day`, switch warming to `beginner`, add broadcast delay.
5. Consider a few days of *observation only* (no automation) for seriously flagged accounts.

---

## 7. AI Provider Problems

### 7.1 "AI provider not configured"

The provider has no API key:
- Set `OPENAI_API_KEY`, `GEMINI_API_KEY`, `DEEPSEEK_API_KEY`, or `LOCAL_LLM_URL`.
- If using the dashboard, also check you didn't override with a blank key in the automation setup payload.

### 7.2 OpenAI: 401/403

- Key invalid or revoked → regenerate at platform.openai.com.
- Organization/quota limits → check billing.
- Model name typo → `gpt-3.5-turbo` vs a gpt-4 variant.

### 7.3 Gemini: 400/429

- `GEMINI_API_KEY` wrong → regenerate at aistudio.google.com.
- Model not enabled for key/region → use `gemini-pro`.
- Quota → wait or raise quota.

### 7.4 DeepSeek: connection refused / CORS

- Uses `https://api.deepseek.com/v1` via OpenAI SDK — verify network can reach it.
- Verify `DEEPSEEK_API_KEY`.

### 7.5 Local LLM (`LOCAL_LLM_URL`)

- Default URL is `http://localhost:11434` (Ollama-style `/api/generate`).
- The server must be running on the host (in Docker, use `host.docker.internal` or a service URL).
- Model `llama2` must be pulled locally.

### 7.6 Responses return "AI error: ..."

Check the log line `AI error` — it contains the provider's own error message and is usually self-explanatory (quota, rate, model not found).

---

## 8. Performance Optimization

### Server tuning (.env)

```env
APP_WORKERS=4            # number of uvicorn workers (prod)
DATABASE_POOL_SIZE=20    # PG only
DATABASE_MAX_OVERFLOW=40
RATE_LIMIT_REQUESTS=30   # raise if you have many concurrent clients
```

### Use PostgreSQL instead of SQLite for any real load

SQLite is single-writer; PostgreSQL scales with the connection pool.

### Frontend caching

- Serve the built `frontend/dist` behind nginx with cache headers for static assets.
- The dashboard bundles Vue 3; keep it built fresh after upgrades.

### Media handling

- Set `STORAGE_MAX_SIZE` sane and prune old media.
- Disable duplicate detection cost concerns are negligible (SHA-256 streaming).

### Worker concurrency

```bash
celery -A worker.tasks.celery_app worker -l info -c 4   # more concurrency
```
Watch memory: each worker holds Python + Telethon objects.

### Keep an eye on

- **System Health** page: CPU, Memory, Disk percentages.
- Celery throughput: `celery -A worker.tasks.celery_app inspect active`.

---

## 9. Log Analysis

The app uses **structlog** — lines are structured key/value JSON-ish entries. Patterns to look for:

| Pattern | Meaning | Action |
|---|---|---|
| `ERROR` | A service threw an exception | Read the message + traceback |
| `WARNING` + `EMERGENCY` | Emergency stop activated | Investigate who/what triggered it |
| `FloodWaitError` | Rate limit hit | See [section 6](#6-telegram-api-limits-floodwait) |
| `Authentication` / `AuthKeyUnregistered` | Session invalidated | Re-auth the Telegram account |
| `ConnectionResetError` | Network/MTProto blip | Usually transient; check connectivity |
| `Rate limit hit for X` | Anti-abuse firing | Slow down automation for `X` |

**Filtering examples:**

```bash
grep -iE "error|exception" storage/logs/app.log | tail -n 100
grep -i flood storage/logs/app.log | tail -n 20
grep -i "emergency" storage/logs/app.log
```

**Audit trail:** the `audit_logs` table records every user action (who/when/what/result). Use the Security/audit endpoints to trace "who changed this".

---

## 10. Recovery Procedures

### 10.1 Recovering from a crashed install without losing data

1. **Back up the data dirs** (do this regularly anyway):
   ```bash
   cp -r storage storage.bak
   ```
   In Docker, the `./storage` bind-mount is your backup.
2. Preserve the `.env` (sessions/keys are encrypted with `ENCRYPTION_KEY`, so **never lose it** — without it, backed-up sessions and encrypted backups cannot be decrypted).
3. Reinstall per [INSTALL.md](INSTALL.md), then copy `storage.bak/*` back.

### 10.2 Restoring a platform backup

1. Backups page → **Restore** on the desired backup.
2. Or via API: `POST /api/backups/{backup_id}/restore`.
3. Backups are validated by SHA-256 hash; a hash mismatch means a corrupted file — do **not** trust it.

### 10.3 Reconnecting after a Telegram session ban/invalid auth

1. Create a **fresh** API app at my.telegram.org (some bans are app-scoped).
2. In Settings, save the new `api_id`/`api_hash`.
3. Clear the stored session (`TELEGRAM_SESSION_STRING`), reconnect, and complete the login code + 2FA.
4. Resume with **Account Warming at beginner** — no broadcasting for the first few days.

### 10.4 Forget password / locked out of dashboard

Run the CLI from the server console:
```bash
python -m backend.app.main init-admin   # idempotent — recreates default admin if missing
```
> If admin already exists, connect to the DB directly to reset the bcrypt hash via SQLAlchemy, or DROP the user row then re-run `init-admin`.

### 10.5 Emergency stop accidentally engaged

Stop everything, then reset the internal flag. If you can't from the UI:
```bash
# Restart the app — emergency stop is in-memory
docker-compose restart app
# or non-Docker
# restart the process
```
Only do this after confirming it was a mistake.

### 10.6 Full wipe and fresh start (destructive)

```bash
# Non-Docker
rm -f storage/database.db
python -m backend.app.main migrate
python -m backend.app.main init-admin

# Docker
docker-compose down -v && docker-compose up -d --build
docker-compose exec app python -m backend.app.main migrate
docker-compose exec app python -m backend.app.main init-admin
```

---

## Still stuck?

- Check the **Logs** section in the dashboard and include relevant lines in any bug report.
- Provide: OS + Python version, install method (script / manual / Docker), and the exact error text.
- Consult the [User Guide](USER_GUIDE.md), [Features doc](docs/FEATURES.md), and [Installation doc](INSTALL.md) for context.
- Open the Swagger UI at `http://localhost:8000/api/docs` to test endpoints interactively while debugging.