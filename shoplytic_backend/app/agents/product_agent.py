"""
Product Agent - Ürün analizi ve sınıflandırma uzmanı
"""
import logging
from typing import Dict, Any, List
from datetime import datetime
from .base_agent import BaseAgent, AgentMessage

logger = logging.getLogger(__name__)

class ProductAgent(BaseAgent):
    """Ürün analizi ve sınıflandırma agent'ı"""
    
    def __init__(self, agent_id: str = "product_agent_001"):
        super().__init__(agent_id, "ProductAnalyst")
        self.product_database = {}
        self.category_mapping = {
            "electronics": ["phone", "laptop", "tablet", "computer", "electronic"],
            "fashion": ["clothing", "shoes", "accessories", "fashion", "wear"],
            "home": ["furniture", "kitchen", "home", "garden", "decoration"],
            "books": ["book", "magazine", "publication", "reading"],
            "sports": ["sport", "fitness", "outdoor", "exercise"],
            "beauty": ["cosmetic", "beauty", "skincare", "makeup"],
            "toys": ["toy", "game", "entertainment", "children"],
            "automotive": ["car", "auto", "vehicle", "motorcycle"]
        }
        
        logger.info(f"Product Agent {agent_id} başlatıldı")
    
    def get_capabilities(self) -> List[str]:
        """Agent'ın yeteneklerini döndür"""
        return [
            "product_classification",
            "product_analysis", 
            "category_mapping",
            "feature_extraction",
            "competitor_analysis",
            "trend_analysis"
        ]
    
    async def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Ana görev işleme"""
        task_type = task.get("type", "unknown")
        
        try:
            if task_type == "classify_product":
                return await self._classify_product(task)
            elif task_type == "analyze_product":
                return await self._analyze_product(task)
            elif task_type == "extract_features":
                return await self._extract_features(task)
            elif task_type == "find_competitors":
                return await self._find_competitors(task)
            elif task_type == "analyze_trends":
                return await self._analyze_trends(task)
            else:
                return await self._general_analysis(task)
                
        except Exception as e:
            logger.error(f"Product Agent task işleme hatası: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "agent_id": self.agent_id
            }
    
    async def _classify_product(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Ürün sınıflandırma"""
        product_data = task.get("product_data", {})
        title = product_data.get("title", "").lower()
        description = product_data.get("description", "").lower()
        
        # Kategori belirleme
        category = "other"
        confidence = 0.0
        
        for cat, keywords in self.category_mapping.items():
            score = 0
            for keyword in keywords:
                if keyword in title or keyword in description:
                    score += 1
            
            if score > 0:
                confidence = score / len(keywords)
                if confidence > 0.3:  # Threshold
                    category = cat
                    break
        
        # AI ile doğrulama
        ai_analysis = await self.think(
            f"Bu ürün '{title}' için en uygun kategori nedir? "
            f"Açıklama: {description}. "
            f"Kategoriler: {list(self.category_mapping.keys())}"
        )
        
        result = {
            "success": True,
            "category": category,
            "confidence": confidence,
            "ai_analysis": ai_analysis,
            "agent_id": self.agent_id,
            "timestamp": datetime.now().isoformat()
        }
        
        # Hafızaya kaydet
        self.update_memory(f"classification_{title[:20]}", result)
        
        return result
    
    async def _analyze_product(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Ürün analizi"""
        product_data = task.get("product_data", {})
        
        # AI analizi
        analysis_prompt = f"""
        Bu ürünü analiz et:
        Başlık: {product_data.get('title', '')}
        Açıklama: {product_data.get('description', '')}
        Fiyat: {product_data.get('price', '')}
        
        Analiz et:
        1. Ürün kalitesi
        2. Fiyat-performans oranı
        3. Hedef müşteri segmenti
        4. Pazarlama potansiyeli
        5. Risk faktörleri
        """
        
        ai_analysis = await self.think(analysis_prompt)
        
        result = {
            "success": True,
            "analysis": ai_analysis,
            "product_id": product_data.get("id"),
            "agent_id": self.agent_id,
            "timestamp": datetime.now().isoformat()
        }
        
        return result
    
    async def _extract_features(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Ürün özelliklerini çıkar"""
        product_data = task.get("product_data", {})
        
        # Özellik çıkarma
        features = []
        description = product_data.get("description", "").lower()
        
        # Basit özellik çıkarma
        feature_keywords = [
            "wifi", "bluetooth", "camera", "battery", "screen", "processor",
            "memory", "storage", "waterproof", "wireless", "smart", "touch"
        ]
        
        for keyword in feature_keywords:
            if keyword in description:
                features.append(keyword)
        
        # AI ile gelişmiş özellik çıkarma
        ai_features = await self.think(
            f"Bu ürün açıklamasından önemli özellikleri çıkar: {description}"
        )
        
        result = {
            "success": True,
            "extracted_features": features,
            "ai_features": ai_features,
            "agent_id": self.agent_id,
            "timestamp": datetime.now().isoformat()
        }
        
        return result
    
    async def _find_competitors(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Rakip ürünleri bul"""
        product_data = task.get("product_data", {})
        
        # Basit rakip analizi
        competitors = []
        category = await self._classify_product({"product_data": product_data})
        
        # Mock rakip verisi
        if category.get("category") == "electronics":
            competitors = [
                {"name": "Samsung Galaxy", "price": 899, "rating": 4.5},
                {"name": "Xiaomi Mi", "price": 699, "rating": 4.2},
                {"name": "OnePlus", "price": 799, "rating": 4.4}
            ]
        
        # AI ile rakip analizi
        ai_competitor_analysis = await self.think(
            f"Bu ürün için rakip analizi yap: {product_data.get('title', '')}"
        )
        
        result = {
            "success": True,
            "competitors": competitors,
            "ai_analysis": ai_competitor_analysis,
            "agent_id": self.agent_id,
            "timestamp": datetime.now().isoformat()
        }
        
        return result
    
    async def _analyze_trends(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Trend analizi"""
        product_data = task.get("product_data", {})
        
        # AI trend analizi
        trend_analysis = await self.think(
            f"Bu ürün için trend analizi yap: {product_data.get('title', '')}"
        )
        
        result = {
            "success": True,
            "trend_analysis": trend_analysis,
            "agent_id": self.agent_id,
            "timestamp": datetime.now().isoformat()
        }
        
        return result
    
    async def _general_analysis(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Genel analiz"""
        return await self._analyze_product(task)
    
    async def get_product_recommendations(self, customer_preferences: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Müşteri tercihlerine göre ürün önerileri"""
        try:
            # Müşteri tercihlerini analiz et
            analysis = await self.think(
                f"Müşteri tercihleri: {customer_preferences}. "
                "Bu müşteri için en uygun ürün türlerini öner."
            )
            
            # Mock öneriler
            recommendations = [
                {"product_id": "rec_001", "reason": "Fiyat uygunluğu", "confidence": 0.8},
                {"product_id": "rec_002", "reason": "Kalite uygunluğu", "confidence": 0.7},
                {"product_id": "rec_003", "reason": "Trend uygunluğu", "confidence": 0.6}
            ]
            
            return {
                "success": True,
                "recommendations": recommendations,
                "ai_analysis": analysis,
                "agent_id": self.agent_id
            }
            
        except Exception as e:
            logger.error(f"Ürün önerisi hatası: {str(e)}")
            return {"success": False, "error": str(e)} 