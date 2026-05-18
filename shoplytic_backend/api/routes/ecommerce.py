from fastapi import APIRouter

from models.product import Product, ProductSearchResult, PlatformPrice
from agents.product_agent import search_products, compare_prices, get_stock

router = APIRouter()


@router.get("/search", response_model=ProductSearchResult)
async def search(q: str = "", category: str = "", budget: float = 0):
    return await search_products(query=q, category=category, budget=budget)


@router.get("/compare/{name}")
async def compare(name: str):
    platforms = await compare_prices(product_name=name)
    return {"product": name, "platforms": platforms}


@router.get("/stock/{product_id}")
async def stock(product_id: str):
    stock_info = await get_stock(product_id=product_id)
    return {"product_id": product_id, **stock_info}


@router.get("/recommendations/{category}")
async def recommendations(category: str):
    result = await search_products(query="", category=category, budget=0)
    return result
