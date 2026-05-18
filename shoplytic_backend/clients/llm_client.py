import logging

from core.config import settings

logger = logging.getLogger(__name__)

_llm_instance = None


def get_llm():
    """
    DeepSeek V4-Flash LLM istemcisini döndürür.
    OpenAI-compatible API kullanır.
    API key yoksa None döner (agent'lar fallback kullanır).
    """
    global _llm_instance

    if _llm_instance is not None:
        return _llm_instance

    if not settings.deepseek_api_key or settings.deepseek_api_key == "your_deepseek_api_key_here":
        logger.warning("DeepSeek API key not configured. Using fallback data.")
        return None

    try:
        from langchain_openai import ChatOpenAI

        _llm_instance = ChatOpenAI(
            model=settings.deepseek_model,
            temperature=0.3,
            api_key=settings.deepseek_api_key,
            base_url=settings.deepseek_base_url,
        )
        return _llm_instance
    except ImportError:
        logger.warning("langchain-openai not installed. Using fallback.")
        return None
    except Exception as e:
        logger.warning(f"Failed to initialize LLM: {e}. Using fallback.")
        return None
