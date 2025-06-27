"""
Insight Project - Unified AI Services API
Combines Form Reader, Money Reader, and PPT/PDF Reader services
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import uuid
import os
from typing import Dict, Any
import logging

# Import service modules
from .services.form_reader import form_reader_routes
from .services.money_reader import money_reader_routes
from .services.ppt_pdf_reader import ppt_pdf_reader_routes
from .models.schemas import HealthResponse, ServiceInfo

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Session storage
sessions: Dict[str, Dict[str, Any]] = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    logger.info("🚀 Starting Insight Project API...")

    # Startup
    logger.info("✅ All services initialized successfully")

    yield

    # Shutdown
    logger.info("📴 Shutting down Insight Project API...")
    sessions.clear()


# Create FastAPI application
app = FastAPI(
    title="🧠 Insight Project - AI Services",
    description="""
    Unified AI services platform combining:
    - 📋 Form Reader: AI-powered form analysis and data extraction
    - 💰 Money Reader: Currency detection and financial document analysis  
    - 📄 PPT/PDF Reader: Document analysis and content extraction
    
    Built with FastAPI, powered by Google Gemini AI
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include service routers with prefixes
app.include_router(
    form_reader_routes.router, prefix="/form-reader", tags=["📋 Form Reader"]
)

app.include_router(
    money_reader_routes.router, prefix="/money-reader", tags=["💰 Money Reader"]
)

app.include_router(
    ppt_pdf_reader_routes.router, prefix="/ppt-pdf-reader", tags=["📄 PPT/PDF Reader"]
)


@app.get("/", response_model=Dict[str, Any])
async def root():
    """Welcome endpoint with service information"""
    return {
        "message": "🧠 Welcome to Insight Project - AI Services Platform",
        "description": "Unified platform for AI-powered document and image analysis",
        "version": "1.0.0",
        "services": {
            "form_reader": {
                "name": "📋 Form Reader",
                "description": "AI-powered form analysis and data extraction",
                "endpoints": "/form-reader/docs",
            },
            "money_reader": {
                "name": "💰 Money Reader",
                "description": "Currency detection and financial document analysis",
                "endpoints": "/money-reader/docs",
            },
            "ppt_pdf_reader": {
                "name": "📄 PPT/PDF Reader",
                "description": "Document analysis and content extraction",
                "endpoints": "/ppt-pdf-reader/docs",
            },
        },
        "documentation": {"interactive_docs": "/docs", "redoc": "/redoc"},
        "status": "active",
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Comprehensive health check for all services"""

    # Check each service health
    services_status = {}

    try:
        # Form Reader health
        from .services.form_reader.gemini import gemini_service

        services_status["form_reader"] = {
            "status": "healthy",
            "ai_service": "available" if gemini_service else "unavailable",
        }
    except Exception as e:
        services_status["form_reader"] = {"status": "error", "error": str(e)}

    try:
        # Money Reader health
        from .services.money_reader.gemini import gemini_service

        services_status["money_reader"] = {
            "status": "healthy",
            "ai_service": "available" if gemini_service else "unavailable",
        }
    except Exception as e:
        services_status["money_reader"] = {"status": "error", "error": str(e)}

    try:
        # PPT/PDF Reader health
        from .services.ppt_pdf_reader.gemini_analyzer import GeminiAnalyzer

        analyzer = GeminiAnalyzer()
        services_status["ppt_pdf_reader"] = {
            "status": "healthy",
            "ai_service": "available" if analyzer else "unavailable",
        }
    except Exception as e:
        services_status["ppt_pdf_reader"] = {"status": "error", "error": str(e)}

    # Overall status
    all_healthy = all(
        service.get("status") == "healthy" for service in services_status.values()
    )

    return HealthResponse(
        status="healthy" if all_healthy else "degraded",
        message=(
            "All services operational" if all_healthy else "Some services have issues"
        ),
        services=services_status,
        total_sessions=len(sessions),
        api_version="1.0.0",
    )


@app.get("/services", response_model=Dict[str, ServiceInfo])
async def get_services_info():
    """Get detailed information about all available services"""
    return {
        "form_reader": ServiceInfo(
            name="Form Reader",
            description="AI-powered form analysis and data extraction using YOLO and Gemini AI",
            version="1.0.0",
            endpoints=[
                "/form-reader/upload-image",
                "/form-reader/analyze-boxes",
                "/form-reader/text-to-speech",
            ],
            capabilities=[
                "Form detection and analysis",
                "Text extraction from forms",
                "Checkbox and field detection",
                "Arabic and English support",
                "Voice output generation",
            ],
        ),
        "money_reader": ServiceInfo(
            name="Money Reader",
            description="Currency detection and financial document analysis",
            version="1.0.0",
            endpoints=["/money-reader/upload-image", "/money-reader/text-to-speech"],
            capabilities=[
                "Currency detection and counting",
                "Bill/coin recognition",
                "Financial document analysis",
                "Multi-currency support",
                "Voice output generation",
            ],
        ),
        "ppt_pdf_reader": ServiceInfo(
            name="PPT/PDF Reader",
            description="Document analysis and content extraction with AI insights",
            version="1.0.0",
            endpoints=[
                "/ppt-pdf-reader/upload-document",
                "/ppt-pdf-reader/document/{session_id}/page/{page_number}",
                "/ppt-pdf-reader/document/{session_id}/summary",
                "/ppt-pdf-reader/navigate",
                "/ppt-pdf-reader/text-to-speech",
            ],
            capabilities=[
                "PowerPoint and PDF processing",
                "Page-by-page analysis",
                "Content summarization",
                "Voice navigation",
                "Multi-language support",
                "Image extraction",
            ],
        ),
    }


# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code,
            "timestamp": str(uuid.uuid4()),
        },
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": "An unexpected error occurred",
            "timestamp": str(uuid.uuid4()),
        },
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app", host="0.0.0.0", port=int(os.getenv("PORT", 8000)), reload=True
    )
