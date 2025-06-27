# Insight Project - Unified Docker Container
# Combines Form Reader, Money Reader, and PPT/PDF Reader services

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies for all services
RUN apt-get update && apt-get install -y \
    # OCR dependencies (for form_reader)
    tesseract-ocr \
    tesseract-ocr-ara \
    tesseract-ocr-eng \
    libtesseract-dev \
    # Image processing dependencies
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    # Audio processing dependencies
    libsndfile1 \
    ffmpeg \
    # System utilities
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ ./app/
COPY test/ ./test/

# Create necessary directories
RUN mkdir -p uploads temp app/models

# Set environment variables
ENV PYTHONPATH=/app
ENV GOOGLE_AI_API_KEY=AIzaSyABJCFK7ylhc6yd0v5qH-2HpCZlZrjoF-Q
ENV PORT=8000
ENV HOST=0.0.0.0

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the application
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"] 