import json
import logging
from typing import Optional

from clients.llm_client import get_llm
from agents.base_agent import BaseAgent
from models.mindmap import MindMapOutput, MindMapCategory

logger = logging.getLogger(__name__)

MINDMAP_PROMPT = """Kullanıcı Bağlamı: {context}

Bu bağlama göre kişiselleştirilmiş bir alışveriş zihin haritası oluştur.
Kategoriler gerçekçi, önceliklendirilmiş ve bütçeye duyarlı olsun.
Türkiye e-ticaret fiyatlarını kullan.

Aşağıdaki JSON formatında yanıt ver:
{{
  "central_topic": "Ana konu başlığı",
  "user_summary": "Kullanıcının durumunun 1 cümlelik özeti",
  "main_categories": [
    {{
      "name": "Kategori adı",
      "emoji": "🎒",
      "items": ["İhtiyaç 1", "İhtiyaç 2"],
      "priority": "high",
      "estimated_budget": "5000-10000 TL"
    }}
  ],
  "total_estimated_budget": "15000-25000 TL"
}}

Sadece JSON döndür, başka açıklama yazma."""


async def generate_mindmap(context: dict, user_input: str) -> MindMapOutput:
    """AI ile zihin haritası oluşturur. Fallback ile mock veri döner."""
    try:
        llm = get_llm()
        context_str = json.dumps(context, ensure_ascii=False, indent=2)
        prompt = MINDMAP_PROMPT.format(context=context_str)

        response = await llm.ainvoke(
            [
                ("system", "Sen bir alışveriş planlama uzmanısın."),
                ("human", prompt),
            ]
        )
        data = json.loads(response.content)
        return MindMapOutput(**data)
    except Exception as e:
        logger.warning(f"LLM mind map generation failed, using fallback: {e}")
        return _fallback_mindmap(user_input)


def _fallback_mindmap(user_input: str) -> MindMapOutput:
    """LLM yoksa kullanılacak örnek zihin haritası."""
    return MindMapOutput(
        central_topic=user_input,
        user_summary=f"Kullanıcının durumu: {user_input}",
        main_categories=[
            MindMapCategory(
                name="Temel İhtiyaçlar",
                emoji="📦",
                items=["Genel alışveriş listesi"],
                priority="high",
                estimated_budget="5000-10000 TL",
            ),
            MindMapCategory(
                name="Teknoloji",
                emoji="💻",
                items=["Laptop", "Telefon", "Kulaklık"],
                priority="medium",
                estimated_budget="15000-30000 TL",
            ),
            MindMapCategory(
                name="Giyim",
                emoji="👕",
                items=["Mevsimlik kıyafetler", "Ayakkabı"],
                priority="medium",
                estimated_budget="3000-7000 TL",
            ),
        ],
        total_estimated_budget="23000-47000 TL",
    )
