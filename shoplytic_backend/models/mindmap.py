from pydantic import BaseModel, Field
from typing import List, Optional


class MindMapCategory(BaseModel):
    name: str = Field(description="Kategori adı")
    emoji: str = Field(description="Kategoriyi temsil eden emoji")
    items: List[str] = Field(description="Bu kategorideki ihtiyaç listesi")
    priority: str = Field(description="high / medium / low")
    estimated_budget: str = Field(description="Tahmini bütçe aralığı TL")


class MindMapOutput(BaseModel):
    central_topic: str = Field(description="Ana konu başlığı")
    user_summary: str = Field(description="Kullanıcının durumunun 1 cümlelik özeti")
    main_categories: List[MindMapCategory] = Field(description="Ana kategoriler")
    total_estimated_budget: str = Field(description="Toplam tahmini bütçe")
