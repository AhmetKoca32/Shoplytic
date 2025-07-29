"""
LLMNode: Gemini API ile entegre çalışan LangGraph LLM Node'u
"""
import logging
from typing import Dict, Any
from app.config.settings import Settings
import google.generativeai as genai

logger = logging.getLogger(__name__)
settings = Settings()

class LLMNode:
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        if not self.api_key:
            logger.error("Gemini API anahtarı bulunamadı. Lütfen .env dosyasına GEMINI_API_KEY ekleyin.")
        genai.configure(api_key=self.api_key)

    async def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        return await self.run(state)

    async def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        PromptNode'dan gelen prompt ile Gemini LLM çağrısı yapar ve yanıtı workflow'a ekler.
        """
        prompt = state.get("prompt")
        if not prompt:
            logger.error("LLMNode: prompt eksik!")
            state["llm_error"] = "LLMNode: prompt eksik."
            return state
        try:
            model = genai.GenerativeModel("gemini-pro")
            response = model.generate_content(prompt)
            if hasattr(response, "text"):
                llm_output = response.text
            else:
                llm_output = str(response)
            state["llm_output"] = llm_output
            state["llm_error"] = None
            logger.info("LLMNode: Gemini yanıtı başarıyla alındı.")
        except Exception as e:
            logger.exception("LLMNode: Gemini API çağrısı başarısız.")
            state["llm_output"] = None
            state["llm_error"] = str(e)
        return state
