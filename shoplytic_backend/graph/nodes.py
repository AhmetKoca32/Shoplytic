import logging

from agents.context_analysis_agent import analyze_context
from agents.mindmap_agent import generate_mindmap
from agents.product_agent import search_products
from agents.legal_agent import analyze_complaint
from graph.state import ShopLyticState

logger = logging.getLogger(__name__)


async def context_analysis_node(state: ShopLyticState) -> dict:
    """Context analizi node'u."""
    logger.info(f"[{state['thread_id']}] Running Context Analysis Agent...")
    try:
        context = await analyze_context(state["user_input"])
        return {"context_analysis": context, "current_step": "context_done"}
    except Exception as e:
        logger.error(f"Context analysis failed: {e}")
        return {"error": str(e), "current_step": "error"}


async def mindmap_node(state: ShopLyticState) -> dict:
    """Zihin haritası oluşturma node'u."""
    logger.info(f"[{state['thread_id']}] Running Mind Map Agent...")
    try:
        context = state.get("context_analysis", {})
        mindmap = await generate_mindmap(context, state["user_input"])
        return {
            "mind_map": mindmap.model_dump(),
            "current_step": "mindmap_done",
        }
    except Exception as e:
        logger.error(f"Mind map generation failed: {e}")
        return {"error": str(e), "current_step": "error"}


async def product_node(state: ShopLyticState) -> dict:
    """Ürün arama node'u."""
    logger.info(f"[{state['thread_id']}] Running Product Agent...")
    try:
        mind_map = state.get("mind_map", {})
        categories = mind_map.get("main_categories", [])
        all_products = []

        for cat in categories[:3]:  # İlk 3 kategoriyi tara
            result = await search_products(
                query=cat.get("name", ""),
                category=cat.get("name", ""),
                budget=10000,
            )
            all_products.extend(result.products)

        return {
            "product_recommendations": {
                "products": [p.model_dump() for p in all_products],
                "total_count": len(all_products),
            },
            "current_step": "product_done",
        }
    except Exception as e:
        logger.error(f"Product search failed: {e}")
        return {"error": str(e), "current_step": "error"}


async def legal_node(state: ShopLyticState) -> dict:
    """Hukuki analiz node'u."""
    logger.info(f"[{state['thread_id']}] Running Legal Agent...")
    try:
        # Simplified: legal analysis from user input context
        legal = await analyze_complaint(state["user_input"])
        return {
            "legal_analysis": legal.model_dump(),
            "current_step": "legal_done",
        }
    except Exception as e:
        logger.error(f"Legal analysis failed: {e}")
        return {"error": str(e), "current_step": "error"}
