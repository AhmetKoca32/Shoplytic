"""
ProcessNode: LLM çıktısını ayrıştıran ve iş akışına uygun hale getiren node
"""
import logging
from typing import Dict, Any
import json

logger = logging.getLogger(__name__)

class ProcessNode:
    async def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        return await self.run(state)

    async def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        llm_output = state.get("llm_output")
        if not llm_output:
            state["process_error"] = "ProcessNode: LLM çıktısı eksik."
            return state
        try:
            try:
                import json
                parsed = json.loads(llm_output)
                state["processed_output"] = parsed
            except Exception:
                state["processed_output"] = llm_output
            state["process_error"] = None
        except Exception as e:
            state["processed_output"] = None
            state["process_error"] = str(e)
        return state
        """
        LLM'den dönen yanıtı ayrıştırır, doğrular ve iş akışına uygun hale getirir.
        """
        llm_output = state.get("llm_output")
        if not llm_output:
            logger.error("ProcessNode: LLM çıktısı eksik!")
            state["process_error"] = "ProcessNode: LLM çıktısı eksik."
            return state
        try:
            # Yanıt JSON bekleniyorsa ayrıştır
            try:
                parsed = json.loads(llm_output)
                state["processed_output"] = parsed
                logger.info("ProcessNode: LLM yanıtı JSON olarak ayrıştırıldı.")
            except json.JSONDecodeError:
                # Düz metin ise doğrudan aktar
                state["processed_output"] = llm_output
                logger.info("ProcessNode: LLM yanıtı düz metin olarak işlendi.")
            state["process_error"] = None
        except Exception as e:
            logger.exception("ProcessNode: LLM çıktısı işlenirken hata oluştu.")
            state["processed_output"] = None
            state["process_error"] = str(e)
        return state
