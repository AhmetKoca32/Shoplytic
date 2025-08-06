"""
E-ticaret entegrasyonu için basit HTTP client
n8n yerine direkt API çağrıları kullanır
"""
import requests
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class EcommerceClient:
    """E-ticaret platformları için basit HTTP client"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Shoplytic/1.0',
            'Content-Type': 'application/json'
        })
        
        # Mock e-ticaret verileri (gerçek API'ler yerine)
        self.mock_products = {
            "laptop": [
                {
                    "id": "1",
                    "name": "Lenovo ThinkPad E15",
                    "price": 15999.99,
                    "platform": "Trendyol",
                    "rating": 4.5,
                    "stock": True,
                    "url": "https://trendyol.com/laptop-1",
                    "image": "https://source.unsplash.com/300x300/?laptop+thinkpad",
                    "category": "Elektronik",
                    "description": "Lenovo ThinkPad E15 - İş ve eğitim için ideal laptop"
                },
                {
                    "id": "2", 
                    "name": "HP Pavilion 15",
                    "price": 17499.99,
                    "platform": "Hepsiburada",
                    "rating": 4.3,
                    "stock": True,
                    "url": "https://hepsiburada.com/laptop-2",
                    "image": "https://source.unsplash.com/300x300/?hp+laptop",
                    "category": "Elektronik",
                    "description": "HP Pavilion 15 - Performanslı ve şık tasarım"
                }
            ],
            "mont": [
                {
                    "id": "3",
                    "name": "Kışlık Kalın Mont",
                    "price": 899.99,
                    "platform": "Trendyol",
                    "rating": 4.7,
                    "stock": True,
                    "url": "https://trendyol.com/mont-1",
                    "image": "https://source.unsplash.com/300x300/?winter+coat",
                    "category": "Giyim",
                    "description": "Kışlık kalın mont - Soğuk havalarda sıcak tutar"
                },
                {
                    "id": "4",
                    "name": "Hafif Kış Montu",
                    "price": 749.99,
                    "platform": "Hepsiburada", 
                    "rating": 4.4,
                    "stock": True,
                    "url": "https://hepsiburada.com/mont-2",
                    "image": "https://source.unsplash.com/300x300/?jacket+coat",
                    "category": "Giyim",
                    "description": "Hafif kış montu - Şık ve pratik tasarım"
                }
            ],
            "çanta": [
                {
                    "id": "5",
                    "name": "Okul Çantası 15.6\"",
                    "price": 299.99,
                    "platform": "Trendyol",
                    "rating": 4.6,
                    "stock": True,
                    "url": "https://trendyol.com/canta-1",
                    "image": "https://source.unsplash.com/300x300/?school+bag",
                    "category": "Giyim",
                    "description": "Okul çantası 15.6\" - Dayanıklı ve ergonomik"
                },
                {
                    "id": "6",
                    "name": "Laptop Çantası",
                    "price": 399.99,
                    "platform": "Hepsiburada",
                    "rating": 4.2,
                    "stock": True,
                    "url": "https://hepsiburada.com/canta-2",
                    "image": "https://source.unsplash.com/300x300/?laptop+bag",
                    "category": "Giyim",
                    "description": "Laptop çantası - Koruyucu ve şık tasarım"
                }
            ]
        }
    
    async def search_products(self, query: str, category: str = None, limit: int = 5) -> List[Dict[str, Any]]:
        """Ürün arama"""
        try:
            # Gerçek API çağrısı yerine mock veri döndür
            products = []
            
            # Kategori bazlı arama
            if category and category.lower() in self.mock_products:
                products = self.mock_products[category.lower()]
            else:
                # Genel arama
                for cat_products in self.mock_products.values():
                    products.extend(cat_products)
            
            # Query filtreleme
            if query:
                products = [p for p in products if query.lower() in p["name"].lower()]
            
            # Limit uygula
            products = products[:limit]
            
            # Resim URL'lerini güncelle
            for product in products:
                if not product.get("image"):
                    product["image"] = self._generate_image_url(product["name"], category or "product")
            
            logger.info(f"Found {len(products)} products for query: {query}")
            return products
            
        except Exception as e:
            logger.error(f"Product search failed: {str(e)}")
            return []
    
    def _generate_image_url(self, product_name: str, category: str) -> str:
        """Ürün için resim URL'si oluştur"""
        import random
        
        # Kategori bazlı resim anahtar kelimeleri
        category_keywords = {
            "laptop": ["laptop", "computer", "electronics", "tech"],
            "smartphone": ["smartphone", "phone", "mobile", "electronics"],
            "clothing": ["clothing", "fashion", "shirt", "dress"],
            "shoes": ["shoes", "footwear", "sneakers", "boots"],
            "furniture": ["furniture", "chair", "table", "home"],
            "cosmetics": ["cosmetics", "beauty", "makeup", "skincare"]
        }
        
        keywords = category_keywords.get(category.lower(), [category.lower(), "product"])
        keyword = random.choice(keywords)
        
        image_urls = [
            f"https://source.unsplash.com/300x300/?{product_name.lower().replace(' ', '+')}",
            f"https://source.unsplash.com/300x300/?{keyword}",
            f"https://source.unsplash.com/300x300/?{keyword}+product",
            f"https://source.unsplash.com/300x300/?{keyword}+item"
        ]
        
        return random.choice(image_urls)
    
    async def get_product_details(self, product_id: str) -> Optional[Dict[str, Any]]:
        """Ürün detayları"""
        try:
            # Tüm ürünlerde ara
            for products in self.mock_products.values():
                for product in products:
                    if product["id"] == product_id:
                        return product
            
            return None
            
        except Exception as e:
            logger.error(f"Product details fetch failed: {str(e)}")
            return None
    
    async def compare_prices(self, product_name: str) -> List[Dict[str, Any]]:
        """Fiyat karşılaştırması"""
        try:
            similar_products = []
            
            # Benzer ürünleri bul
            for products in self.mock_products.values():
                for product in products:
                    if product_name.lower() in product["name"].lower():
                        similar_products.append(product)
            
            # Fiyata göre sırala
            similar_products.sort(key=lambda x: x["price"])
            
            return similar_products
            
        except Exception as e:
            logger.error(f"Price comparison failed: {str(e)}")
            return []
    
    async def check_stock(self, product_id: str) -> Dict[str, Any]:
        """Stok kontrolü"""
        try:
            product = await self.get_product_details(product_id)
            if product:
                return {
                    "product_id": product_id,
                    "in_stock": product.get("stock", False),
                    "last_checked": datetime.now().isoformat()
                }
            return {"product_id": product_id, "in_stock": False, "error": "Product not found"}
            
        except Exception as e:
            logger.error(f"Stock check failed: {str(e)}")
            return {"product_id": product_id, "in_stock": False, "error": str(e)}
    
    async def get_recommendations(self, category: str, budget: float = None) -> List[Dict[str, Any]]:
        """Kategori bazlı öneriler"""
        try:
            if category.lower() in self.mock_products:
                products = self.mock_products[category.lower()]
                
                # Bütçe filtresi
                if budget:
                    products = [p for p in products if p["price"] <= budget]
                
                # Rating'e göre sırala
                products.sort(key=lambda x: x["rating"], reverse=True)
                
                return products[:3]  # En iyi 3 ürün
            
            return []
            
        except Exception as e:
            logger.error(f"Recommendations failed: {str(e)}")
            return []
    
    async def get_trending_products(self, category: str = None) -> List[Dict[str, Any]]:
        """Trend ürünler"""
        try:
            trending = []
            
            if category and category.lower() in self.mock_products:
                products = self.mock_products[category.lower()]
            else:
                # Tüm kategorilerden
                products = []
                for cat_products in self.mock_products.values():
                    products.extend(cat_products)
            
            # Rating'e göre sırala
            products.sort(key=lambda x: x["rating"], reverse=True)
            
            return products[:5]  # En popüler 5 ürün
            
        except Exception as e:
            logger.error(f"Trending products fetch failed: {str(e)}")
            return [] 