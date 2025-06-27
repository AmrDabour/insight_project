"""
Money Reader API Routes
FastAPI routes for currency detection and financial document analysis
"""

from fastapi import APIRouter, File, UploadFile, HTTPException, Form
import io
import logging
from PIL import Image

from ...models.schemas import MoneyAnalysisResponse, TTSRequest, TTSResponse

# Import money reader services
from .gemini import gemini_service
from .speech import SpeechService

logger = logging.getLogger(__name__)

# Initialize router
router = APIRouter()

# Initialize services
try:
    speech_service = SpeechService()
    MONEY_READER_AVAILABLE = True
except Exception as e:
    logger.error(f"Failed to initialize money reader services: {e}")
    MONEY_READER_AVAILABLE = False


@router.get("/")
async def money_reader_info():
    """Get money reader service information"""
    return {
        "service": "Money Reader",
        "description": "Currency detection and financial document analysis",
        "version": "1.0.0",
        "status": "available" if MONEY_READER_AVAILABLE else "unavailable",
        "capabilities": [
            "Currency detection and counting",
            "Bill/coin recognition",
            "Financial document analysis",
            "Multi-currency support",
            "Voice output generation",
        ],
    }


@router.get("/health")
async def money_reader_health():
    """Health check for money reader service"""
    health_status = {
        "service": "money_reader",
        "status": "healthy" if MONEY_READER_AVAILABLE else "unhealthy",
        "components": {
            "gemini_service": "available" if gemini_service else "unavailable",
            "speech_service": (
                "available" if "speech_service" in globals() else "unavailable"
            ),
        },
    }
    return health_status


@router.post("/upload-image", response_model=MoneyAnalysisResponse)
async def upload_and_analyze_money(
    file: UploadFile = File(...),
    language: str = Form(default="ar"),
    detect_bills: bool = Form(default=True),
    detect_coins: bool = Form(default=True),
):
    """
    Upload and analyze money image for currency detection
    """
    if not MONEY_READER_AVAILABLE:
        raise HTTPException(
            status_code=503, detail="Money reader service is not available"
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
        image = Image.open(io.BytesIO(file_content))
        if image.mode != "RGB":
            image = image.convert("RGB")

        # Analyze with Gemini AI
        detected_currencies = []
        total_amount = {}
        currency_count = {}
        ai_explanation = ""

        if gemini_service:
            try:
                # Create analysis request
                analysis_request = {
                    "detect_bills": detect_bills,
                    "detect_coins": detect_coins,
                    "language": language,
                    "image_info": {
                        "width": image.width,
                        "height": image.height,
                        "format": image.format or "Unknown",
                    },
                }

                # Get AI analysis
                analysis_result = gemini_service.analyze_money(
                    image, analysis_request, language
                )

                # Parse results
                detected_currencies = analysis_result.get("detected_currencies", [])
                total_amount = analysis_result.get("total_amount", {})
                currency_count = analysis_result.get("currency_count", {})
                ai_explanation = analysis_result.get("explanation", "")

            except Exception as e:
                logger.warning(f"AI analysis failed: {e}")
                ai_explanation = "AI analysis not available"
        else:
            ai_explanation = "AI service not available"

        # Prepare response
        response = MoneyAnalysisResponse(
            detected_currencies=detected_currencies,
            total_amount=total_amount,
            currency_count=currency_count,
            analysis_language=language,
            ai_explanation=ai_explanation,
            image_info={
                "width": image.width,
                "height": image.height,
                "format": image.format or "Unknown",
                "size_bytes": len(file_content),
                "channels": len(image.getbands()),
            },
        )

        return response

    except Exception as e:
        logger.error(f"Money analysis error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Money analysis failed: {str(e)}")


@router.post("/analyze-currency")
async def analyze_currency_only(
    file: UploadFile = File(...),
    currency_type: str = Form(default="all"),  # bills, coins, all
    language: str = Form(default="ar"),
):
    """
    Analyze specific type of currency in the image
    """
    if not MONEY_READER_AVAILABLE:
        raise HTTPException(
            status_code=503, detail="Money reader service is not available"
        )

    try:
        # Read and process image
        file_content = await file.read()
        image = Image.open(io.BytesIO(file_content))
        if image.mode != "RGB":
            image = image.convert("RGB")

        # Set detection flags based on currency type
        detect_bills = currency_type in ["bills", "all"]
        detect_coins = currency_type in ["coins", "all"]

        # Analyze with AI
        analysis_result = {}
        if gemini_service:
            try:
                analysis_request = {
                    "detect_bills": detect_bills,
                    "detect_coins": detect_coins,
                    "currency_focus": currency_type,
                    "language": language,
                }

                analysis_result = gemini_service.analyze_currency_type(
                    image, analysis_request, language
                )
            except Exception as e:
                logger.warning(f"Currency analysis failed: {e}")

        return {
            "currency_type_analyzed": currency_type,
            "detections": analysis_result.get("detections", []),
            "analysis_summary": analysis_result.get("summary", ""),
            "confidence_score": analysis_result.get("confidence", 0.0),
            "analysis_language": language,
            "image_info": {
                "width": image.width,
                "height": image.height,
                "format": image.format or "Unknown",
            },
        }

    except Exception as e:
        logger.error(f"Currency analysis error: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Currency analysis failed: {str(e)}"
        )


@router.post("/count-money")
async def count_money_total(
    file: UploadFile = File(...),
    target_currency: str = Form(default="all"),  # USD, SAR, EUR, etc.
    language: str = Form(default="ar"),
):
    """
    Count total money amount in the image
    """
    if not MONEY_READER_AVAILABLE:
        raise HTTPException(
            status_code=503, detail="Money reader service is not available"
        )

    try:
        # Read and process image
        file_content = await file.read()
        image = Image.open(io.BytesIO(file_content))
        if image.mode != "RGB":
            image = image.convert("RGB")

        # Count money with AI
        counting_result = {}
        if gemini_service:
            try:
                counting_request = {
                    "target_currency": target_currency,
                    "language": language,
                    "count_focus": True,
                }

                counting_result = gemini_service.count_money(
                    image, counting_request, language
                )
            except Exception as e:
                logger.warning(f"Money counting failed: {e}")

        return {
            "target_currency": target_currency,
            "total_count": counting_result.get("total_count", {}),
            "denomination_breakdown": counting_result.get("breakdown", {}),
            "confidence_score": counting_result.get("confidence", 0.0),
            "counting_explanation": counting_result.get("explanation", ""),
            "analysis_language": language,
        }

    except Exception as e:
        logger.error(f"Money counting error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Money counting failed: {str(e)}")


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


@router.get("/supported-currencies")
async def get_supported_currencies():
    """
    Get list of supported currencies
    """
    return {
        "supported_currencies": [
            {"code": "USD", "name": "US Dollar", "symbol": "$"},
            {"code": "SAR", "name": "Saudi Riyal", "symbol": "ر.س"},
            {"code": "EUR", "name": "Euro", "symbol": "€"},
            {"code": "AED", "name": "UAE Dirham", "symbol": "د.إ"},
            {"code": "KWD", "name": "Kuwaiti Dinar", "symbol": "د.ك"},
            {"code": "QAR", "name": "Qatari Riyal", "symbol": "ر.ق"},
            {"code": "BHD", "name": "Bahraini Dinar", "symbol": "د.ب"},
            {"code": "OMR", "name": "Omani Rial", "symbol": "ر.ع"},
        ],
        "detection_capabilities": [
            "Paper bills",
            "Coins",
            "Mixed currency detection",
            "Denomination counting",
            "Total value calculation",
        ],
    }
