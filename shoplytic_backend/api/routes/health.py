from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health():
    return {"status": "ok", "service": "Shoplytic"}


@router.get("/api/v1/system/status")
async def system_status():
    return {
        "status": "operational",
        "version": "1.0.0",
        "agents": {
            "context_analysis": "ready",
            "mind_map": "ready",
            "product": "ready",
            "legal": "ready",
        },
    }
