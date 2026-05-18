import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings
from api.routes.health import router as health_router
from api.routes.ai import router as ai_router
from api.routes.ecommerce import router as ecommerce_router
from api.routes.legal import router as legal_router

logging.basicConfig(level=logging.INFO if settings.debug else logging.WARNING)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 Shoplytic backend starting...")
    logger.info(f"API docs: http://{settings.host}:{settings.port}/docs")
    yield
    logger.info("Shoplytic backend shutting down.")


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routes ─────────────────────────────────────────────────────────────────────
app.include_router(health_router, tags=["Health"])
app.include_router(ai_router, prefix="/api/v1/ai", tags=["AI"])
app.include_router(ecommerce_router, prefix="/api/v1/ecommerce", tags=["E-Commerce"])
app.include_router(legal_router, prefix="/api/v1/legal", tags=["Legal"])
