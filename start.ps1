# Insight Project - Startup Script for Windows PowerShell
# Unified AI Services Platform

Write-Host "🚀 Starting Insight Project - AI Services Platform" -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Green

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Python is not installed or not in PATH. Please install Python 3.8 or higher." -ForegroundColor Red
        exit 1
    }
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
}
catch {
    Write-Host "❌ Python is not installed. Please install Python 3.8 or higher." -ForegroundColor Red
    exit 1
}

# Create virtual environment if it doesn't exist
if (!(Test-Path "venv")) {
    Write-Host "📦 Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
}

# Activate virtual environment
Write-Host "🔧 Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

# Install/upgrade pip
Write-Host "⬆️ Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

# Install requirements
Write-Host "📚 Installing requirements..." -ForegroundColor Yellow
pip install -r requirements.txt

# Create necessary directories
Write-Host "📁 Creating necessary directories..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path "uploads" | Out-Null
New-Item -ItemType Directory -Force -Path "temp" | Out-Null
New-Item -ItemType Directory -Force -Path "app\models" | Out-Null

# Set environment variables
if (!$env:GOOGLE_AI_API_KEY) {
    $env:GOOGLE_AI_API_KEY = "AIzaSyABJCFK7ylhc6yd0v5qH-2HpCZlZrjoF-Q"
}
if (!$env:PORT) {
    $env:PORT = "8000"
}
if (!$env:HOST) {
    $env:HOST = "0.0.0.0"
}
$env:PYTHONPATH = Get-Location

# Display service information
Write-Host ""
Write-Host "🧠 Insight Project Services:" -ForegroundColor Cyan
Write-Host "  📋 Form Reader    - AI-powered form analysis" -ForegroundColor White
Write-Host "  💰 Money Reader   - Currency detection" -ForegroundColor White
Write-Host "  📄 PPT/PDF Reader - Document analysis" -ForegroundColor White
Write-Host ""
Write-Host "🌐 API Documentation:" -ForegroundColor Cyan
Write-Host "  Interactive Docs: http://localhost:$($env:PORT)/docs" -ForegroundColor White
Write-Host "  ReDoc:           http://localhost:$($env:PORT)/redoc" -ForegroundColor White
Write-Host "  Health Check:    http://localhost:$($env:PORT)/health" -ForegroundColor White
Write-Host ""

# Start the application
Write-Host "🚀 Starting FastAPI server..." -ForegroundColor Green
Write-Host "📡 Server running on: http://localhost:$($env:PORT)" -ForegroundColor Green
Write-Host "🛑 Press Ctrl+C to stop" -ForegroundColor Yellow
Write-Host ""

# Start with error handling
try {
    python -m uvicorn app.main:app --host $env:HOST --port $env:PORT --reload
}
catch {
    Write-Host "❌ Failed to start server: $_" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
} 