# Telegram Self-Bot / Account Management Platform

A professional, modular, and production-ready Telegram Self-Bot and Account Management Platform.

## Features

- **Telegram Client** - Full MTProto client with session management
- **Message Archive** - Complete message history with search and export
- **Media Archive** - Photo, video, voice, document archiving with duplicate detection
- **Deleted Message Tracking** - Monitor deleted/changed messages
- **Story Archive** - Archive stories from contacts
- **Profile Monitor** - Track profile changes (name, username, bio)
- **Auto Reply Engine** - Rule-based auto-reply with multiple trigger types
- **Friend/Enemy System** - Categorize contacts with auto-actions
- **Group Management** - Anti-spam, anti-link, welcome system
- **Channel Management** - Post scheduling, admin management
- **Security Center** - Session monitoring, login alerts, audit logs
- **Backup System** - Full/partial backups with encryption
- **Scheduler** - Cron-based task scheduling
- **Broadcast** - Mass messaging with rate limiting
- **Message Repeater** - Scheduled message repetition
- **Statistics** - Comprehensive analytics dashboard
- **Media Converter** - Text-to-voice, video conversion
- **Workflow Builder** - Visual automation builder
- **AI Integration** - OpenAI, Gemini, DeepSeek support
- **Multi-language** - English and Persian (RTL) support
- **Dark/Light Theme** - Multiple theme support
- **WebSocket** - Real-time notifications
- **REST API** - Complete API with OpenAPI docs
- **Plugin System** - Modular plugin architecture
- **Docker** - Docker Compose ready
- **Security** - JWT auth, CSRF, rate limiting, audit logs

## Quick Start

### Prerequisites

- Python 3.11+
- FFmpeg (for media conversion)
- Redis (for task queue)

### Installation

**Linux/macOS:**
```bash
chmod +x install.sh
./install.sh
```

**Windows:**
```powershell
.\install.ps1
```

**Manual:**
```bash
pip install -e ".[dev]"
cp .env.example .env
# Edit .env with your Telegram API credentials
python -m backend.app.main serve --reload
```

### Docker

```bash
docker-compose up -d
```

## Configuration

Copy `.env.example` to `.env` and configure:

1. Get Telegram API credentials from https://my.telegram.org
2. Set `TELEGRAM_API_ID` and `TELEGRAM_API_HASH`
3. Set a secure `JWT_SECRET_KEY` and `ENCRYPTION_KEY`
4. Configure database (SQLite by default, PostgreSQL recommended for production)

## Usage

### Dashboard
Open http://localhost:8000 in your browser.

### API Documentation
Open http://localhost:8000/api/docs for Swagger UI.

### CLI Commands
```bash
# Start server
python -m backend.app.main serve --reload

# Run migrations
python -m backend.app.main migrate

# Create admin user
python -m backend.app.main init-admin
```

## Project Structure

```
project/
├── backend/          # FastAPI backend
│   └── app/
│       ├── api/      # REST API endpoints
│       ├── core/     # Database, security, logging
│       ├── models/   # SQLAlchemy models
│       ├── schemas/  # Pydantic schemas
│       ├── services/ # Business logic
│       └── middleware/
├── frontend/         # Vue 3 + Vite dashboard
│   └── src/
│       ├── views/    # Page components
│       ├── components/
│       ├── stores/   # Pinia stores
│       ├── router/   # Vue Router
│       └── i18n/     # Translations
├── worker/           # Celery workers
├── telegram/         # Telegram engine
├── plugins/          # Plugin system
├── migrations/       # Alembic migrations
├── tests/            # Test suite
├── scripts/          # Utility scripts
├── docker/           # Docker configs
├── docs/             # Documentation
├── storage/          # Data storage
├── config/           # Configuration
├── docker-compose.yml
├── Dockerfile
├── install.sh
├── install.ps1
└── pyproject.toml
```

## API Endpoints

| Endpoint | Description |
|----------|-------------|
| `POST /api/auth/register` | Register new user |
| `POST /api/auth/login` | Login |
| `GET /api/messages/` | List messages |
| `GET /api/media/` | List media |
| `GET /api/stories/` | List stories |
| `GET /api/autoreply/` | List auto-reply rules |
| `GET /api/friends/` | List friends |
| `GET /api/enemies/` | List enemies |
| `GET /api/groups/` | List groups |
| `GET /api/channels/` | List channels |
| `GET /api/security/events` | Security events |
| `GET /api/backups/` | List backups |
| `GET /api/scheduler/` | List scheduled tasks |
| `GET /api/statistics/account` | Account statistics |
| `POST /api/system/emergency-stop` | Emergency stop |
| `GET /api/system/health` | Health check |

## Security

- JWT-based authentication
- Password hashing with bcrypt
- CSRF protection
- Rate limiting
- Audit logging
- Session management
- Emergency stop functionality
- Encryption at rest for sensitive data

## License

MIT License
