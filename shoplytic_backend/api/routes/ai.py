from fastapi import APIRouter

from models.mindmap import MindMapOutput
from graph.workflow import run_mindmap_workflow

router = APIRouter()


@router.post("/generate-mindmap", response_model=MindMapOutput)
async def generate_mindmap(body: dict):
    """
    Kullanıcı girdisine göre zihin haritası oluşturur.
    Body: { "user_input": "...", "thread_id": "..." }
    """
    result = await run_mindmap_workflow(
        user_input=body.get("user_input", ""),
        thread_id=body.get("thread_id", "default"),
    )
    return result


@router.post("/chat")
async def chat(body: dict):
    """
    AI sohbet endpointi.
    Body: { "message": "...", "thread_id": "...", "node_context": "..." }
    """
    from agents.context_analysis_agent import analyze_context
    from agents.mindmap_agent import generate_mindmap

    message = body.get("message", "")
    thread_id = body.get("thread_id", "default")
    node_context = body.get("node_context")

    # For now, return a structured response
    return {
        "response": f"Analiz ediliyor: '{message}'... Bu bir mock yanıttır. Backend bağlandığında gerçek AI yanıtı gelecek.",
        "actions": [],
        "thread_id": thread_id,
    }
