import logging
from typing import Optional

from agents.base_agent import BaseAgent

logger = logging.getLogger(__name__)


async def segment_user(user_context: dict) -> dict:
    """
    Kullanıcıyı segmentine göre kategorize eder.

    Segmentler:
    - university_student: Bütçe duyarlı, teknoloji odaklı
    - new_employee: Profesyonel giyim, ofis malzemeleri
    - married_couple: Ev eşyası, beyaz eşya
    - retiree: Sağlık, hobi, seyahat
    - general: Diğer
    """
    life_situation = user_context.get("life_situation", {})
    situation_type = life_situation.get("type", "general")

    segments = {
        "university_student": {
            "segment": "Üniversite Öğrencisi",
            "price_sensitivity": 0.8,
            "priority_categories": ["teknoloji", "kırtasiye", "giyim"],
        },
        "new_employee": {
            "segment": "Yeni Çalışan",
            "price_sensitivity": 0.5,
            "priority_categories": ["giyim", "teknoloji", "ofis"],
        },
        "married_couple": {
            "segment": "Evli Çift",
            "price_sensitivity": 0.4,
            "priority_categories": ["ev eşyası", "beyaz eşya", "mobilya"],
        },
        "retiree": {
            "segment": "Emekli",
            "price_sensitivity": 0.6,
            "priority_categories": ["sağlık", "hobi", "seyahat"],
        },
    }

    return segments.get(situation_type, segments["general"])
