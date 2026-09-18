# Telegram Self-Bot Architecture

## System Overview

```
┌─────────────────────────────────────────────┐
│              Web Dashboard (Vue 3)           │
│         REST API + WebSocket (FastAPI)       │
├─────────────────────────────────────────────┤
│              Application Layer              │
│  ┌─────────┐ ┌──────────┐ ┌──────────────┐ │
│  │  Auth   │ │ Security │ │  Scheduler   │ │
│  │ Service │ │  Service │ │   Service    │ │
│  └─────────┘ └──────────┘ └──────────────┘ │
│  ┌─────────┐ ┌──────────┐ ┌──────────────┐ │
│  │  Auto   │ │  Media   │ │   Backup     │ │
│  │ Reply   │ │ Archive  │ │   Service    │ │
│  └─────────┘ └──────────┘ └──────────────┘ │
├─────────────────────────────────────────────┤
│              Telegram Engine                │
│  ┌────────────────────────────────────────┐ │
│  │           Telethon Client              │ │
│  │   MTProto | Session | Update Handler   │ │
│  └────────────────────────────────────────┘ │
├─────────────────────────────────────────────┤
│              Data Layer                     │
│  ┌─────────┐ ┌──────────┐ ┌──────────────┐ │
│  │  SQLite │ │  Redis   │ │   Storage    │ │
│  │  / PG   │ │  Cache   │ │   Files      │ │
│  └─────────┘ └──────────┘ └──────────────┘ │
├─────────────────────────────────────────────┤
│              Task Queue (Celery)            │
│  ┌─────────┐ ┌──────────┐ ┌──────────────┐ │
│  │ Worker  │ │  Beat    │ │   Broker     │ │
│  └─────────┘ └──────────┘ └──────────────┘ │
└─────────────────────────────────────────────┘
```

## Module Architecture

### Telegram Engine
- **Client**: Telethon-based MTProto client
- **Session Management**: Persistent session storage
- **Update Handler**: Real-time event processing
- **FloodWait Handler**: Automatic retry with backoff

### Core Services
- **Authentication**: JWT + refresh tokens
- **Security**: Encryption, CSRF, rate limiting
- **Anti-Abuse**: Rate limiting, emergency stop
- **Scheduler**: APScheduler + Celery Beat

### Data Layer
- **Database**: SQLAlchemy async (SQLite/PostgreSQL)
- **Cache**: Redis for sessions and queues
- **Storage**: File system for media and backups

### Frontend
- **Framework**: Vue 3 + TypeScript
- **State**: Pinia
- **Router**: Vue Router
- **i18n**: vue-i18n (EN/FA)
- **Charts**: Chart.js
- **Styling**: Custom CSS with themes

## Plugin System

Each plugin has:
- `manifest.json` - Plugin metadata
- `config.py` - Configuration
- `routes.py` - API routes (optional)
- `services.py` - Business logic
- `events.py` - Event handlers

## Security Architecture

1. JWT authentication with refresh tokens
2. Password hashing (bcrypt)
3. CSRF token protection
4. Rate limiting (per IP and global)
5. Input validation (Pydantic)
6. SQL injection prevention (SQLAlchemy ORM)
7. XSS protection (headers)
8. Audit logging
9. Emergency stop mechanism
10. Session encryption at rest
