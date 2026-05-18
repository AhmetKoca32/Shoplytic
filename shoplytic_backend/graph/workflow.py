import logging
from typing import Optional

from graph.state import ShopLyticState
from graph.nodes import context_analysis_node, mindmap_node, product_node, legal_node

logger = logging.getLogger(__name__)


async def run_mindmap_workflow(user_input: str, thread_id: str = "default") -> dict:
    """
    Kullanıcı girdisini alır, agent workflow'unu başlatır ve sonucu döner.
    LangGraph StateGraph olmadan sequential çalışır (minimal bağımlılık için).
    """
    state: ShopLyticState = {
        "user_input": user_input,
        "thread_id": thread_id,
        "context_analysis": None,
        "mind_map": None,
        "product_recommendations": None,
        "legal_analysis": None,
        "messages": [],
        "current_step": "start",
        "error": None,
    }

    logger.info(f"[{thread_id}] Workflow started: {user_input[:50]}...")

    # 1. Context Analysis
    state.update(await context_analysis_node(state))
    if state.get("error"):
        return {"error": state["error"], "step": state["current_step"]}

    # 2. Mind Map
    state.update(await mindmap_node(state))
    if state.get("error"):
        return {"error": state["error"], "step": state["current_step"]}

    # 3. Product Search (based on mind map)
    state.update(await product_node(state))

    # 4. Legal Analysis
    state.update(await legal_node(state))

    logger.info(f"[{thread_id}] Workflow completed successfully.")

    return {
        "central_topic": state["mind_map"].get("central_topic", ""),
        "user_summary": state["mind_map"].get("user_summary", ""),
        "main_categories": state["mind_map"].get("main_categories", []),
        "total_estimated_budget": state["mind_map"].get("total_estimated_budget", ""),
        "products": state["product_recommendations"],
        "context": state["context_analysis"],
    }
