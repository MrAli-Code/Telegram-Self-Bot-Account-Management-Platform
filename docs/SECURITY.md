# Security Guide

## Authentication

The platform uses JWT (JSON Web Token) authentication:
- Access tokens expire after 30 minutes
- Refresh tokens expire after 7 days
- Passwords are hashed with bcrypt

## Configuration

Set these in `.env`:
```
JWT_SECRET_KEY=<random-32-char-key>
ENCRYPTION_KEY=<random-32-byte-key>
CSRF_SECRET_KEY=<random-key>
```

## API Security

- All API endpoints require authentication (except login/register)
- Rate limiting: 30 requests per minute per IP
- CORS is restricted to configured origins
- Security headers are set on all responses

## Emergency Stop

The emergency stop mechanism immediately halts:
- All automation tasks
- Broadcast operations
- Scheduled tasks
- Auto-reply system
- Message repeaters

Access via: `POST /api/system/emergency-stop`

## Session Security

- Telegram session strings are encrypted at rest
- Sessions are never exposed in API responses
- Session tokens are stored server-side only

## Best Practices

1. Use strong, unique secrets
2. Enable 2FA for dashboard login
3. Regular backups with encryption
4. Monitor security events regularly
5. Use PostgreSQL for production
6. Run behind a reverse proxy (nginx)
7. Enable HTTPS in production
8. Review audit logs periodically
