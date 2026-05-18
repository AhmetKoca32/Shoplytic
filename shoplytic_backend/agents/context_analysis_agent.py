import json
import logging

from clients.llm_client import get_llm
from agents.base_agent import BaseAgent

logger = logging.getLogger(__name__)

CONTEXT_PROMPT = """Sen bir yaşam durumu analiz uzmanısın.
Kullanıcının verdiği metni analiz et ve aşağıdaki JSON formatında dön:
{{
  "location": {{"city": "", "climate": "", "season_now": ""}},
  "life_situation": {{"type": "", "priorities": [], "budget_level": ""}},
  "immediate_needs": [],
  "context_tags": []
}}

Sadece JSON döndür, başka hiçbir şey yazma."""


async def analyze_context(user_input: str) -> dict:
    """
    Kullanıcı girdisini analiz eder.
    Mock fallback ile — LLM bağlanamazsa temel bir analiz döner.
    """
    try:
        llm = get_llm()
        response = await llm.ainvoke(
            [
                ("system", CONTEXT_PROMPT),
                ("human", user_input),
            ]
        )
        return json.loads(response.content)
    except Exception as e:
        logger.warning(f"LLM context analysis failed, using fallback: {e}")
        return _fallback_analysis(user_input)


def _fallback_analysis(user_input: str) -> dict:
    """LLM yoksa kullanılacak basit analiz."""
    return {
        "location": {"city": "bilinmiyor", "climate": "bilinmiyor", "season_now": "bilinmiyor"},
        "life_situation": {
            "type": "general",
            "priorities": ["general_shopping"],
            "budget_level": "medium",
        },
        "immediate_needs": [user_input],
        "context_tags": ["general"],
    }
