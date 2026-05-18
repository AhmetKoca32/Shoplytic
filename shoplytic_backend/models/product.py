from pydantic import BaseModel, Field
from typing import List, Optional


class PlatformPrice(BaseModel):
    platform: str = Field(description="E-ticaret platformu (Trendyol, Hepsiburada, vb.)")
    price: float = Field(description="Fiyat (TL)")
    url: str = Field(description="Ürün linki")
    in_stock: bool = Field(default=True, description="Stok durumu")


class Product(BaseModel):
    id: str = Field(description="Ürün ID")
    name: str = Field(description="Ürün adı")
    brand: str = Field(default="", description="Marka")
    price: float = Field(description="Fiyat (TL)")
    platform: str = Field(description="Platform adı")
    rating: float = Field(default=4.0, description="Kullanıcı puanı (1-5)")
    review_count: int = Field(default=0, description="Yorum sayısı")
    image_url: str = Field(default="", description="Ürün görsel URL")
    url: str = Field(default="", description="Ürün sayfası linki")
    category: str = Field(default="", description="Kategori")
    why_recommended: str = Field(default="", description="Neden önerildiği")


class ProductSearchResult(BaseModel):
    products: List[Product]
    total_count: int
    category: str = ""
