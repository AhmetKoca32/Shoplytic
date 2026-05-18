import json
import logging
from typing import List

from clients.llm_client import get_llm
from models.legal import LegalAnalysis, LawArticle, PetitionRequest

logger = logging.getLogger(__name__)

LEGAL_PROMPT = """Kullanıcı Şikayeti: {complaint}

Şikayeti 6502 Sayılı Tüketicinin Korunması Hakkında Kanun kapsamında analiz et.
Aşağıdaki JSON formatında yanıt ver:
{{
  "complaint_summary": "Şikayet özeti",
  "violated_articles": [
    {{
      "article": "Madde 4",
      "title": "Ayıplı mal",
      "content": "Madde içeriği kısa özeti",
      "relevance": 0.95
    }}
  ],
  "consumer_rights": ["Hak 1", "Hak 2"],
  "authorities_to_apply": ["Tüketici Hakem Heyeti", "Ticaret Bakanlığı"],
  "recommended_actions": ["Adım 1", "Adım 2"]
}}

Sadece JSON döndür, başka açıklama yazma."""

PETITION_PROMPT = """Aşağıdaki bilgilerle Tüketici Hakem Heyeti'ne resmi dilekçe yaz:

Şikayet: {complaint}
İhlal edilen madde: {violated_law}
Talep: {demand}

Dilekçe resmi Türkçe hukuk diliyle yazılmalı,
kanuni dayanakları içermeli ve profesyonel olmalıdır."""


async def analyze_complaint(complaint: str) -> LegalAnalysis:
    """Kullanıcı şikayetini analiz eder."""
    try:
        llm = get_llm()
        prompt = LEGAL_PROMPT.format(complaint=complaint)
        response = await llm.ainvoke(
            [
                ("system", "Sen bir tüketici hukuku uzmanısın."),
                ("human", prompt),
            ]
        )
        data = json.loads(response.content)
        return LegalAnalysis(**data)
    except Exception as e:
        logger.warning(f"LLM legal analysis failed, using fallback: {e}")
        return _fallback_legal_analysis(complaint)


async def generate_petition(request: PetitionRequest) -> str:
    """Şikayet için resmi dilekçe oluşturur."""
    try:
        llm = get_llm()
        prompt = PETITION_PROMPT.format(
            complaint=request.complaint,
            violated_law=request.violated_law,
            demand=request.demand,
        )
        response = await llm.ainvoke(
            [
                ("system", "Sen bir hukuk danışmanısın."),
                ("human", prompt),
            ]
        )
        return response.content
    except Exception as e:
        logger.warning(f"LLM petition generation failed, using fallback: {e}")
        return _fallback_petition(request)


def _fallback_legal_analysis(complaint: str) -> LegalAnalysis:
    return LegalAnalysis(
        complaint_summary=complaint,
        violated_articles=[
            LawArticle(
                article="Madde 4",
                title="Ayıplı Mal",
                content="Satıcı, ayıplı maldan sorumludur ve tüketici seçimlik haklara sahiptir.",
                relevance=0.85,
            )
        ],
        consumer_rights=[
            "Malın iadesini talep etme",
            "Bedelin iadesini isteme",
            "Ayıp oranında bedel indirimi",
        ],
        authorities_to_apply=[
            "Tüketici Hakem Heyeti",
            "Ticaret Bakanlığı Tüketicinin Korunması Dairesi",
        ],
        recommended_actions=[
            "Satıcıya yazılı başvuru yapın",
            "Tüketici Hakem Heyeti'ne başvurun",
            "Dilekçe hazırlayın",
        ],
    )


def _fallback_petition(request: PetitionRequest) -> str:
    return f"""TÜKETİCİ HAKEM HEYETİ BAŞKANLIĞI'NA

ŞİKAYET EDEN: [Adınız ve Soyadınız]
ADRES: [Adresiniz]

KONU: Şikayet dilekçesi

AÇIKLAMALAR:
{request.complaint}

İHLAL EDİLEN MADDE:
{request.violated_law}

TALEP:
{request.demand}

Sayın Yetkili,
Yukarıda açıklanan nedenlerle talebimin kabulüne karar verilmesini arz ederim.

[Tarih]
[İmza]"""
