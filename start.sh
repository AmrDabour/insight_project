#!/bin/bash

# Insight Project - Startup Script for Linux/Mac
# Unified AI Services Platform

echo "🚀 Starting Insight Project - AI Services Platform"
echo "=================================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 --version | cut -d ' ' -f 2 | cut -d '.' -f 1,2)
REQUIRED_VERSION="3.8"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo "❌ Python 3.8 or higher is required. Current version: $PYTHON_VERSION"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install/upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📚 Installing requirements..."
pip install -r requirements.txt

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p uploads temp app/models

# Set environment variables
export GOOGLE_AI_API_KEY=${GOOGLE_AI_API_KEY:-"AIzaSyABJCFK7ylhc6yd0v5qH-2HpCZlZrjoF-Q"}
export PORT=${PORT:-8000}
export HOST=${HOST:-"0.0.0.0"}
export PYTHONPATH=$(pwd)

# Display service information
echo ""
echo "🧠 Insight Project Services:"
echo "  📋 Form Reader    - AI-powered form analysis"
echo "  💰 Money Reader   - Currency detection" 
echo "  📄 PPT/PDF Reader - Document analysis"
echo ""
echo "🌐 API Documentation:"
echo "  Interactive Docs: http://localhost:$PORT/docs"
echo "  ReDoc:           http://localhost:$PORT/redoc"
echo "  Health Check:    http://localhost:$PORT/health"
echo ""

# Start the application
echo "🚀 Starting FastAPI server..."
echo "📡 Server running on: http://localhost:$PORT"
echo "🛑 Press Ctrl+C to stop"
echo ""

python -m uvicorn app.main:app --host "$HOST" --port "$PORT" --reload 