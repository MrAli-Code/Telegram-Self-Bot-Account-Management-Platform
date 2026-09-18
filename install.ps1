# Telegram Self-Bot Installation Script for Windows
$ErrorActionPreference = "Stop"

Write-Host "===================================" -ForegroundColor Cyan
Write-Host " Telegram Self-Bot Installer" -ForegroundColor Cyan
Write-Host "===================================" -ForegroundColor Cyan

$python = "python"
try { & $python --version 2>&1 | Out-Null } catch {
    $python = "python3"
    try { & $python --version 2>&1 | Out-Null } catch {
        Write-Host "ERROR: Python not found. Install Python 3.11+" -ForegroundColor Red
        exit 1
    }
}

Write-Host "Using: $(& $python --version)" -ForegroundColor Green

& $python -m pip install --upgrade pip
& $python -m pip install -e ".[dev,ai,media]"

if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "Created .env from .env.example" -ForegroundColor Yellow
}

New-Item -ItemType Directory -Path "storage\media" -Force | Out-Null
New-Item -ItemType Directory -Path "storage\backups" -Force | Out-Null
New-Item -ItemType Directory -Path "storage\logs" -Force | Out-Null

Write-Host ""
Write-Host "===================================" -ForegroundColor Green
Write-Host " Installation Complete!" -ForegroundColor Green
Write-Host "===================================" -ForegroundColor Green
Write-Host ""
Write-Host "To start:" -ForegroundColor Cyan
Write-Host "  $python -m backend.app.main serve --reload"
Write-Host ""
Write-Host "Dashboard: http://localhost:8000"
Write-Host "API Docs:  http://localhost:8000/api/docs"
Write-Host ""
