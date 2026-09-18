#!/bin/bash
set -e

echo "==================================="
echo " Telegram Self-Bot Installer"
echo "==================================="

PYTHON_CMD=""
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "ERROR: Python not found. Install Python 3.11+"
    exit 1
fi

echo "Using: $($PYTHON_CMD --version)"

$PYTHON_CMD -m pip install --upgrade pip
$PYTHON_CMD -m pip install -e ".[dev,ai,media]"

if ! command -v ffmpeg &> /dev/null; then
    echo "WARNING: FFmpeg not found. Media conversion features will be limited."
    echo "Install: sudo apt install ffmpeg"
fi

cp -n .env.example .env 2>/dev/null || true

mkdir -p storage/media storage/backups storage/logs

echo ""
echo "Running database migrations..."
$PYTHON_CMD -m backend.app.main migrate 2>/dev/null || echo "Migrations will run on first start"

echo ""
echo "Creating admin user..."
$PYTHON_CMD -m backend.app.main init-admin 2>/dev/null || echo "Admin user will be created on first start"

echo ""
echo "==================================="
echo " Installation Complete!"
echo "==================================="
echo ""
echo "To start:"
echo "  $PYTHON_CMD -m backend.app.main serve --reload"
echo ""
echo "Dashboard: http://localhost:8000"
echo "API Docs:  http://localhost:8000/api/docs"
echo ""
