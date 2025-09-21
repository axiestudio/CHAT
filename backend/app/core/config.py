"""
Configuration settings for the FastAPI backend
"""

import os
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    """Application settings."""
    
    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "AxieStudio AI Flow Generator"
    VERSION: str = "1.0.0"
    
    # CORS Configuration
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "https://*.vercel.app",
        "https://*.koyeb.app"
    ]
    
    # AI Configuration
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    
    # AxieStudio Configuration
    AXIESTUDIO_DATA_PATH: str = "axiestudio_core/axiestudio"
    AI_SERVICES_PATH: str = "axiestudio_core/ai"
    
    # Generation Settings
    DEFAULT_MODEL: str = "gpt-4"
    MAX_COMPONENTS: int = 20
    GENERATION_TIMEOUT: int = 30
    
    class Config:
        case_sensitive = True
        env_file = ".env"
        extra = "ignore"  # Allow extra fields in .env

settings = Settings()
