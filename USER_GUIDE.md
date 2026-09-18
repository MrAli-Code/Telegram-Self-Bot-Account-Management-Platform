# Telegram Self-Bot — User Guide

Welcome to the **Telegram Self-Bot / Account Management Platform**. This guide walks you through every part of the dashboard, from basic navigation to advanced AI-powered automation.

> **Quick facts before you start**
>
> - Dashboard URL: `http://localhost:8000`
> - Default admin: `admin` / `admin123` (change it!)
> - The interface has a collapsible dark sidebar; the gear icon (`⚙️`) at the bottom opens **Settings**
> - English and Persian (RTL) are supported

---

## Table of Contents

1. [Dashboard Overview](#1-dashboard-overview)
2. [Dashboard Section](#2-dashboard)
3. [Messages](#3-messages)
4. [Media Archive](#4-media-archive)
5. [Deleted Messages](#5-deleted-messages)
6. [Stories](#6-stories)
7. [Profile Monitor](#7-profile-monitor)
8. [Auto Reply](#8-auto-reply)
9. [Friends & Enemies](#9-friends--enemies)
10. [Backups](#10-backups)
11. [Groups & Channels](#11-groups--channels)
12. [Security Center](#12-security-center)
13. [Scheduler](#13-scheduler)
14. [Broadcast](#14-broadcast)
15. [Repeater](#15-repeater)
16. [Statistics](#16-statistics)
17. [Media Converter](#17-media-converter)
18. [Workflow Builder](#18-workflow-builder)
19. [Logs](#19-logs)
20. [System Health](#20-system-health)
21. [Settings & Themes](#21-settings--themes)
22. [AI Chat Automation (Trending)](#22-ai-chat-automation-trending)
23. [Account Warming (Trending)](#23-account-warming-trending)
24. [Neuro Dialogs (Trending)](#24-neuro-dialogs-trending)
25. [Smart Forward (Trending)](#25-smart-forward-trending)
26. [Multi-Account Management (Trending)](#26-multi-account-management-trending)
27. [Keyboard Shortcuts](#27-keyboard-shortcuts)

---

## 1. Dashboard Overview

After logging in you land on the **Dashboard**, the control center for the entire platform.

**Sidebar navigation** (top to bottom):

| Icon | Section | Purpose |
|---|---|---|
| 📊 | Dashboard | Overview stats and recent activity |
| 💬 | Messages | Message archive & search |
| 🖼️ | Media Archive | Photos, video, voice, documents |
| 🗑️ | Deleted Messages | Tracked deletions |
| 📖 | Stories | Archived stories |
| 👤 | Profile Monitor | Profile change tracking |
| 🤖 | Auto Reply | Rule-based auto reply |
| ❤️ | Friends | Categorized contacts |
| 🚫 | Enemies | Blocked/restricted contacts |
| 💾 | Backups | Backup & restore |
| 👥 | Groups | Group management |
| 📢 | Channels | Channel management |
| 🔒 | Security Center | Sessions, events, emergency stop |
| ⏰ | Scheduler | Cron/interval tasks |
| 📡 | Broadcast | Mass messaging |
| 🔁 | Repeater | Repeated messages |
| 📈 | Statistics | Analytics |
| 🔄 | Media Converter | FFmpeg conversions |
| ⚡ | Workflows | Visual automation builder |
| 📋 | Logs | Application logs |
| 💚 | System Health | CPU/memory/disk metrics |
| ⚙️ | Settings | Connection, theme, language |

The **connection status** (green/red dot at the bottom of the sidebar) shows whether the Telegram client is connected.

---

## 2. Dashboard

The dashboard summarizes everything happening in your account.

**Stat cards you'll see:**
- **Total Chats** / **Private Chats** / **Groups** / **Channels**
- **Total Messages**
- **Total Media**
- **Total Contacts**
- **Stories**
- **Deleted Messages**
- **Connection Status**
- **Recent Activity** list (latest events in chronological order)

**Practical tips:**
- Use the dashboard as your daily "health check" — if media or message counts stop growing, your Telegram session may have disconnected.
- Click any stat to jump into the related section for details.

---

## 3. Messages

The **Messages** section is a searchable archive of every message Telegram has processed for your account.

**What you can do:**
- **Browse** all archived messages (paged list).
- **Search** by text, chat, or sender.
- **Filter** by chat type (private / group / channel), date range, and media presence.
- **View message details**: sender, timestamp, edit date, media type, and whether it was forwarded.

**Practical tips:**
- Search is case-insensitive and matches partial text.
- Use the `has_media` filter to find only messages that contain photos, videos, or files.
- Deleted messages that were tracked while online continue to appear under **Deleted Messages**, not here.

---

## 4. Media Archive

The **Media Archive** automatically organizes all photos, videos, voice notes, audio, documents, GIFs, stickers, and animations you've received.

**What you can do:**
- Browse by **type**: Photos, Videos, Voice, Audio, Documents, GIFs, Stickers, Animations.
- See **Total Size** used and the number of **duplicates** detected.
- **Download** any archived file.
- Media is **deduplicated** using SHA-256 file hashes — identical files are stored once.

**Practical tips:**
- Storage is bounded by `STORAGE_MAX_SIZE` (default 10 GB) in `.env`.
- Files are stored under `storage/media/<file_type>/` on disk.
- Duplicate detection compares content hashes, so re-sent or re-forwarded files are recognized even with different file names.

---

## 5. Deleted Messages

Telegram's "ghost" edits and deletions are captured by the update handler while your session is online.

**What you can do:**
- See **original text** of deleted messages.
- See **who** sent them and **when**.
- Browse by chat.
- The Telegram message ID is preserved for cross-referencing.

**Practical tips:**
- Spam bots that "delete their message after sending" are the classic use case — their text is preserved here.
- Deleted messages are also kept via the `DeletedMessage` model with raw event data, so you can inspect exactly what was sent.

---

## 6. Stories

The **Stories** section archives Stories posted by your contacts (photo, video, or other media).

**What you can do:**
- Browse archived stories with captions, media type, and views.
- See **expiry timestamps**.
- Media is stored locally so it remains available after the story expires on Telegram.
- The Celery **beat** scheduler runs `archive_stories` every 6 hours to keep the archive fresh.

**Practical tips:**
- Stories that you don't open will still be archived in the background if your account is actively connected.
- Use the archive to monitor story activity without leaving "seen" traces if that matters to your workflow.

---

## 7. Profile Monitor

The **Profile Monitor** tracks changes to contact profiles — usernames, first names, last names, and bios.

**What you can do:**
- See a **change history** per contact (`ProfileChange` records).
- Understand **what changed** (old value → new value) and **when**.
- The scheduler checks profiles **hourly** (`monitor_profiles` beat task).

**Practical tips:**
- Great for detecting username squatters or spotting when a contact rebrands.
- Combine with the REST API to build alerts on top of change data.

---

## 8. Auto Reply

The **Auto Reply** engine responds automatically to incoming messages based on **rules**. This is one of the most powerful features of the platform.

### Creating a rule

Click **+ Create Rule** and configure:

| Field | Description |
|---|---|
| **Name** | A label for the rule |
| **Trigger Type** | How the trigger matches incoming text |
| **Trigger Value** | The pattern to match |
| **Response** | The text (or media) to send back |
| **Delay (seconds)** | Wait before replying (human-like pacing) |
| **Priority** | Higher priority rules are evaluated first |
| **Chat Scope** | `all` / `private` / `group` |
| **User Scope** | `all` / `whitelist` (only `allowed_users`) |
| **Working Hours** | Only reply during this window (hour 0–23) |

### Trigger types

| Type | Matches when… | Example |
|---|---|---|
| `exact` | Text equals the trigger (case-insensitive) | trigger `hi` matches only `hi` |
| `contains` | Text contains the trigger | trigger `price` matches *"what's the price?"* |
| `starts_with` | Text begins with the trigger | trigger `order` matches *"order status?"* |
| `ends_with` | Text ends with the trigger | trigger `ok` matches *"that's ok"* |
| `regex` | Text matches a regular expression | `\b(hello|hey|hi)\b` |
| `command` | Text is a command or starts with `/` | `/start`, `start` |

### Example rules

**1. Greeting responder**
- Trigger type: `contains` · Trigger value: `hi` · Response: *"Hello! How can I help you?"* · Delay: `2`

**2. Price inquiry (higher priority overlaps)**
- Trigger type: `regex` · Trigger value: `price|cost|how much` · Priority: `10` · Response: *"Our plans start at $9/mo. Chat scope: private."*

**3. After-hours silence**
- Trigger type: `exact` · Trigger value: `help` · Working hours: `9` to `18` · Delay: `1`

### Advanced settings
- **Multiple responses** (`responses` field): one is chosen at **random**, making replies feel natural.
- **Blocked users**: skip replying to specific sender IDs.
- **Max replies**: stop replying after N total replies.
- **Working days**: restrict which days rules are active.

> **Tip:** Keep the delay between 1–5 seconds for a human-like feel and to avoid Telegram rate limits.

---

## 9. Friends & Enemies

### Friends
Categorize important contacts for special treatment:
- **Category** and **priority** tags
- **Auto-reply enabled** — rules with user scope apply
- **Ignore messages** — suppress/mark-as-read handling
- **Special notification** — elevated in-app alert
- **Notes** and **tags** for your own organization

### Enemies
Manage contacts you want to restrict:
- Default **action** (`mute`) applied when they message
- **Alert on message** — notify you instantly
- **Auto-block** — block immediately
- **Auto-restrict** — restrict their messages
- **Notes** + tags

**Practical tips:**
- Use the Friends list to prioritize who gets AI features (e.g. Neuro Dialogs).
- Enemies work well with the Security Center's event log — alerts on unwanted contacts create `SecurityEvent` records.

---

## 10. Backups

Back up and restore your data with the built-in **Backup** engine.

### Creating a backup
Click **+ Create Backup**, then set:
- **Name** — e.g. `weekly-backup-2025-06-01`
- **Type**:
  - `full` — everything
  - `messages` — message text only
  - `media` — media files only
- **Include Media** — attach media files to the archive

Options available via API: set `chat_ids`, `date_from`, `date_to` to back up a **subset** of chats or a date range.

### Managing backups
Each backup has a **status** (`pending`, `running`, `completed`, `failed`) and a **progress** percentage. You can:
- **Download** completed backups (`/api/backups/{id}/download`)
- **Restore** a backup
- **Delete** old backups

Backups are:
- Stored in `storage/backups/`
- **Encrypted** when `BACKUP_ENCRYPTION_ENABLED=true`
- **Compressed** with configurable level (`BACKUP_COMPRESSION_LEVEL`, default 6)
- SHA-256 hashed for integrity checks

**Practical tips:**
- Schedule regular backups with a Repeater/Scheduler task, or run one before upgrading.
- A backup file is a `.zip`; un-encrypted backups can be inspected directly.

---

## 11. Groups & Channels

### Groups
The **Groups** section lists all groups/supergroups. On each group you can configure **Group Management**:

| Feature | Description |
|---|---|
| **Anti-Link** | Block/remove messages containing links |
| **Anti-Spam** | Heuristic spam detection |
| **Anti-Flood** | Mute users who flood (threshold + window in seconds) |
| **Anti-Forward** | Block forwarded messages |
| **Keyword Filter** | Block messages containing blacklisted keywords |
| **Welcome Message** | Greet new members |
| **Rules Text** | Post configured rules |
| **Auto Reply** | Enable the auto-reply engine inside the group |

**Member moderation:**
- **Mute** a member (`POST /groups/{chat_id}/members/mute`)
- **Ban** a member (`POST /groups/{chat_id}/members/ban`)
- **Unban** (`POST /groups/{chat_id}/members/unban`)

### Channels
Manage your channels with **Channel Management**:
- **Auto Post** — schedule posts automatically
- **Scheduled Posts** — a JSON list of queued posts
- **Comment Management** — moderate discussion
- Per-channel **settings** JSON

**Practical tips:**
- Combine anti-spam + keyword filters for quiet but safe public groups.
- The welcome system is the fastest way to professionally onboard new members.

---

## 12. Security Center

The **Security Center** monitors everything that could compromise your account.

### Emergency Stop 🛑
The big red **EMERGENCY STOP** button immediately halts **all** automation:
- Broadcasts
- Scheduled tasks
- Auto-reply
- Repeaters

It is exposed via `POST /api/system/emergency-stop`. Use it the moment you suspect abuse or a problem.

### Sessions
Table of connected Telegram sessions with status (**Connected** / **Disconnected**) and last-connected time.

### Security Events
A feed of events with:
- **Type** (e.g. `new_login`)
- **Severity** — `critical` / `warning` / `info`
- **Title** and **description**
- **Resolved** state

The security service automatically detects **new sessions** and raises flood-risk warnings. The event summary cards on top show:
- **Unresolved events**
- **Critical events**
- **Total events**

### Audit integration
Every API action is recorded to the **audit log** (who, what, when, IP, result), giving you a complete trail.

**Practical tips:**
- Review the events feed weekly.
- If you see a new session you don't recognize, use emergency stop, rotate secrets, and log out all sessions.
- Anti-abuse rate limits (per action / per chat / per user) are enforced automatically by `AntiAbuseService`.

---

## 13. Scheduler

Create **cron-based** or **interval-based** tasks that run automatically.

**Task fields:**
- **Name**
- **Task type**
- **Schedule type**: `cron` (5-field cron expression) / `interval` (seconds) / one-time `run_at`
- **Target chat** and **message** to send
- **Max runs** (stop after N) and **working hours**

**Managing tasks:**
- Create / edit / delete tasks
- **Toggle** enabled/disabled
- **Run now** — queues the task for immediate execution

The scheduler is powered by **APScheduler** in the app, and the Celery **beat** service periodically checks `worker.tasks.check_scheduled_tasks` (every minute) for additional scheduled jobs.

**Example cron expression:** `0 9 * * 1-5` = 09:00 Monday–Friday.

**Practical tips:**
- Use `SCHEDULER_TIMEZONE` in `.env` to set a local timezone (default `UTC`).
- For "repeat message every X": the **Repeater** is usually a better fit than the Scheduler (see below).

---

## 14. Broadcast

Send a message (or media) to **many targets** at once, with built-in rate limiting.

**Broadcast fields:**
- **Name** and **message text** (or media)
- **Target type** and **target IDs** (chats/contacts/groups/channels)
- **Delay seconds** between sends (default 5 — important to avoid FloodWait)

**Workflow:**
1. **Create** a broadcast (status `draft`)
2. **Start** it — status becomes `running`, progress shows `sent_count / total_targets`
3. Optional **Pause** / **Resume**
4. **Cancel** drops the rest
5. On completion, status is `completed` and failure counts are tracked in `error_log`

**Practical tips:**
- Never set delay below 3–4 seconds for mass sends to accounts with many targets.
- Media broadcasts reuse the same rate-limiter as text.
- Use the broadcast **with** the account-warming feature on fresh accounts to stay under limits.

---

## 15. Repeater

The **Repeater** resends a message to a target **over and over** on a fixed interval.

**Fields:**
- Message text / media
- Target chat
- **Interval seconds**
- **Max repetitions** (or unlimited)
- **Cooldown seconds**
- Working hours window

**Practical tips:**
- Perfect for "keep-alive" activity or scheduled reminders inside a group/channel.
- Pair intervals with working hours so you don't ping chats at night.
- Tracked with `current_repetitions`, `last_run`, and `next_run`.

---

## 16. Statistics

The **Statistics** section gives you analytical insight into your account activity.

**What's measured (via the statistics API):**
- Messages per chat / per time period
- Media counts by type
- Message volume trends over time
- System retention window: **90 days** by default (configurable in the Statistics plugin)

Charts support line, bar, and pie renderings (`chart_types`).

**Practical tips:**
- Use stats to catch **unusual spikes** (e.g. a sudden flood of messages usually means spam).
- Combine with Security Center events for a full picture.

---

## 17. Media Converter

Convert media directly in the dashboard using **FFmpeg**.

**Supported conversions** (from the Converter plugin):

| From | To | Description |
|---|---|---|
| Text | Voice | Text-to-speech |
| Voice | Text | Speech-to-text (Whisper) |
| Video | Round | Round video message |
| Round | Video | Normalize round video |
| Audio | Voice | Normalize audio as voice message |
| Video | Audio | Extract audio track |

The **Recent Conversions** table shows each task's status and **progress** percentage. Conversions run as background Celery tasks (`run_conversion_task`).

**Prerequisites:** FFmpeg and FFprobe on `PATH` (or configured via `FFMPEG_PATH` / `FFPROBE_PATH`). Whisper transcription uses the model set by `WHISPER_MODEL` (default `base`).

**Practical tips:**
- Convert text to voice for natural voice replies to use with Auto Reply.
- Voice-to-text is handy for archiving important voice messages as searchable text.

---

## 18. Workflow Builder

The **Workflow Builder** lets you create automation as a visual graph of **nodes** and **edges** (triggers → actions).

**Workflow fields:**
- **Name** and description
- **Trigger event** (what starts the workflow, e.g. `on_new_message`)
- **Nodes** — JSON array describing steps (send message, wait, branch, call a service)
- **Edges** — JSON array describing connections between nodes
- **Run count** and **last run** tracking
- **Enabled/disabled** toggle

**Workflow endpoints** (`/api/workflows`):
- `GET /` — list (filter by `is_enabled`, paged)
- `POST /` — create
- `GET /{id}` — get
- `PUT /{id}` — update
- `PATCH /{id}/toggle` — enable/disable
- `DELETE /{id}` — delete

**Practical tips:**
- Start simple: one trigger node that sends a canned reply, then add branches.
- Because nodes/edges are JSON, you can version and import workflows programmatically.

---

## 19. Logs

The **Logs** section streams the application's structured logs (structlog) directly in the dashboard.

**What you'll find:**
- Startup/shutdown events
- Telegram connection events
- Automation actions
- Errors and warnings at the configured `APP_LOG_LEVEL`

Logs are also written to `storage/logs/app.log` (see `APP_LOG_FILE`). A beat task (`cleanup_old_logs`) prunes old log entries every day at 03:00.

**Practical tips:**
- Grep the log file for `EMERGENCY` or `ERROR` to diagnose issues quickly.
- Logs are the first place to look when something fails silently.

---

## 20. System Health

Monitor the server hosting the platform:

- **Status** (healthy/unhealthy — includes a DB check and Telegram connection check)
- **CPU %**
- **Memory %**
- **Disk %**
- **Version**, **platform**, and **Python** version

The health endpoint is available at `GET /health` (configurable via `HEALTH_CHECK_PATH`).

**Practical tips:**
- If disk is high, purge old media/backups (or increase `STORAGE_MAX_SIZE`).
- Use the exported health JSON with an external uptime monitor.

---

## 21. Settings & Themes

The **Settings** page is where connection and appearance are configured.

### Telegram Connection
- **API ID** / **API Hash** / **Phone** → **Save & Connect**
- On success the connection status turns green.

### Theme & Language
- **Theme:** Dark / Light (colors defined by CSS variables; dark is default)
- **Language:** English (en) / فارسی (فرسی / fa, full RTL support)

Both choices persist to `localStorage` and apply instantly.

Back-end theme/language preferences are also stored per user (`User.theme`, `User.language`).

---

## 22. AI Chat Automation (Trending)

> ⭐ **New trending feature** — mirrors Telegram's native *Chat Automation* (Settings > Chat Automation) where a connected AI responds to messages on your behalf, 24/7.

The **Chat Automation** service builds a fully AI-driven auto-responder profile for your account.

### API surface (`/api/automation/chat-automation`)

| Endpoint | Purpose |
|---|---|
| `POST /setup` | Configure a responder profile |
| `POST /toggle/{user_id}` | Enable/disable |
| `GET /log/{user_id}?limit=` | Recent AI responses |

### What you can configure on setup

| Field | Description |
|---|---|
| `ai_provider` | `openai`, `gemini`, `deepseek`, `local` |
| `ai_model` | e.g. `gpt-3.5-turbo` |
| `api_key` | Provider key |
| `system_prompt` | Custom system prompt (overrides personality) |
| `allowed_chats` | `all` or a target chat scope |
| `excluded_chats` | Chat IDs to never respond in |
| `max_responses_per_day` | Daily quota (default 100) |
| `response_delay_min` / `response_delay_max` | Random delay between messages (2–10s default) |
| `working_hours_start` / `end` | Only work during a window |
| `language` | `auto` / specific language |
| `personality` | `friendly`, `professional`, `casual`, `sales`, `support` |

The service won't respond to your own messages, respects excluded chats, honors daily caps, and respects working hours. A full response log is kept per user.

### Quick example (curl)

```bash
curl -X POST http://localhost:8000/api/automation/chat-automation/setup \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "ai_provider": "openai",
    "ai_model": "gpt-3.5-turbo",
    "api_key": "sk-...",
    "personality": "friendly",
    "max_responses_per_day": 50,
    "working_hours_start": 9,
    "working_hours_end": 21
  }'
```

> **Tip:** Combine chat automation with Account Warming on new accounts — automation gives presence and activity while warming builds a safe usage ramp.

---

## 23. Account Warming (Trending)

> ⭐ **New trending feature** — gradually increase account activity to avoid Telegram restrictions. Essential for **new accounts** or accounts that have been inactive for a long time.

### How it works

The warming engine simulates **natural human activity patterns**: periodic online hours, typing, reading messages, viewing stories, scrolling the feed, sending occasional messages — with **randomized delays** and **daily caps**.

### Warming levels

| Level | Actions/hour | Messages/day | Joins/day | Online window |
|---|---|---|---|---|
| `beginner` | 5 | 20 | 2 | 10:00–14:00 |
| `intermediate` | 15 | 80 | 5 | 08:00–22:00 |
| `advanced` | 30 | 200 | 10 | 07:00–23:00 |
| `expert` | 60 | 500 | 20 | 06:00–24:00 |

When you start warming you pick a **level** and a **duration** (default 14 days). The service schedules automatic **level-ups** (beginner → intermediate → advanced → expert) across the duration.

### API surface (`/api/automation/warming`)

| Endpoint | Purpose |
|---|---|
| `POST /start` | Start warming (`level`, `duration_days`) |
| `GET /status/{user_id}` | Current quotas/counters/level plan |
| `POST /stop/{user_id}` | Stop warming |
| `GET /levels` | List all level configs |

### Practical tips
- **New account:** start at `beginner` for 14 days and let it level up automatically.
- **Warmed account:** jump to `intermediate`/`advanced`.
- Always keep `TELEGRAM_FLOOD_WAIT_ENABLED=true` and the platform's rate limiters enabled — they prevent the warming engine from tripping FloodWait.

---

## 24. Neuro Dialogs (Trending)

> ⭐ **New trending feature** — context-aware, *personality-driven* AI conversations that feel natural and human-like in real chats.

Neuro Dialogs create a persistent **conversation session** with a specific contact/chat. The AI keeps a rolling **context window**, remembers who is who, and replies without being robotic.

### Personalities built in

| Personality | Style |
|---|---|
| `natural` | Conversational, contractions, occasional emojis |
| `sales` | Enthusiastic, benefit-focused, objection handling |
| `support` | Patient, solution-oriented, follow-up |
| `bilingual_fa` | Fluent Persian + English, matches user's language |
| `bilingual_ar` | Fluent Arabic + English |

You can also supply a **custom system prompt** and adjust the **context window** (default 10 messages).

### API surface (`/api/automation/neuro-dialog`)

| Endpoint | Purpose |
|---|---|
| `POST /create` | Create a session (chat_id, provider, model, personality…) |
| `GET /templates` | List saved prompt templates |

### Example: natural Persian/English sales conversation

```bash
curl -X POST http://localhost:8000/api/automation/neuro-dialog/create \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{
    "chat_id": 120000001,
    "ai_provider": "openai",
    "personality": "bilingual_fa",
    "context_window": 12
  }'
```

The session maintains history automatically and trims old messages to the context window as the conversation grows.

---

## 25. Smart Forward (Trending)

> ⭐ **New trending feature** — forward messages between chats selectively, with **filters** and **content transformation**.

A **Smart Forward rule** watches a **source chat** and forwards qualifying messages to one or more **target chats**.

### Filters

| Filter | Behavior |
|---|---|
| `keywords` | Forward only if message contains one of these |
| `exclude_keywords` | Skip if message contains any of these |
| `min_length` | Forward only messages at least N characters |
| `sender_whitelist` | Forward only from these sender IDs |

### Transformations

| Transform | Behavior |
|---|---|
| `prefix` | Prepend text to the forwarded message |
| `suffix` | Append text |
| `remove_forwarded` | Strip "Forwarded from:" markers |

### API surface (`/api/automation/smart-forward`)

| Endpoint | Purpose |
|---|---|
| `POST /create` | Create a rule (name, source, targets, filters, transform) |
| `GET /rules` | List all rules |
| *(delete via service)* | Remove a rule |

### Example: forward price-drop alerts, prefixing your brand

```bash
curl -X POST http://localhost:8000/api/automation/smart-forward/create \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{
    "name": "Deals to team",
    "source_chat": -1001000000001,
    "target_chats": [-1001000000002],
    "filters": { "keywords": ["discount", "deal", "-50%"] },
    "transform": { "prefix": "[DEALS]", "remove_forwarded": true }
  }'
```

---

## 26. Multi-Account Management (Trending)

> ⭐ **New trending feature** — manage **multiple Telegram accounts** from a single dashboard, each with its own API credentials and automation toggles.

### How it works

The **MultiAccountManager** keeps a registry of accounts:

- Each account has `name`, `api_id`, `api_hash`, `phone`, `notes`
- Per-account toggles for **auto-reply**, **warming**, and **chat automation**
- **Connected** / **active** status and `last_active` timestamp

### API surface (`/api/automation/multi-account`)

| Endpoint | Purpose |
|---|---|
| `POST /add` | Add an account (name, api_id, api_hash, phone, notes) |
| `GET /list` | List all accounts |
| `DELETE /{account_id}` | Remove an account |

### Related: User Parser

`UserParserService` parses and extracts user data from groups/channels (`parse_chat`), producing a `parse_id` you can fetch results with — useful for building target lists for Broadcasts.

**Practical tips:**
- Give accounts descriptive names so your warming/broadcast jobs are easy to reason about.
- Add accounts with **different API credentials**; keep notes about each account's purpose.

---

## 27. Keyboard Shortcuts

Global shortcuts save time on the dashboard:

| Shortcut | Action |
|---|---|
| `Ctrl/⌘ + K` | Jump to search (Search… in top bar) |
| `Ctrl/⌘ + S` | Save current form (when a form is focused) |
| `Esc` | Close open modal / cancel |
| `Ctrl/⌘ + F` | Browser in-page search (long tables) |
| `Sidebar ☰` (toggle button) | Collapse/expand navigation |
| `Ctrl/⌘ + R` | Refresh current section data |

*(Where a shortcut isn't bound by the app, the browser's native behavior applies. New shortcuts can be wired in the `TopBar`/`Sidebar` components as needed.)*

---

## Where to go next

- **Installation:** see [INSTALL.md](INSTALL.md)
- **Troubleshooting:** see [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- **Full feature & API reference:** see [docs/FEATURES.md](docs/FEATURES.md)
- **Architecture:** see [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- **Security hardening:** see [docs/SECURITY.md](docs/SECURITY.md)
- **Interactive API playground:** `http://localhost:8000/api/docs`