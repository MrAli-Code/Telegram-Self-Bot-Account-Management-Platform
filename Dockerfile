FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml .
RUN pip install --no-cache-dir -e ".[dev]" 2>/dev/null || pip install --no-cache-dir fastapi uvicorn[standard] telethon sqlalchemy aiosqlite pydantic pydantic-settings python-jose[cryptography] passlib[bcrypt] python-multipart httpx aiofiles python-dotenv cryptography apscheduler structlog rich click redis celery[redis] python-dateutil

COPY . .

RUN mkdir -p storage/media storage/backups storage/logs

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD python -c "import httpx; httpx.get('http://localhost:8000/health')"

CMD ["python", "-m", "uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
