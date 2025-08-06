"""
LLMNode: LangChain ile entegre çalışan LangGraph LLM Node'u
"""
import logging
import os
import asyncio
from typing import Dict, Any, Optional, List
from app.config.settings import Settings
# Google GenAI kullan
from langchain_google_genai import ChatGoogleGenerativeAI
GEMINI_AVAILABLE = True

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser, StrOutputParser
from pydantic import BaseModel, Field
import json

logger = logging.getLogger(__name__)
settings = Settings()

class ProductClassification(BaseModel):
    """Ürün sınıflandırma çıktısı"""
    category: str = Field(description="Ürün kategorisi")
    confidence: float = Field(description="Sınıflandırma güven oranı (0-1)")
    subcategory: Optional[str] = Field(description="Alt kategori")
    tags: list = Field(description="Ürün etiketleri")

class ProductRecommendation(BaseModel):
    """Ürün öneri çıktısı"""
    recommended_products: list = Field(description="Önerilen ürünler")
    reasoning: str = Field(description="Öneri mantığı")
    confidence: float = Field(description="Öneri güven oranı")

class LLMNode:
    def __init__(self):
        # Hem GEMINI_API_KEY hem de GOOGLE_API_KEY'yi kontrol et
        self.api_key = settings.GEMINI_API_KEY or settings.GOOGLE_API_KEY
        
        # API key debug bilgisi
        logger.info(f"GEMINI_API_KEY: {settings.GEMINI_API_KEY}")
        logger.info(f"GOOGLE_API_KEY: {settings.GOOGLE_API_KEY}")
        logger.info(f"Kullanılan API key: {self.api_key}")
        
        self.llm = None
        
        if self.api_key and GEMINI_AVAILABLE:
            try:
                # Environment variable'ı manuel olarak ayarla
                import os
                os.environ["GOOGLE_API_KEY"] = self.api_key
                
                # LangChain Gemini modeli
                self.llm = ChatGoogleGenerativeAI(
                    model="gemini-2.0-flash",
                    google_api_key=self.api_key,
                    temperature=0.7,
                    max_output_tokens=2048
                )
                logger.info("Gemini AI modeli başarıyla yüklendi.")
            except Exception as e:
                logger.error(f"Gemini AI modeli yüklenemedi: {e}")
                self.llm = None
        elif settings.OPENAI_API_KEY:
            try:
                from langchain_openai import ChatOpenAI
                self.llm = ChatOpenAI(
                    model="gpt-4",
                    temperature=0.7,
                    max_tokens=2048
                )
                logger.info("OpenAI modeli başarıyla yüklendi.")
            except Exception as e:
                logger.error(f"OpenAI modeli yüklenemedi: {e}")
                self.llm = None
        else:
            logger.warning("AI API anahtarı bulunamadı. Mock veri kullanılacak.")
        
        # Output parser'lar
        self.classification_parser = PydanticOutputParser(pydantic_object=ProductClassification)
        self.recommendation_parser = PydanticOutputParser(pydantic_object=ProductRecommendation)
        self.string_parser = StrOutputParser()
        
        # Prompt template'leri
        self._setup_prompt_templates()

    def _setup_prompt_templates(self):
        """Prompt template'lerini hazırla"""
        
        # Ürün sınıflandırma template'i
        self.classification_template = ChatPromptTemplate.from_messages([
            ("system", """Sen bir e-ticaret ürün sınıflandırma uzmanısın. 
            Verilen ürün bilgilerini analiz ederek en uygun kategoriyi belirle.
            
            {format_instructions}
            
            Önceki konuşma geçmişi: {conversation_history}
            Kullanıcı tercihleri: {user_preferences}"""),
            ("human", """Ürün Başlığı: {product_title}
            Ürün Açıklaması: {product_description}
            Ek Bilgiler: {additional_info}
            
            Bu ürünü sınıflandır:""")
        ])
        
        # Ürün öneri template'i
        self.recommendation_template = ChatPromptTemplate.from_messages([
            ("system", """Sen bir e-ticaret öneri sistemi uzmanısın.
            Sepet içeriğine ve kullanıcı tercihlerine göre en uygun ürünleri öner.
            
            {format_instructions}
            
            Kullanıcı geçmişi: {user_history}
            Benzer ürünler: {similar_products}"""),
            ("human", """Sepet İçeriği: {cart_items}
            Kullanıcı Tercihleri: {user_preferences}
            
            Bu kullanıcı için ürün önerileri oluştur:""")
        ])
        
        # Genel analiz template'i
        self.general_template = ChatPromptTemplate.from_messages([
            ("system", """Sen bir e-ticaret AI asistanısın.
            Verilen görevi en iyi şekilde yerine getir.
            
            {format_instructions}
            
            Konuşma geçmişi: {conversation_history}"""),
            ("human", "{task_description}")
        ])
        
        # Mind map generation template'i
        self.mindmap_template = ChatPromptTemplate.from_messages([
            ("system", """Sen bir e-ticaret zihin haritası oluşturma uzmanısın.
            Kullanıcının ihtiyaçlarına göre kategoriler ve ürünler öner.
            
            ÖNEMLİ: Yanıtını SADECE JSON formatında ver, markdown kodu kullanma!
            
            Örnek format:
            {{
                "categories": [
                    {{
                        "name": "Ev Eşyaları",
                        "priority": 1,
                        "products": ["Yatak", "Çalışma Masası", "Mutfak Gereçleri"]
                    }},
                    {{
                        "name": "Teknoloji",
                        "priority": 2,
                        "products": ["Laptop", "Tablet", "Kulaklık"]
                    }}
                ]
            }}
            
            Konuşma geçmişi: {conversation_history}"""),
            ("human", "Kullanıcı ihtiyacı: {user_input}")
        ])

    async def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        return await self.run(state)

    async def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        LangChain ile gelişmiş LLM işlemleri yapar
        """
        workflow_type = state.get("workflow_type", "")
        prompt = state.get("prompt", "")
        processed_data = state.get("processed_data", {})
        memory_context = state.get("memory_context", {})
        
        if not prompt and not processed_data:
            logger.error("LLMNode: prompt ve processed_data eksik!")
            state["llm_error"] = "LLMNode: Giriş verisi eksik."
            return state

        try:
            # Workflow tipine göre farklı işlemler
            if workflow_type == "product_classification":
                result = await self._handle_product_classification(processed_data, memory_context)
            elif workflow_type == "product_recommendation":
                result = await self._handle_product_recommendation(processed_data, memory_context)
            elif workflow_type == "mind_map_generation":
                result = await self._handle_mind_map_generation(processed_data, memory_context)
            else:
                result = await self._handle_general_task(prompt, processed_data, memory_context)
            
            state["llm_output"] = result
            state["llm_error"] = None
            logger.info(f"LLMNode: {workflow_type} işlemi başarıyla tamamlandı.")
            
        except Exception as e:
            logger.exception(f"LLMNode: {workflow_type} işlemi başarısız.")
            state["llm_output"] = None
            state["llm_error"] = str(e)
        
        return state

    async def _handle_product_classification(self, data: Dict[str, Any], memory_context: Dict[str, Any]) -> Dict[str, Any]:
        """Ürün sınıflandırma işlemi"""
        
        if not self.llm:
            # Mock veri döndür
            return {
                "type": "classification",
                "result": {
                    "category": "Elektronik",
                    "confidence": 0.85,
                    "subcategory": "Bilgisayar",
                    "tags": ["laptop", "teknoloji", "bilgisayar"]
                },
                "confidence": 0.85,
                "category": "Elektronik",
                "subcategory": "Bilgisayar",
                "tags": ["laptop", "teknoloji", "bilgisayar"]
            }
        
        # Memory context'ten bilgileri al
        conversation_history = memory_context.get("conversation_history", [])
        user_preferences = memory_context.get("user_preferences", {})
        
        # Prompt'u hazırla
        chain = self.classification_template | self.llm | self.classification_parser
        
        result = await chain.ainvoke({
            "product_title": data.get("product_title", ""),
            "product_description": data.get("product_description", ""),
            "additional_info": data.get("additional_info", ""),
            "format_instructions": self.classification_parser.get_format_instructions(),
            "conversation_history": str(conversation_history[-3:]) if conversation_history else "",
            "user_preferences": str(user_preferences)
        })
        
        return {
            "type": "classification",
            "result": result.dict(),
            "confidence": result.confidence,
            "category": result.category,
            "subcategory": result.subcategory,
            "tags": result.tags
        }

    async def _handle_product_recommendation(self, data: Dict[str, Any], memory_context: Dict[str, Any]) -> Dict[str, Any]:
        """Ürün öneri işlemi"""
        
        if not self.llm:
            logger.error("LLM modeli bulunamadı!")
            return {
                "type": "recommendation",
                "error": "LLM modeli bulunamadı",
                "result": {}
            }
        
        # Memory context'ten bilgileri al
        user_history = memory_context.get("conversation_history", [])
        similar_workflows = memory_context.get("similar_workflows", [])
        
        # Prompt'u hazırla
        chain = self.recommendation_template | self.llm | self.recommendation_parser
        
        result = await chain.ainvoke({
            "cart_items": data.get("cart_items", []),
            "user_preferences": data.get("user_preferences", {}),
            "format_instructions": self.recommendation_parser.get_format_instructions(),
            "user_history": str(user_history[-5:]) if user_history else "",
            "similar_products": str(similar_workflows[-3:]) if similar_workflows else ""
        })
        
        return {
            "type": "recommendation",
            "result": result.dict(),
            "recommended_products": result.recommended_products,
            "reasoning": result.reasoning,
            "confidence": result.confidence
        }

    async def _handle_general_task(self, prompt: str, data: Dict[str, Any], memory_context: Dict[str, Any]) -> Dict[str, Any]:
        """Genel AI görevleri"""
        
        if not self.llm:
            logger.error("LLM modeli bulunamadı!")
            return {
                "type": "general",
                "error": "LLM modeli bulunamadı",
                "result": ""
            }
        
        conversation_history = memory_context.get("conversation_history", [])
        
        # Prompt'u hazırla
        chain = self.general_template | self.llm | self.string_parser
        
        result = await chain.ainvoke({
            "task_description": prompt or str(data),
            "format_instructions": "Yanıtını JSON formatında ver.",
            "conversation_history": str(conversation_history[-3:]) if conversation_history else ""
        })
        
        return {
            "type": "general",
            "result": result,
            "raw_response": result
        }

    async def _handle_mind_map_generation(self, data: Dict[str, Any], memory_context: Dict[str, Any]) -> Dict[str, Any]:
        """Mind map generation işlemi"""
        
        if not self.llm:
            logger.error("LLM modeli bulunamadı!")
            return {
                "type": "mind_map",
                "error": "LLM modeli bulunamadı",
                "result": {}
            }
        
        user_input = data.get("user_input", "")
        conversation_history = memory_context.get("conversation_history", [])
        
        try:
            # Mind map template'ini kullan
            chain = self.mindmap_template | self.llm | self.string_parser
            
            result = await chain.ainvoke({
                "user_input": user_input,
                "conversation_history": str(conversation_history[-3:]) if conversation_history else ""
            })
            
            # JSON parse et
            import json
            import re
            
            # Markdown kod bloklarını temizle
            cleaned_result = result.strip()
            if cleaned_result.startswith("```json"):
                cleaned_result = cleaned_result[7:]  # ```json kısmını kaldır
            if cleaned_result.startswith("```"):
                cleaned_result = cleaned_result[3:]  # ``` kısmını kaldır
            if cleaned_result.endswith("```"):
                cleaned_result = cleaned_result[:-3]  # Sondaki ``` kısmını kaldır
            
            cleaned_result = cleaned_result.strip()
            
            try:
                mind_map_data = json.loads(cleaned_result)
                
                # E-ticaret ürünlerini çek
                if mind_map_data.get('categories'):
                    await self._enrich_categories_with_products(mind_map_data['categories'])
                
                return {
                    "type": "mind_map",
                    "result": mind_map_data,
                    "raw_response": result
                }
            except json.JSONDecodeError as e:
                logger.error(f"JSON parse hatası: {e}")
                logger.error(f"Temizlenmiş yanıt: {cleaned_result}")
                # JSON parse edilemezse raw response'u döndür
                return {
                    "type": "mind_map",
                    "result": {"categories": []},
                    "raw_response": result
                }
                
        except Exception as e:
            logger.error(f"Mind map generation hatası: {e}")
            return {
                "type": "mind_map",
                "error": str(e),
                "result": {}
            }
    
    async def _enrich_categories_with_products(self, categories: List[Dict[str, Any]]):
        """Kategorileri e-ticaret ürünleri ile zenginleştir"""
        try:
            # E-ticaret API'leri geçici olarak devre dışı, gerçekçi demo ürünler kullan
            logger.info("E-ticaret API'leri geçici olarak devre dışı - gerçekçi demo ürünler kullanılıyor")
            
            for category in categories:
                category_name = category.get('name', '')
                products = category.get('products', [])
                
                if products:
                    # Gerçekçi demo ürünler ekle
                    category['ecommerce_products'] = self._get_demo_products(category_name, products)
                    logger.info(f"Kategori '{category_name}' için gerçekçi demo ürünler eklendi")
            
        except Exception as e:
            logger.error(f"Ürün zenginleştirme hatası: {e}")
            # Hata durumunda demo ürünler ekle
            for category in categories:
                category['ecommerce_products'] = self._get_demo_products(category.get('name', ''), category.get('products', []))
    
    def _get_demo_products(self, category_name: str, products: List[str]) -> List[Dict[str, Any]]:
        """Gerçekçi demo ürünler oluştur"""
        demo_products = []
        
        # Kategori bazlı gerçekçi ürün verileri
        category_data = {
            "Elektronik": {
                "price_range": (800, 8000),
                "platforms": ["Trendyol", "Hepsiburada", "Amazon"],
                "brands": ["Samsung", "Apple", "Xiaomi", "Huawei", "Sony"],
                "suffixes": ["Pro", "Max", "Ultra", "Premium", "Smart"],
                "image_keywords": ["smartphone", "laptop", "electronics", "gadget", "tech"]
            },
            "Giyim": {
                "price_range": (80, 800),
                "platforms": ["Trendyol", "Hepsiburada", "Zara", "H&M"],
                "brands": ["Nike", "Adidas", "Puma", "Under Armour", "New Balance"],
                "suffixes": ["Sport", "Casual", "Elegant", "Comfort", "Style"],
                "image_keywords": ["clothing", "fashion", "shirt", "dress", "shoes"]
            },
            "Ev ve Yaşam": {
                "price_range": (150, 1500),
                "platforms": ["IKEA", "Hepsiburada", "Trendyol", "Amazon"],
                "brands": ["IKEA", "Philips", "Bosch", "Siemens", "LG"],
                "suffixes": ["Home", "Living", "Comfort", "Modern", "Elegant"],
                "image_keywords": ["furniture", "home", "kitchen", "bedroom", "living"]
            },
            "Kişisel Bakım": {
                "price_range": (50, 400),
                "platforms": ["Trendyol", "Hepsiburada", "Douglas", "Sephora"],
                "brands": ["L'Oreal", "Nivea", "Dove", "Garnier", "Neutrogena"],
                "suffixes": ["Care", "Beauty", "Natural", "Organic", "Premium"],
                "image_keywords": ["cosmetics", "beauty", "skincare", "makeup", "perfume"]
            },
            "Kitap ve Kırtasiye": {
                "price_range": (30, 300),
                "platforms": ["Kitap Yurdu", "Hepsiburada", "Trendyol", "Amazon"],
                "brands": ["Penguin", "Can", "Yapı Kredi", "İş Bankası", "Remzi"],
                "suffixes": ["Classic", "Modern", "Educational", "Creative", "Inspirational"],
                "image_keywords": ["book", "stationery", "pen", "notebook", "office"]
            },
            "Spor ve Outdoor": {
                "price_range": (120, 1200),
                "platforms": ["Decathlon", "Trendyol", "Hepsiburada", "Amazon"],
                "brands": ["Nike", "Adidas", "Puma", "Under Armour", "Columbia"],
                "suffixes": ["Sport", "Active", "Performance", "Outdoor", "Adventure"],
                "image_keywords": ["sports", "fitness", "outdoor", "exercise", "gym"]
            }
        }
        
        cat_data = category_data.get(category_name, {
            "price_range": (100, 1000),
            "platforms": ["Trendyol", "Hepsiburada", "Amazon"],
            "brands": ["Generic", "Premium", "Quality", "Best", "Top"],
            "suffixes": ["Pro", "Max", "Premium", "Quality", "Best"]
        })
        
        min_price, max_price = cat_data["price_range"]
        platforms = cat_data["platforms"]
        brands = cat_data["brands"]
        suffixes = cat_data["suffixes"]
        
        for i, product_name in enumerate(products[:10]):  # 10 ürün
            import random
            
            # Gerçekçi fiyat hesaplama
            base_price = min_price + (i * (max_price - min_price) // 3)
            price_variation = random.randint(-50, 100)
            price = max(base_price + price_variation, min_price)
            
            # Gerçekçi rating
            rating = round(3.5 + (i * 0.3) + random.uniform(-0.2, 0.2), 1)
            rating = min(max(rating, 3.0), 5.0)
            
            # Rastgele seçimler
            platform = random.choice(platforms)
            brand = random.choice(brands)
            suffix = random.choice(suffixes)
            
            # Gerçekçi ürün adı
            product_title = f"{brand} {product_name} {suffix}"
            
            # Kategori bazlı gerçek ürün resimleri (Unsplash API)
            image_keywords = cat_data.get("image_keywords", ["product", "item", "shopping"])
            keyword = random.choice(image_keywords)
            
            image_urls = [
                f"https://source.unsplash.com/300x300/?{product_name.lower().replace(' ', '+')}",
                f"https://source.unsplash.com/300x300/?{keyword}",
                f"https://source.unsplash.com/300x300/?{category_name.lower().replace(' ', '+')}",
                f"https://source.unsplash.com/300x300/?{keyword}+product",
                f"https://source.unsplash.com/300x300/?{keyword}+item"
            ]
            
            demo_products.append({
                "id": f"demo_{category_name}_{i}_{random.randint(1000, 9999)}",
                "name": product_title,
                "price": price,
                "platform": platform,
                "rating": rating,
                "stock": random.choice([True, True, True, False]),  # %75 stokta
                "url": f"https://{platform.lower().replace(' ', '')}.com/{product_name.lower().replace(' ', '-')}",
                "image": random.choice(image_urls),
                "category": category_name,
                "description": f"{brand} marka {product_name} {suffix} - {category_name} kategorisinde en çok tercih edilen ürünlerden biri. Yüksek kalite ve uygun fiyat garantisi."
            })
        
        return demo_products

    async def get_model_info(self) -> Dict[str, Any]:
        """Model bilgilerini döndür"""
        return {
            "model_name": "gemini-2.0-flash",
            "provider": "google",
            "max_tokens": 2048,
            "temperature": 0.7,
            "supports_streaming": True,
            "supports_tools": True
        }
