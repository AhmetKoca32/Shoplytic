from pydantic_settings import BaseSettings
from typing import Optional
import os
from functools import lru_cache

class Settings(BaseSettings):
    """Uygulama ayarları"""
    
    # Temel ayarlar
    APP_NAME: str = "Shoplytic API"
    VERSION: str = "1.0.0"
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Veritabanı ayarları
    DATABASE_URL: Optional[str] = None
    REDIS_URL: Optional[str] = None
    
    # AI Model ayarları
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    GEMINI_API_KEY: Optional[str] = None
    DEFAULT_LLM_MODEL: str = "gpt-4"
    
    # E-ticaret API ayarları
    SHOPIFY_API_KEY: Optional[str] = None
    SHOPIFY_SECRET_KEY: Optional[str] = None
    WOOCOMMERCE_API_KEY: Optional[str] = None
    WOOCOMMERCE_SECRET_KEY: Optional[str] = None
    
    # n8n entegrasyon ayarları
    N8N_WEBHOOK_URL: Optional[str] = None
    N8N_API_KEY: Optional[str] = None
    
    # Güvenlik ayarları
    SECRET_KEY: str = "shoplytic-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS ayarları
    ALLOWED_ORIGINS: list = ["*"]
    
    # Logging ayarları
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    """Ayarları döndür (cache ile)"""
    return Settings()