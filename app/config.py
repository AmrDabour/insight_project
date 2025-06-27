"""
Configuration settings for Insight Project
Unified settings for all services: Form Reader, Money Reader, PPT/PDF Reader
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings"""

    # API Configuration
    api_title: str = "Insight Project - AI Services"
    api_version: str = "1.0.0"
    debug: bool = Field(default=False, env="DEBUG")

    # Server Configuration
    host: str = Field(default="0.0.0.0", env="HOST")
    port: int = Field(default=8000, env="PORT")

    # AI Service Configuration
    google_ai_api_key: Optional[str] = Field(default=None, env="GOOGLE_AI_API_KEY")

    # Form Reader Configuration
    form_reader_enabled: bool = Field(default=True, env="FORM_READER_ENABLED")
    yolo_model_path: str = Field(default="app/models/boxes.pt", env="YOLO_MODEL_PATH")
    dot_line_model_path: str = Field(
        default="app/models/dot_line.pt", env="DOT_LINE_MODEL_PATH"
    )

    # Money Reader Configuration
    money_reader_enabled: bool = Field(default=True, env="MONEY_READER_ENABLED")

    # PPT/PDF Reader Configuration
    ppt_pdf_reader_enabled: bool = Field(default=True, env="PPT_PDF_READER_ENABLED")
    max_file_size: int = Field(default=50 * 1024 * 1024, env="MAX_FILE_SIZE")  # 50MB

    # File Upload Configuration
    upload_dir: str = Field(default="uploads", env="UPLOAD_DIR")
    temp_dir: str = Field(default="temp", env="TEMP_DIR")

    # TTS Configuration
    tts_enabled: bool = Field(default=True, env="TTS_ENABLED")

    # Session Configuration
    session_timeout: int = Field(default=3600, env="SESSION_TIMEOUT")  # 1 hour
    max_sessions: int = Field(default=1000, env="MAX_SESSIONS")

    # CORS Configuration
    allowed_origins: list = Field(default=["*"], env="ALLOWED_ORIGINS")

    # Logging Configuration
    log_level: str = Field(default="INFO", env="LOG_LEVEL")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Set default API key if not provided
        if not self.google_ai_api_key:
            self.google_ai_api_key = "AIzaSyABJCFK7ylhc6yd0v5qH-2HpCZlZrjoF-Q"

        # Create directories if they don't exist
        os.makedirs(self.upload_dir, exist_ok=True)
        os.makedirs(self.temp_dir, exist_ok=True)

        # Create models directory
        os.makedirs("app/models", exist_ok=True)


# Global settings instance
settings = Settings()


# Service-specific configurations
class FormReaderConfig:
    """Form Reader specific configuration"""

    # YOLO model settings
    confidence_threshold: float = 0.5
    iou_threshold: float = 0.4

    # OCR settings
    ocr_languages: list = ["en", "ar"]

    # Image processing settings
    max_image_size: tuple = (1920, 1080)
    image_quality: int = 95


class MoneyReaderConfig:
    """Money Reader specific configuration"""

    # Currency detection settings
    supported_currencies: list = ["USD", "EUR", "SAR", "AED", "KWD"]

    # Image processing settings
    max_image_size: tuple = (1920, 1080)
    image_quality: int = 95


class PPTReaderConfig:
    """PPT/PDF Reader specific configuration"""

    # Document processing settings
    supported_formats: list = [".pptx", ".ppt", ".pdf"]
    max_pages: int = 100
    image_dpi: int = 150

    # Analysis settings
    analysis_languages: list = ["arabic", "english"]
    max_text_length: int = 10000


# Service configurations
form_reader_config = FormReaderConfig()
money_reader_config = MoneyReaderConfig()
ppt_reader_config = PPTReaderConfig()
