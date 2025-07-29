from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router as api_router
from app.config.settings import get_settings
import uvicorn

# Ayarları yükle
settings = get_settings()

# FastAPI uygulamasını oluştur
app = FastAPI(
    title="Shoplytic API",
    description="AI-Assisted Smart E-commerce Workflow API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware ekle
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Production'da daha kısıtlayıcı olmalı
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API router'ını ekle
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    """Ana endpoint - API durumunu kontrol et"""
    return {
        "message": "Shoplytic API is running!",
        "version": "1.0.0",
        "status": "healthy"
    }

@app.get("/health")
async def health_check():
    """Sağlık kontrolü endpoint'i"""
    return {"status": "healthy", "service": "shoplytic-api"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info"
    )