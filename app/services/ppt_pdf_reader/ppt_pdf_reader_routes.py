"""
PPT/PDF Reader API Routes
FastAPI routes for document analysis and content extraction
"""

from fastapi import APIRouter, File, UploadFile, HTTPException, Form
from fastapi.responses import Response
from typing import Dict, Any
import uuid
import os
import logging
import base64

from ...models.schemas import (
    DocumentUploadResponse,
    DocumentSummary,
    SlideAnalysis,
    NavigationRequest,
    NavigationResponse,
    TTSRequest,
    TTSResponse,
)

# Import PPT/PDF reader services
from .document_processor import DocumentProcessor
from .gemini_analyzer import GeminiAnalyzer
from .speech import SpeechService

logger = logging.getLogger(__name__)

# Initialize router
router = APIRouter()

# Session storage for document data
sessions: Dict[str, Dict[str, Any]] = {}

# Initialize services
try:
    document_processor = DocumentProcessor()
    gemini_analyzer = GeminiAnalyzer()
    speech_service = SpeechService()
    PPT_PDF_READER_AVAILABLE = True
except Exception as e:
    logger.error(f"Failed to initialize PPT/PDF reader services: {e}")
    PPT_PDF_READER_AVAILABLE = False


@router.get("/")
async def ppt_pdf_reader_info():
    """Get PPT/PDF reader service information"""
    return {
        "service": "PPT/PDF Reader",
        "description": "Document analysis and content extraction with AI insights",
        "version": "1.0.0",
        "status": "available" if PPT_PDF_READER_AVAILABLE else "unavailable",
        "capabilities": [
            "PowerPoint and PDF processing",
            "Page-by-page analysis",
            "Content summarization",
            "Voice navigation",
            "Multi-language support",
            "Image extraction",
        ],
    }


@router.get("/health")
async def ppt_pdf_reader_health():
    """Health check for PPT/PDF reader service"""
    health_status = {
        "service": "ppt_pdf_reader",
        "status": "healthy" if PPT_PDF_READER_AVAILABLE else "unhealthy",
        "components": {
            "document_processor": (
                "available" if "document_processor" in globals() else "unavailable"
            ),
            "gemini_analyzer": (
                "available" if "gemini_analyzer" in globals() else "unavailable"
            ),
            "speech_service": (
                "available" if "speech_service" in globals() else "unavailable"
            ),
        },
    }
    return health_status


@router.post("/upload-document", response_model=DocumentUploadResponse)
async def upload_and_analyze_document(
    file: UploadFile = File(...),
    language: str = Form(default="ar"),
    extract_images: bool = Form(default=True),
    analyze_content: bool = Form(default=True),
):
    """
    Upload and analyze PowerPoint or PDF document
    """
    if not PPT_PDF_READER_AVAILABLE:
        raise HTTPException(
            status_code=503, detail="PPT/PDF reader service is not available"
        )

    try:
        # Validate file type
        if not file.filename:
            raise HTTPException(status_code=400, detail="No filename provided")

        file_extension = os.path.splitext(file.filename)[1].lower()
        if file_extension not in [".pptx", ".ppt", ".pdf"]:
            raise HTTPException(
                status_code=400,
                detail="Invalid file type. Please upload a PowerPoint (.pptx, .ppt) or PDF file.",
            )

        # Read file content
        file_content = await file.read()

        # Process document
        document_data = document_processor.process_document(
            file_content, file_extension
        )

        # Generate session ID
        session_id = str(uuid.uuid4())

        # Analyze content with AI if requested
        if analyze_content and gemini_analyzer:
            try:
                # Analyze each page/slide
                for page in document_data["pages"]:
                    analysis = gemini_analyzer.analyze_page(
                        page["text"], page["page_number"], language
                    )

                    # Add analysis to page data
                    page.update(
                        {
                            "slide_type": analysis.get("slide_type", "content"),
                            "importance_level": analysis.get(
                                "importance_level", "medium"
                            ),
                            "key_points": analysis.get("key_points", []),
                            "explanation": analysis.get("explanation", ""),
                            "title": analysis.get("title", page["title"]),
                        }
                    )

                # Generate document summary
                summary = gemini_analyzer.generate_summary(
                    document_data["pages"], language
                )
                document_data["summary"] = summary

            except Exception as e:
                logger.warning(f"AI analysis failed: {e}")
                # Add minimal analysis data
                for page in document_data["pages"]:
                    page.update(
                        {
                            "slide_type": "content",
                            "importance_level": "medium",
                            "key_points": [],
                            "explanation": "AI analysis not available",
                        }
                    )

        # Store session data
        sessions[session_id] = {
            "session_id": session_id,
            "filename": file.filename,
            "file_type": file_extension,
            "language": language,
            "document_data": document_data,
            "current_page": 1,
            "upload_time": str(uuid.uuid4()),  # Using uuid as timestamp placeholder
        }

        # Prepare response
        response = DocumentUploadResponse(
            session_id=session_id,
            filename=file.filename,
            file_type=file_extension,
            total_pages=document_data["total_pages"],
            analysis_language=language,
            message=f"Document uploaded and analyzed successfully. {document_data['total_pages']} pages processed.",
        )

        return response

    except Exception as e:
        logger.error(f"Document upload error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Document upload failed: {str(e)}")


@router.get("/document/{session_id}/page/{page_number}")
async def get_page_analysis(session_id: str, page_number: int):
    """
    Get analysis for a specific page/slide
    """
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    session_data = sessions[session_id]
    document_data = session_data["document_data"]

    if page_number < 1 or page_number > document_data["total_pages"]:
        raise HTTPException(status_code=400, detail="Invalid page number")

    # Get page data (pages are 0-indexed in storage)
    page_data = document_data["pages"][page_number - 1]

    # Update current page in session
    sessions[session_id]["current_page"] = page_number

    return {
        "session_id": session_id,
        "page_number": page_number,
        "title": page_data.get("title", f"Page {page_number}"),
        "slide_type": page_data.get("slide_type", "content"),
        "importance_level": page_data.get("importance_level", "medium"),
        "key_points": page_data.get("key_points", []),
        "explanation": page_data.get("explanation", ""),
        "original_text": page_data.get("text", ""),
        "has_image": bool(page_data.get("image_base64")),
    }


@router.get("/document/{session_id}/page/{page_number}/image")
async def get_page_image(session_id: str, page_number: int):
    """
    Get image for a specific page/slide
    """
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    session_data = sessions[session_id]
    document_data = session_data["document_data"]

    if page_number < 1 or page_number > document_data["total_pages"]:
        raise HTTPException(status_code=400, detail="Invalid page number")

    # Get page data
    page_data = document_data["pages"][page_number - 1]

    if not page_data.get("image_base64"):
        raise HTTPException(status_code=404, detail="No image available for this page")

    # Decode base64 image
    try:
        image_data = base64.b64decode(page_data["image_base64"])
        return Response(
            content=image_data,
            media_type="image/png",
            headers={"Content-Disposition": f"inline; filename=page_{page_number}.png"},
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load image: {str(e)}")


@router.get("/document/{session_id}/summary", response_model=DocumentSummary)
async def get_document_summary(session_id: str):
    """
    Get comprehensive document summary
    """
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    session_data = sessions[session_id]
    document_data = session_data["document_data"]

    # Prepare slides analysis
    slides_analysis = []
    for page in document_data["pages"]:
        slide_analysis = SlideAnalysis(
            slide_number=page["page_number"],
            title=page.get("title", f"Slide {page['page_number']}"),
            slide_type=page.get("slide_type", "content"),
            importance_level=page.get("importance_level", "medium"),
            key_points=page.get("key_points", []),
            explanation=page.get("explanation", ""),
            original_text=page.get("text", ""),
        )
        slides_analysis.append(slide_analysis)

    # Get summary
    summary_text = document_data.get("summary", {}).get(
        "presentation_summary", "Summary not available"
    )

    response = DocumentSummary(
        total_pages=document_data["total_pages"],
        language=session_data["language"],
        presentation_summary=summary_text,
        slides_analysis=slides_analysis,
    )

    return response


@router.post("/navigate", response_model=NavigationResponse)
async def navigate_document(request: NavigationRequest):
    """
    Process navigation commands
    """
    if request.session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    session_data = sessions[request.session_id]
    document_data = session_data["document_data"]
    current_page = session_data["current_page"]
    total_pages = document_data["total_pages"]

    # Process navigation command
    command = request.command.lower().strip()
    new_page = current_page
    success = False
    message = ""

    if command in ["next", "التالي", "التالية"]:
        if current_page < total_pages:
            new_page = current_page + 1
            success = True
            message = f"Moved to page {new_page}"
        else:
            message = "Already at last page"

    elif command in ["previous", "prev", "السابق", "السابقة"]:
        if current_page > 1:
            new_page = current_page - 1
            success = True
            message = f"Moved to page {new_page}"
        else:
            message = "Already at first page"

    elif command in ["first", "الأول", "البداية"]:
        new_page = 1
        success = True
        message = "Moved to first page"

    elif command in ["last", "الأخير", "النهاية"]:
        new_page = total_pages
        success = True
        message = "Moved to last page"

    else:
        # Try to parse as page number
        try:
            # Handle Arabic numerals and English
            page_num = int(command)
            if 1 <= page_num <= total_pages:
                new_page = page_num
                success = True
                message = f"Moved to page {new_page}"
            else:
                message = f"Invalid page number. Must be between 1 and {total_pages}"
        except ValueError:
            message = f"Unknown navigation command: {command}"

    # Update session if successful
    if success:
        sessions[request.session_id]["current_page"] = new_page

    return NavigationResponse(
        success=success, current_page=new_page, total_pages=total_pages, message=message
    )


@router.post("/text-to-speech")
async def text_to_speech(request: TTSRequest):
    """
    Convert text to speech
    """
    try:
        if not speech_service:
            raise HTTPException(
                status_code=503, detail="Text-to-speech service is not available"
            )

        # Generate audio
        audio_data = speech_service.text_to_speech(request.text, request.language)

        if not audio_data:
            raise HTTPException(status_code=500, detail="Failed to generate speech")

        return TTSResponse(audio_base64=audio_data, language=request.language)

    except Exception as e:
        logger.error(f"TTS error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Text-to-speech failed: {str(e)}")


@router.get("/sessions")
async def get_active_sessions():
    """
    Get list of active sessions
    """
    session_info = []
    for session_id, data in sessions.items():
        session_info.append(
            {
                "session_id": session_id,
                "filename": data.get("filename", "Unknown"),
                "file_type": data.get("file_type", "Unknown"),
                "total_pages": data.get("document_data", {}).get("total_pages", 0),
                "current_page": data.get("current_page", 1),
                "language": data.get("language", "ar"),
            }
        )

    return {"active_sessions": session_info, "total_sessions": len(sessions)}


@router.delete("/session/{session_id}")
async def delete_session(session_id: str):
    """
    Delete a session and free up memory
    """
    if session_id in sessions:
        del sessions[session_id]
        return {"message": f"Session {session_id} deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Session not found")


@router.get("/supported-formats")
async def get_supported_formats():
    """
    Get list of supported document formats
    """
    return {
        "supported_formats": [
            {
                "extension": ".pptx",
                "description": "PowerPoint Presentation (2007+)",
                "mime_types": [
                    "application/vnd.openxmlformats-officedocument.presentationml.presentation"
                ],
            },
            {
                "extension": ".ppt",
                "description": "PowerPoint Presentation (Legacy)",
                "mime_types": ["application/vnd.ms-powerpoint"],
            },
            {
                "extension": ".pdf",
                "description": "Portable Document Format",
                "mime_types": ["application/pdf"],
            },
        ],
        "processing_capabilities": [
            "Text extraction",
            "Image conversion",
            "AI content analysis",
            "Page navigation",
            "Content summarization",
            "Multi-language support",
        ],
    }
