@echo off
echo ===================================
echo  Telegram Self-Bot Installer
echo ===================================

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found. Install Python 3.11+
    pause
    exit /b 1
)

python -m pip install --upgrade pip
python -m pip install -e ".[dev]"

if not exist .env copy .env.example .env
if not exist storage\media mkdir storage\media
if not exist storage\backups mkdir storage\backups
if not exist storage\logs mkdir storage\logs

echo.
echo ===================================
echo  Installation Complete!
echo ===================================
echo.
echo To start: python -m backend.app.main serve --reload
echo Dashboard: http://localhost:8000
echo API Docs:  http://localhost:8000/api/docs
echo.
pause
