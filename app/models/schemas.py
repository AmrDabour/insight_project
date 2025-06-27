"""
Unified Pydantic schemas for Insight Project
Contains models for all services: Form Reader, Money Reader, PPT/PDF Reader
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


# ==================== COMMON SCHEMAS ====================


class HealthResponse(BaseModel):
    """Health check response"""

    status: str = Field(..., description="Overall service status")
    message: str = Field(..., description="Status message")
    services: Dict[str, Any] = Field(..., description="Individual service statuses")
    total_sessions: int = Field(..., description="Number of active sessions")
    api_version: str = Field(..., description="API version")


class ServiceInfo(BaseModel):
    """Service information model"""

    name: str = Field(..., description="Service name")
    description: str = Field(..., description="Service description")
    version: str = Field(..., description="Service version")
    endpoints: List[str] = Field(..., description="Available endpoints")
    capabilities: List[str] = Field(..., description="Service capabilities")


class TTSRequest(BaseModel):
    """Text-to-speech request"""

    text: str = Field(..., description="Text to convert to speech")
    language: str = Field(default="ar", description="Language code (ar/en)")


class TTSResponse(BaseModel):
    """Text-to-speech response"""

    audio_base64: str = Field(..., description="Base64 encoded audio")
    language: str = Field(..., description="Audio language")
    duration: Optional[float] = Field(None, description="Audio duration in seconds")


# ==================== FORM READER SCHEMAS ====================


class BoxDetection(BaseModel):
    """Box detection result"""

    x: int = Field(..., description="X coordinate")
    y: int = Field(..., description="Y coordinate")
    width: int = Field(..., description="Box width")
    height: int = Field(..., description="Box height")
    confidence: float = Field(..., description="Detection confidence")
    class_name: str = Field(..., description="Detected class")


class TextExtraction(BaseModel):
    """Text extraction result"""

    text: str = Field(..., description="Extracted text")
    confidence: float = Field(..., description="OCR confidence")
    box: BoxDetection = Field(..., description="Text bounding box")


class FormField(BaseModel):
    """Form field model"""

    field_type: str = Field(..., description="Type of field (text, checkbox, etc.)")
    label: Optional[str] = Field(None, description="Field label")
    value: Optional[str] = Field(None, description="Field value")
    box: BoxDetection = Field(..., description="Field bounding box")
    confidence: float = Field(..., description="Field confidence")


class FormAnalysisRequest(BaseModel):
    """Form analysis request"""

    language: str = Field(default="ar", description="Analysis language (ar/en)")
    include_boxes: bool = Field(default=True, description="Include bounding boxes")
    extract_text: bool = Field(default=True, description="Extract text from fields")


class FormAnalysisResponse(BaseModel):
    """Form analysis response"""

    form_fields: List[FormField] = Field(..., description="Detected form fields")
    extracted_text: List[TextExtraction] = Field(..., description="All extracted text")
    total_boxes: int = Field(..., description="Total detected boxes")
    analysis_language: str = Field(..., description="Analysis language used")
    image_info: Dict[str, Any] = Field(..., description="Image metadata")
    ai_explanation: str = Field(..., description="AI analysis of the form")


# ==================== MONEY READER SCHEMAS ====================


class CurrencyDetection(BaseModel):
    """Currency detection result"""

    currency_type: str = Field(..., description="Type of currency (bill/coin)")
    denomination: str = Field(..., description="Currency denomination")
    currency_code: str = Field(..., description="Currency code (USD, SAR, etc.)")
    confidence: float = Field(..., description="Detection confidence")
    box: Optional[BoxDetection] = Field(None, description="Currency bounding box")


class MoneyAnalysisResponse(BaseModel):
    """Money analysis response"""

    detected_currencies: List[CurrencyDetection] = Field(
        ..., description="Detected currencies"
    )
    total_amount: Dict[str, float] = Field(..., description="Total amount per currency")
    currency_count: Dict[str, int] = Field(..., description="Count per currency type")
    analysis_language: str = Field(..., description="Analysis language")
    ai_explanation: str = Field(..., description="AI analysis of the money")
    image_info: Dict[str, Any] = Field(..., description="Image metadata")


class MoneyAnalysisRequest(BaseModel):
    """Money analysis request"""

    language: str = Field(default="ar", description="Analysis language (ar/en)")
    detect_bills: bool = Field(default=True, description="Detect paper bills")
    detect_coins: bool = Field(default=True, description="Detect coins")


# ==================== PPT/PDF READER SCHEMAS ====================


class PageContent(BaseModel):
    """Page content model"""

    page_number: int = Field(..., description="Page number")
    title: str = Field(..., description="Page title")
    text: str = Field(..., description="Extracted text")
    image_base64: Optional[str] = Field(None, description="Page image as base64")
    notes: Optional[str] = Field(None, description="Additional notes")


class SlideAnalysis(BaseModel):
    """Slide analysis model"""

    slide_number: int = Field(..., description="Slide number")
    title: str = Field(..., description="Slide title")
    slide_type: str = Field(..., description="Type of slide")
    importance_level: str = Field(..., description="Importance level")
    key_points: List[str] = Field(..., description="Key points from slide")
    explanation: str = Field(..., description="AI explanation")
    original_text: str = Field(..., description="Original extracted text")


class DocumentUploadResponse(BaseModel):
    """Document upload response"""

    session_id: str = Field(..., description="Session ID")
    filename: str = Field(..., description="Uploaded filename")
    file_type: str = Field(..., description="File type")
    total_pages: int = Field(..., description="Total number of pages")
    analysis_language: str = Field(..., description="Analysis language")
    message: str = Field(..., description="Success message")


class DocumentSummary(BaseModel):
    """Document summary model"""

    total_pages: int = Field(..., description="Total pages")
    language: str = Field(..., description="Document language")
    presentation_summary: str = Field(..., description="Overall summary")
    slides_analysis: List[SlideAnalysis] = Field(
        ..., description="Individual slide analyses"
    )


class NavigationRequest(BaseModel):
    """Navigation request"""

    session_id: str = Field(..., description="Session ID")
    command: str = Field(..., description="Navigation command")
    language: str = Field(default="ar", description="Command language")


class NavigationResponse(BaseModel):
    """Navigation response"""

    success: bool = Field(..., description="Navigation success")
    current_page: int = Field(..., description="Current page number")
    total_pages: int = Field(..., description="Total pages")
    message: str = Field(..., description="Navigation result message")


class DocumentAnalysisRequest(BaseModel):
    """Document analysis request"""

    language: str = Field(default="ar", description="Analysis language (ar/en)")
    extract_images: bool = Field(default=True, description="Extract page images")
    analyze_content: bool = Field(default=True, description="Analyze content with AI")


# ==================== ERROR SCHEMAS ====================


class ErrorResponse(BaseModel):
    """Error response model"""

    error: str = Field(..., description="Error message")
    status_code: int = Field(..., description="HTTP status code")
    timestamp: str = Field(..., description="Error timestamp")
    details: Optional[Dict[str, Any]] = Field(
        None, description="Additional error details"
    )


class ValidationError(BaseModel):
    """Validation error model"""

    field: str = Field(..., description="Field with validation error")
    message: str = Field(..., description="Validation error message")
    value: Any = Field(..., description="Invalid value")


# ==================== SESSION SCHEMAS ====================


class SessionInfo(BaseModel):
    """Session information"""

    session_id: str = Field(..., description="Session ID")
    service_type: str = Field(..., description="Service type")
    created_at: datetime = Field(..., description="Session creation time")
    last_accessed: datetime = Field(..., description="Last access time")
    file_info: Optional[Dict[str, Any]] = Field(None, description="File information")
    analysis_data: Optional[Dict[str, Any]] = Field(None, description="Analysis data")


class SessionListResponse(BaseModel):
    """Session list response"""

    sessions: List[SessionInfo] = Field(..., description="Active sessions")
    total_count: int = Field(..., description="Total session count")
    page: int = Field(default=1, description="Current page")
    per_page: int = Field(default=10, description="Items per page")


# ==================== UTILITY SCHEMAS ====================


class ImageInfo(BaseModel):
    """Image information"""

    width: int = Field(..., description="Image width")
    height: int = Field(..., description="Image height")
    format: str = Field(..., description="Image format")
    size_bytes: int = Field(..., description="Image size in bytes")
    channels: int = Field(..., description="Number of channels")


class ProcessingStats(BaseModel):
    """Processing statistics"""

    processing_time: float = Field(..., description="Processing time in seconds")
    memory_used: Optional[float] = Field(None, description="Memory used in MB")
    model_version: Optional[str] = Field(None, description="Model version used")
    confidence_score: Optional[float] = Field(None, description="Overall confidence")
