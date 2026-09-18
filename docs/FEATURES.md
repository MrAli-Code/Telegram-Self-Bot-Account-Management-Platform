# Telegram Self-Bot — Features Documentation

Complete reference for every feature of the **Telegram Self-Bot / Account Management Platform** (v1.0.0).

The platform is a professional, modular, production-ready Telegram self-bot and account management system built on **FastAPI**, **Vue 3**, **Telethon (MTProto)**, **SQLAlchemy**, **Redis**, and **Celery**.

---

## Table of Contents

1. [Architecture at a Glance](#1-architecture-at-a-glance)
2. [New Trending Features](#2-new-trending-features)
3. [AI Capabilities](#3-ai-capabilities)
4. [Automation Features](#4-automation-features)
5. [Communication & Monitoring](#5-communication--monitoring)
6. [Security Features](#6-security-features)
7. [Media Features](#7-media-features)
8. [Data Management](#8-data-management)
9. [Platform & UX](#9-platform--ux)
10. [Plugin System](#10-plugin-system)
11. [API Reference Summary](#11-api-reference-summary)
12. [Comparison with Telegram's Native Features](#12-comparison-with-telegrams-native-features)

---

## 1. Architecture at a Glance

```
┌───────────────────────────────────────────────┐
│      Web Dashboard (Vue 3 + Pinia + Router)   │
│     REST API + WebSocket  (FastAPI / Uvicorn) │
├───────────────────────────────────────────────┤
│              Application Layer                 │
│   Auth · Security · Scheduler · AutoReply      │
│   Media Archive · Backup · Broadcast · Logs    │
├───────────────────────────────────────────────┤
│              Telegram Engine (Telethon)        │
│       MTProto Client · Sessions · Handlers     │
├───────────────────────────────────────────────┤
│        Data Layer · Task Queue                │
│  SQLite/PostgreSQL · Redis · Storage · Celery │
└───────────────────────────────────────────────┘
```

**Key components**

| Layer | Tech |
|---|---|
| Backend API | FastAPI (`/api`), OpenAPI docs at `/api/docs` |
| Frontend | Vue 3 + TypeScript, Vite, Pinia, vue-i18n (EN/FA), Chart.js |
| Telegram client | Telethon (MTProto) with session management & FloodWait handling |
| Database | SQLAlchemy async — SQLite (default) / PostgreSQL / MySQL |
| Cache & queues | Redis (+ Celery worker & beat) |
| Real-time | WebSocket at `/ws` |
| Extensibility | Plugin system under `plugins/` |

---

## 2. New Trending Features

These are the newest additions, mirroring — and extending — the automation features Telegram itself has started advertising (Chat Automation, etc.).

### 2.1 AI Chat Automation ⭐

Telegram's own *Chat Automation* (Settings → Chat Automation) lets you connect a bot to respond in your chats automatically. This platform implements the **self-hosted equivalent**: a fully coded AI **profile** that replies on your behalf.

**Capabilities**
- Multiple AI backends: OpenAI, Gemini, DeepSeek, local LLM
- Personality presets: `friendly`, `professional`, `casual`, `sales`, `support`
- Scoping: respond in `all` chats, exclude specific chats, or restrict by ID
- Daily response quota (`max_responses_per_day`)
- Randomized human-like delay between `response_delay_min` and `response_delay_max` seconds
- Working-hours window support
- Auto language matching, full response log per user

**API** → `/api/automation/chat-automation/*` (setup, toggle, log)

### 2.2 Account Warming ⭐

Gradually and **safely** ramps an account's activity to avoid Telegram restrictions. Critical for brand-new accounts and long-dormant ones.

**Capabilities**
- 4 intensity tiers: `beginner` → `intermediate` → `advanced` → `expert`
- Simulated human behavior: random typing, reading messages, viewing stories, scrolling feeds, occasional messages, all with random delays
- Strict daily caps (messages, joins, actions per hour)
- Online-window awareness (never active in the "dead of night")
- Automatic **level-up scheduling** over the warming duration (default 14 days)
- Live status: actions/messages/joins today vs. max, total actions, active window

**API** → `/api/automation/warming/*` (start, status, stop, levels)

### 2.3 Neuro Dialogs ⭐

Personality-driven, **context-aware** AI conversations. Unlike one-shot auto-replies, Neuro Dialogs keep a **rolling context window** and respond naturally within real chats.

**Capabilities**
- Persistent per-chat sessions with conversation history
- 5 built-in personalities incl. **bilingual Persian** (`bilingual_fa`) and **bilingual Arabic** (`bilingual_ar`)
- Custom system prompts and configurable context window (default 10 messages)
- Automatic history trimming
- Saved prompt templates

**API** → `/api/automation/neuro-dialog/*` (create, templates)

### 2.4 Smart Forward ⭐

Selective message forwarding from a source chat to one or more target chats, with content filtering and transformation.

**Capabilities**
- Keyword include / exclude filters
- Minimum message length filter
- Sender whitelist filter
- Transforms: prefix, suffix, remove "Forwarded from:" markers
- Per-rule forwarded-message counters

**API** → `/api/automation/smart-forward/*` (create, rules)

### 2.5 Multi-Account Management ⭐

Operate **multiple Telegram accounts** from one dashboard.

**Capabilities**
- Account registry with API credentials, phone, notes, active/connected state
- Per-account toggles for auto-reply, warming, and chat automation
- Companion **User Parser** — extract contact lists from groups/channels for targeting broadcasts

**API** → `/api/automation/multi-account/*` (add, list, delete)

---

## 3. AI Capabilities

| Provider | Backend | Env keys | Model default |
|---|---|---|---|
| OpenAI | `openai` | `OPENAI_API_KEY` | `gpt-3.5-turbo` |
| Google Gemini | `gemini` | `GEMINI_API_KEY` | `gemini-pro` |
| DeepSeek | `deepseek` | `DEEPSEEK_API_KEY` | `deepseek-chat` |
| OpenRouter | (via `openai` SDK) | `OPENROUTER_API_KEY` | — |
| Local LLM (Ollama-style) | `local` | `LOCAL_LLM_URL` | `llama2` at port 11434 |

**Where AI is used**
- AI **Chat Automation** (self-hosted equivalent of Telegram's native feature)
- **Neuro Dialogs** (conversational sessions)
- **Text-to-voice / voice-to-text** via FFmpeg + Whisper (`WHISPER_MODEL`)

**Architecture:** `AIProviderFactory` + abstract `AIProvider` — you can `register()` custom providers. Install extras with `pip install -e ".[ai]"`.

---

## 4. Automation Features

### 4.1 Auto Reply Engine
Rule-based automatic responses with:

- **6 trigger types**: `exact`, `contains`, `starts_with`, `ends_with`, `regex`, `command`
- Priority ordering (highest first)
- Random multi-response selection
- Chat scope (`all`/`private`/`group`), user scope (whitelist), blocked users
- Working hours + working days
- Max-reply counters and configurable delay
- Media responses (photo/video/voice/document/sticker) supported
- Limits: up to 1000 rules (plugin config)

**API** → `/api/autoreply/*`

### 4.2 Scheduler
Cron / interval / one-time task execution (APScheduler in-process + Celery beat background checks).

- `cron_expression`, `interval_seconds`, or exact `run_at`
- Message or media delivery to a target chat
- Max runs, last/next run tracking, run counts
- Enable/disable toggle, "run now"

**API** → `/api/scheduler/*`

### 4.3 Broadcast
Rate-limited mass messaging.

- Text or media payloads
- Target types + target ID lists (chats/contacts/groups/channels)
- Inter-message **delay** (default 5 s) to avoid FloodWait
- Lifecycle: draft → running → paused/resumed → completed/cancelled
- Live progress (`sent_count / total_targets`) and error log

**API** → `/api/broadcast/*`

### 4.4 Message Repeater
Repeated delivery of a message at fixed intervals.

- Interval seconds, optional max repetitions, cooldown
- Working-hours window
- Session tracking (last run, next run)

**API** → `/api/repeater/*`

### 4.5 Workflow Builder
Graph-based automation (JSON **nodes** + **edges**).

- Trigger events (e.g. `on_new_message`)
- Enable/disable, run count, last run
- Full CRUD via REST

**API** → `/api/workflows/*`

### 4.6 Group Automation
- Anti-link, anti-spam, anti-flood (threshold + window), anti-forward
- Keyword filtering, welcome messages, rules text, auto-reply
- Member moderation: mute / ban / unban

**API** → `/api/groups/*`

### 4.7 Channel Automation
- Auto-post enablement
- Scheduled post queues
- Comment management
- Per-channel settings

**API** → `/api/channels/*`

---

## 5. Communication & Monitoring

### Message Archive
Full MTProto message history with search, filtering, and export. `Message` model stores text, sender, chat, dates (`message_date`, `edit_date`), media flags, forward provenance, and raw JSON payload.

### Deleted Message Tracking
`DeletedMessage` records preserve the **original text/content** of deleted and "ghost-edited" messages plus sender and timestamp — useful against spam bots that clean up after themselves.

### Story Archive
Stories from contacts are archived (media downloaded locally) every **6 hours** by the beat task `archive_stories`. Fields include caption, media type/path, views, expiry, and dimensions.

### Profile Monitor
Hourly `monitor_profiles` beat task captures profile changes (username, first/last name, bio) into `ProfileChange` records with old → new values.

### Friends / Enemies
- **Friends**: categories, priority, specialized notifications, auto-reply flags, ignore settings, notes/tags.
- **Enemies**: default actions (`mute`), alert-on-message, auto-block, auto-restrict, notes/tags.

### Notifications & WebSocket
- `Notification` model with severity and read state; real-time WebSocket channel at `/ws`.
- **API** → `/api/notifications/*`

---

## 6. Security Features

### Authentication
- JWT access tokens (30 min) + refresh tokens (7 days)
- bcrypt password hashing
- Enforced CSRF middleware
- Rate limiting (30 req/min/IP by default) — `RateLimitMiddleware`
- Audit logging of every action — `AuditMiddleware`

### Security Center
- **Sessions table** — connection state & last-connected time
- **Security events feed** — new-login detection (`detect_new_session`), flood-risk analysis (`check_flood_risk`), severity levels, resolved flags
- **Emergency Stop** — one click halts broadcasts, scheduler, auto-reply, repeaters, and all automation
- Anti-abuse engine (`AntiAbuseService`): per-action / per-chat / per-user rate caps plus global kill switch

### Data protection
- `<TELEGRAM_SESSION_STRING>` and session data **encrypted at rest**
- `ENCRYPTION_KEY`-based encryption for backups (`BACKUP_ENCRYPTION_ENABLED`)
- Sessions never exposed in API responses

### Hardening checklist
1. Strong random `APP_SECRET_KEY`, `JWT_SECRET_KEY`, `ENCRYPTION_KEY`, `CSRF_SECRET_KEY`
2. Enable 2FA for dashboard login
3. PostgreSQL in production
4. nginx reverse proxy + TLS
5. Review audit logs and security events weekly

**API** → `/api/security/*`, `/api/system/emergency-stop`, `/health`

---

## 7. Media Features

### Media Archive
- Type-organized storage: photos, videos, voice, audio, documents, GIFs, stickers, animations
- **SHA-256 duplicate detection** (`find_duplicate`)
- Local download paths, thumbnails, dimensions, duration, captions
- Storage stats (files count, total bytes/MB)
- Archive/download/dedupe via REST

**API** → `/api/media/*`

### Media Converter (FFmpeg)
| From | To |
|---|---|
| Text | Voice (TTS) |
| Voice | Text (Whisper STT) |
| Video | Round video |
| Round | Video |
| Audio | Voice |
| Video | Audio |

- Background Celery conversion tasks with progress %
- Requires FFmpeg/FFprobe on PATH or via `FFMPEG_PATH` / `FFPROBE_PATH`

**API** → `/api/converter/*`

---

## 8. Data Management

### Backups
- Full / messages-only / media-only types
- Optional chat and date scoping
- Status lifecycle (pending → running → completed/failed) with progress
- **Encryption + compression** (level configurable)
- Download, restore, delete operations
- SHA-256 integrity hashes

**API** → `/api/backups/*`

### Migration tooling
Alembic migrations via CLI:
```bash
python -m backend.app.main migrate          # upgrade to head
python -m backend.app.main makemigration -m "desc"   # new autogenerated revision
```

### Storage layout
```
storage/
├── database.db        # SQLite (when used)
├── media/<type>/      # archived media
├── backups/           # .zip backup archives
└── logs/app.log       # structured application logs
```

---

## 9. Platform & UX

### Multi-language UI
English and **Persian (RTL)** via vue-i18n — full right-to-left layout switching.

### Themes
Dark (default) and Light themes driven by CSS variables; per-user preference persisted.

### Thin-client live updates
WebSocket channel pushes real-time notifications and connection-state changes to the dashboard.

### System Health
`GET /health` and dashboard page: DB connectivity check, Telegram connection state, CPU/memory/disk/version/platform/Python info.

### API Platform
- Swagger UI `/api/docs`, ReDoc `/api/redoc`, OpenAPI JSON `/api/openapi.json`
- JWT bearer auth, paginated list responses, validation by Pydantic

### CLI
```bash
telegram-bot      # project console script (entry point)
python -m backend.app.main serve [--host] [--port] [--reload] [--workers]
python -m backend.app.main migrate
python -m backend.app.main makemigration -m <message>
python -m backend.app.main init-admin
```

---

## 10. Plugin System

Pluggable modules live under `plugins/<name>/` and register a **manifest** + optional service integration.

| Plugin | Manifest description | Notable config |
|---|---|---|
| `autoreply` | Rule-based matching engine | `max_rules: 1000`, 6 trigger types, media responses |
| `backup` | Full backup & restore | `zip/json/html/txt/csv` formats, encryption, compression |
| `security` | Monitoring & anti-abuse | alert on new session, max login attempts: 5 |
| `media` | Media archive | `max_file_size: 52428800`, duplicate detection |
| `scheduler` | Task scheduling | `max_concurrent_tasks: 10`, tz `UTC` |
| `converter` | Media conversion engine | FFmpeg path, 6 conversion pairs |
| `statistics` | Analytics | retention 90 days, line/bar/pie charts |

Manifest fields: `name`, `version`, `description`, `author`, `permissions`, `enabled`.

> Extension path: add a `plugins/<name>/` folder with a manifest and service, register routes if needed, and enable it in config.

---

## 11. API Reference Summary

Base URL: `http://<host>:8000/api` · Auth: `Authorization: Bearer <token>`

| Module | Endpoints (representative) | Description |
|---|---|---|
| **Auth** | `POST /auth/register`, `POST /auth/login`, `POST /auth/refresh` | User auth |
| **Account** | `GET/POST /account/session`, `POST /account/session/connect` | Telegram session mgmt |
| **Messages** | `GET /messages/`, `GET /messages/{id}`, search & filters | Archive + search |
| **Media** | `GET /media/`, `GET /media/{id}`, `GET /media/stats`, download | Media archive |
| **Stories** | `GET /stories/`, `GET /stories/{id}` | Story archive |
| **Profile** | `GET /profile/`, `GET /profile/changes` | Profile monitor |
| **AutoReply** | `GET/POST /autoreply/`, `PATCH /autoreply/{id}/toggle`, `DELETE` | Rules |
| **Friends** | `GET/POST /friends/`, CRUD | Friend categories |
| **Enemies** | `GET/POST /enemies/`, CRUD | Enemy actions |
| **Groups** | `GET /groups/`, `GET /groups/{id}/management`, `POST .../management`, member mute/ban/unban | Group mgmt |
| **Channels** | `GET /channels/`, management endpoints | Channel mgmt |
| **Security** | `GET /security/events`, `GET /security/sessions`, `GET /security/summary` | Security center |
| **Backups** | `GET/POST /backups/`, `POST /backups/{id}/restore`, `GET .../download`, `DELETE` | Backup/restore |
| **Scheduler** | `GET/POST /scheduler/`, `PATCH /scheduler/{id}/toggle`, `POST /scheduler/{id}/run`, `DELETE` | Scheduled tasks |
| **Statistics** | `GET /statistics/account`, `GET /statistics/messages`, etc. | Analytics |
| **Converter** | `GET /converter/formats`, `GET /converter/`, POST conversions | FFmpeg conversions |
| **Broadcast** | `GET/POST /broadcast/`, `POST /broadcast/{id}/start\|pause\|resume\|cancel` | Mass messaging |
| **Repeater** | `GET/POST /repeater/`, toggle, delete | Repeats |
| **Workflows** | `GET/POST /workflows/`, `GET/PUT/PATCH/DELETE /workflows/{id}` | Visual automation |
| **Notifications** | `GET /notifications/` | Read notifications |
| **System** | `GET /system/health`, `POST /system/emergency-stop`, `GET /system/info` | Ops |
| **Search** | `GET /search/?q=` | Global search |
| **Automation & AI** | `POST /automation/chat-automation/setup`, `POST /automation/warming/start`, `POST /automation/neuro-dialog/create`, `POST /automation/smart-forward/create`, `POST /automation/multi-account/add` | Trending AI/Automation |

**Health** (no auth): `GET /health`

**Docs:** Swagger UI → `/api/docs` · ReDoc → `/api/redoc` · OpenAPI → `/api/openapi.json`

---

## 12. Comparison with Telegram's Native Features

| Capability | Telegram Native | This Platform |
|---|---|---|
| Chat Automation | Closed bot-based, limited | Self-hosted AI with personalities/scopes/quotas |
| Message Search | Limited in-app | Full archive + regex/filters + history |
| Deleted message tracking | Not available | Full capture |
| Story archiving | Not available (stories expire) | Permanent local archive |
| Profile change alerts | Not available | Automated monitoring |
| Account warming | Not available | Scheduled human-like ramp-up |
| Smart forwarding w/ filters | Not available | Rule + transform engine |
| Mass broadcast | Slow/manual | Rate-limited scheduled engine |
| Backups | Chat export only | Encrypted full data backup/restore |

---

*Companion documents: [INSTALL.md](../INSTALL.md) · [USER_GUIDE.md](../USER_GUIDE.md) · [TROUBLESHOOTING.md](../TROUBLESHOOTING.md) · [docs/ARCHITECTURE.md](ARCHITECTURE.md) · [docs/SECURITY.md](SECURITY.md)*