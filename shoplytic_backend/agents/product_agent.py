import json
import logging
from typing import List, Optional

from clients.llm_client import get_llm
from models.product import Product, ProductSearchResult, PlatformPrice

logger = logging.getLogger(__name__)

PRODUCT_PROMPT = """Kategori: {category}
Bütçe: {budget} TL
Kullanıcı Bağlamı: {context}

Trendyol ve Hepsiburada'da gerçekten satılan, gerçekçi fiyatlı
3 ürün önerisi oluştur. JSON formatında:
[
  {{
    "name": "Ürün Adı",
    "brand": "Marka",
    "price": 0000,
    "platform": "Trendyol",
    "rating": 4.5,
    "review_count": 1250,
    "url": "https://trendyol.com/...",
    "image_url": "",
    "why_recommended": "Bu kullanıcıya neden uygun olduğu"
  }}
]
Fiyatlar Türkiye piyasasıyla tutarlı olsun."""


def score_product(product: dict, user_context: dict) -> float:
    """
    Ürünü kullanıcı bağlamına göre puanla.

    Faktörler:
    - Fiyat-bütçe uyumu      : %30
    - Kullanıcı rating'i     : %25
    - Yorum sayısı (güven)   : %20
    - İklim/durum uygunluğu  : %25
    """
    budget = user_context.get("budget", 5000)
    budget_score = 1.0 - min(abs(product["price"] - budget) / budget, 1.0)
    rating_score = product.get("rating", 4.0) / 5.0
    trust_score = min(product.get("review_count", 0) / 1000, 1.0)
    relevance_score = 0.75  # Placeholder

    weights = [0.30, 0.25, 0.20, 0.25]
    scores = [budget_score, rating_score, trust_score, relevance_score]

    return sum(w * s for w, s in zip(weights, scores))


async def search_products(
    query: str, category: str, budget: float = 0
) -> ProductSearchResult:
    """Ürün araması yapar. LLM-generated mock veri kullanır."""
    try:
        llm = get_llm()
        prompt = PRODUCT_PROMPT.format(
            category=category or "genel", budget=budget or 5000, context=query
        )
        response = await llm.ainvoke(
            [
                ("system", "Sen bir e-ticaret uzmanısın."),
                ("human", prompt),
            ]
        )
        products_data = json.loads(response.content)
        products = [Product(**p) for p in products_data]
        return ProductSearchResult(products=products, total_count=len(products), category=category)
    except Exception as e:
        logger.warning(f"LLM product search failed, using fallback: {e}")
        return _fallback_products(category)


async def compare_prices(product_name: str) -> List[PlatformPrice]:
    """Fiyat karşılaştırması yapar."""
    return [
        PlatformPrice(platform="Trendyol", price=15999.99, url=f"https://trendyol.com/{product_name}"),
        PlatformPrice(platform="Hepsiburada", price=16499.00, url=f"https://hepsiburada.com/{product_name}"),
    ]


async def get_stock(product_id: str) -> dict:
    """Stok durumu sorgular."""
    return {"in_stock": True, "stock_count": 42, "estimated_delivery": "3-5 iş günü"}


def _fallback_products(category: str) -> ProductSearchResult:
    """LLM yoksa kullanılacak örnek ürünler."""
    products = [
        Product(
            id="1",
            name="Örnek Ürün 1",
            brand="Marka A",
            price=4999.99,
            platform="Trendyol",
            rating=4.5,
            review_count=1250,
            category=category,
            why_recommended="Popüler ve bütçe dostu",
        ),
        Product(
            id="2",
            name="Örnek Ürün 2",
            brand="Marka B",
            price=7499.00,
            platform="Hepsiburada",
            rating=4.3,
            review_count=890,
            category=category,
            why_recommended="Yüksek puanlı ve güvenilir",
        ),
    ]
    return ProductSearchResult(products=products, total_count=len(products), category=category)
