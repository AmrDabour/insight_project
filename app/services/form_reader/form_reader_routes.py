"""
Form Reader API Routes
FastAPI routes for form analysis and data extraction
"""

from fastapi import APIRouter, File, UploadFile, HTTPException, Form
import logging

from ...models.schemas import FormAnalysisResponse, TTSRequest, TTSResponse

# Import form reader services
from .gemini import gemini_service
from .yolo import YoloService
from .ocr import OCRService
from .image import ImageProcessor
from .speech import SpeechService

logger = logging.getLogger(__name__)

# Initialize router
router = APIRouter()

# Initialize services
try:
    yolo_service = YoloService()
    ocr_service = OCRService()
    image_processor = ImageProcessor()
    speech_service = SpeechService()
    FORM_READER_AVAILABLE = True
except Exception as e:
    logger.error(f"Failed to initialize form reader services: {e}")
    FORM_READER_AVAILABLE = False


@router.get("/")
async def form_reader_info():
    """Get form reader service information"""
    return {
        "service": "Form Reader",
        "description": "AI-powered form analysis and data extraction",
        "version": "1.0.0",
        "status": "available" if FORM_READER_AVAILABLE else "unavailable",
        "capabilities": [
            "Form detection and analysis",
            "Text extraction from forms",
            "Checkbox and field detection",
            "Arabic and English support",
            "Voice output generation",
        ],
    }


@router.get("/health")
async def form_reader_health():
    """Health check for form reader service"""
    health_status = {
        "service": "form_reader",
        "status": "healthy" if FORM_READER_AVAILABLE else "unhealthy",
        "components": {
            "yolo_service": (
                "available" if "yolo_service" in globals() else "unavailable"
            ),
            "ocr_service": "available" if "ocr_service" in globals() else "unavailable",
            "gemini_service": "available" if gemini_service else "unavailable",
            "speech_service": (
                "available" if "speech_service" in globals() else "unavailable"
            ),
        },
    }
    return health_status


@router.post("/upload-image", response_model=FormAnalysisResponse)
async def upload_and_analyze_form(
    file: UploadFile = File(...),
    language: str = Form(default="ar"),
    include_boxes: bool = Form(default=True),
    extract_text: bool = Form(default=True),
):
    """
    Upload and analyze form image
    """
    if not FORM_READER_AVAILABLE:
        raise HTTPException(
            status_code=503, detail="Form reader service is not available"
        )

    try:
        # Validate file type
        if not file.content_type or not file.content_type.startswith("image/"):
            raise HTTPException(
                status_code=400,
                detail="Invalid file type. Please upload an image file.",
            )

        # Read file content
        file_content = await file.read()

        # Process image
        processed_image = image_processor.process_image(file_content)

        # Detect boxes with YOLO
        box_detections = []
        if include_boxes:
            detections = yolo_service.detect_boxes(processed_image)
            box_detections = [
                {
                    "x": det["x"],
                    "y": det["y"],
                    "width": det["width"],
                    "height": det["height"],
                    "confidence": det["confidence"],
                    "class_name": det["class_name"],
                }
                for det in detections
            ]

        # Extract text with OCR
        text_extractions = []
        if extract_text:
            ocr_results = ocr_service.extract_text(processed_image, language)
            text_extractions = [
                {
                    "text": result["text"],
                    "confidence": result["confidence"],
                    "box": {
                        "x": result["box"]["x"],
                        "y": result["box"]["y"],
                        "width": result["box"]["width"],
                        "height": result["box"]["height"],
                        "confidence": result["confidence"],
                        "class_name": "text",
                    },
                }
                for result in ocr_results
            ]

        # Create form fields from detections
        form_fields = []
        for detection in box_detections:
            form_field = {
                "field_type": detection["class_name"],
                "label": None,
                "value": None,
                "box": detection,
                "confidence": detection["confidence"],
            }

            # Try to find associated text
            for text in text_extractions:
                if _boxes_overlap(detection, text["box"]):
                    form_field["value"] = text["text"]
                    break

            form_fields.append(form_field)

        # Get AI explanation
        ai_explanation = ""
        if gemini_service:
            try:
                # Prepare context for AI analysis
                context = {
                    "total_boxes": len(box_detections),
                    "total_text_fields": len(text_extractions),
                    "form_fields": form_fields,
                    "language": language,
                }

                ai_explanation = gemini_service.analyze_form(
                    processed_image, context, language
                )
            except Exception as e:
                logger.warning(f"AI analysis failed: {e}")
                ai_explanation = "AI analysis not available"

        # Prepare response
        response = FormAnalysisResponse(
            form_fields=form_fields,
            extracted_text=text_extractions,
            total_boxes=len(box_detections),
            analysis_language=language,
            image_info={
                "width": processed_image.width,
                "height": processed_image.height,
                "format": processed_image.format or "Unknown",
                "size_bytes": len(file_content),
                "channels": len(processed_image.getbands()),
            },
            ai_explanation=ai_explanation,
        )

        return response

    except Exception as e:
        logger.error(f"Form analysis error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Form analysis failed: {str(e)}")


@router.post("/analyze-boxes")
async def analyze_boxes_only(
    file: UploadFile = File(...), language: str = Form(default="ar")
):
    """
    Analyze only the boxes/fields in a form (no text extraction)
    """
    if not FORM_READER_AVAILABLE:
        raise HTTPException(
            status_code=503, detail="Form reader service is not available"
        )

    try:
        # Read and process image
        file_content = await file.read()
        processed_image = image_processor.process_image(file_content)

        # Detect boxes only
        detections = yolo_service.detect_boxes(processed_image)

        # Get AI analysis of the form structure
        ai_explanation = ""
        if gemini_service:
            try:
                context = {
                    "total_boxes": len(detections),
                    "analysis_type": "boxes_only",
                    "language": language,
                }
                ai_explanation = gemini_service.analyze_form_structure(
                    processed_image, detections, language
                )
            except Exception as e:
                logger.warning(f"AI analysis failed: {e}")

        return {
            "detections": detections,
            "total_boxes": len(detections),
            "analysis_language": language,
            "ai_explanation": ai_explanation,
            "image_info": {
                "width": processed_image.width,
                "height": processed_image.height,
                "format": processed_image.format or "Unknown",
            },
        }

    except Exception as e:
        logger.error(f"Box analysis error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Box analysis failed: {str(e)}")


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


def _boxes_overlap(box1: dict, box2: dict, threshold: float = 0.1) -> bool:
    """
    Check if two boxes overlap significantly
    """
    try:
        # Calculate overlap area
        x1_overlap = max(box1["x"], box2["x"])
        y1_overlap = max(box1["y"], box2["y"])
        x2_overlap = min(box1["x"] + box1["width"], box2["x"] + box2["width"])
        y2_overlap = min(box1["y"] + box1["height"], box2["y"] + box2["height"])

        if x2_overlap <= x1_overlap or y2_overlap <= y1_overlap:
            return False

        overlap_area = (x2_overlap - x1_overlap) * (y2_overlap - y1_overlap)

        # Calculate areas
        box1_area = box1["width"] * box1["height"]
        box2_area = box2["width"] * box2["height"]

        # Check if overlap is significant
        overlap_ratio = overlap_area / min(box1_area, box2_area)
        return overlap_ratio > threshold

    except Exception:
        return False
