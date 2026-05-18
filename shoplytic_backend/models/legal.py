from pydantic import BaseModel, Field
from typing import List, Optional


class LawArticle(BaseModel):
    article: str = Field(description="Madde numarası")
    title: str = Field(description="Madde başlığı")
    content: str = Field(description="Madde içeriği")
    relevance: float = Field(description="Alaka düzeyi (0-1)")


class LegalAnalysis(BaseModel):
    complaint_summary: str = Field(description="Şikayet özeti")
    violated_articles: List[LawArticle] = Field(description="İhlal edilen maddeler")
    consumer_rights: List[str] = Field(description="Kullanıcının hakları")
    authorities_to_apply: List[str] = Field(description="Başvurulacak kurumlar")
    recommended_actions: List[str] = Field(description="Tavsiye edilen aksiyonlar")


class PetitionRequest(BaseModel):
    complaint: str = Field(description="Şikayet metni")
    violated_law: str = Field(description="İhlal edilen kanun maddesi")
    demand: str = Field(description="Talep")
