"""
OutputNode: İş akışı sonucunu formatlayan LangGraph node'u
"""
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class OutputNode:
    async def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        return await self.run(state)

    async def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        try:
            output = state.get("api_response") or state.get("processed_output") or state.get("llm_output")
            state["final_output"] = output
            state["output_error"] = None
        except Exception as e:
            state["final_output"] = None
            state["output_error"] = str(e)
        return state
        """
        İş akışı sonucunu uygun biçimde formatlar ve döner.
        """
        try:
            # Öncelikli olarak API yanıtı, yoksa işlenmiş LLM çıktısı, yoksa LLM çıktısı döner
            output = state.get("api_response") or state.get("processed_output") or state.get("llm_output")
            state["final_output"] = output
            state["output_error"] = None
            logger.info("OutputNode: Çıktı başarıyla formatlandı.")
        except Exception as e:
            logger.exception("OutputNode: Çıktı formatlanırken hata oluştu.")
            state["final_output"] = None
            state["output_error"] = str(e)
        return state
