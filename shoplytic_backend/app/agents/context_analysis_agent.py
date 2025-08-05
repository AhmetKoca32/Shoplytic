"""
Context Analysis Agent - Kullanıcının durumunu analiz eden uzman
"""
import logging
from typing import Dict, Any, List
from datetime import datetime
from .base_agent import BaseAgent, AgentMessage

logger = logging.getLogger(__name__)

class ContextAnalysisAgent(BaseAgent):
    """Kullanıcı durumu analiz agent'ı"""
    
    def __init__(self, agent_id: str = "context_agent_001"):
        super().__init__(agent_id, "ContextAnalyst")
        
        # Şehir bilgileri
        self.city_data = {
            "adana": {
                "climate": "subtropical",
                "winter_temp": "5-15°C",
                "summer_temp": "25-40°C",
                "humidity": "high",
                "rainfall": "moderate",
                "special_needs": ["nemlendirici", "klima", "hafif mont"]
            },
            "istanbul": {
                "climate": "temperate",
                "winter_temp": "-5-10°C",
                "summer_temp": "20-35°C",
                "humidity": "moderate",
                "rainfall": "high",
                "special_needs": ["yağmurluk", "kalın mont", "şemsiye"]
            },
            "ankara": {
                "climate": "continental",
                "winter_temp": "-15-5°C",
                "summer_temp": "15-35°C",
                "humidity": "low",
                "rainfall": "low",
                "special_needs": ["çok kalın mont", "nemlendirici", "ısıtıcı"]
            }
        }
        
        # Yaşam durumu analizi
        self.life_situations = {
            "university_student": {
                "needs": ["laptop", "çanta", "defter", "kalem", "kırtasiye"],
                "budget": "limited",
                "lifestyle": "active",
                "priorities": ["pratik", "uygun fiyat", "dayanıklı"]
            },
            "new_job": {
                "needs": ["iş kıyafeti", "laptop", "çanta", "aksesuar"],
                "budget": "moderate",
                "lifestyle": "professional",
                "priorities": ["kalite", "profesyonel görünüm", "konfor"]
            },
            "new_home": {
                "needs": ["mobilya", "ev eşyası", "mutfak", "banyo"],
                "budget": "variable",
                "lifestyle": "settled",
                "priorities": ["fonksiyonel", "uzun ömürlü", "estetik"]
            }
        }
        
        logger.info(f"Context Analysis Agent {agent_id} başlatıldı")
    
    def get_capabilities(self) -> List[str]:
        """Agent'ın yeteneklerini döndür"""
        return [
            "location_analysis",
            "situation_analysis",
            "need_extraction",
            "context_mapping",
            "seasonal_analysis",
            "lifestyle_analysis"
        ]
    
    async def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Ana görev işleme"""
        task_type = task.get("type", "unknown")
        
        try:
            if task_type == "analyze_user_context":
                return await self._analyze_user_context(task)
            elif task_type == "extract_needs":
                return await self._extract_needs(task)
            elif task_type == "generate_context_map":
                return await self._generate_context_map(task)
            else:
                return await self._general_context_analysis(task)
                
        except Exception as e:
            logger.error(f"Context Agent task işleme hatası: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "agent_id": self.agent_id
            }
    
    async def _analyze_user_context(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Kullanıcı durumunu analiz et"""
        user_input = task.get("user_input", "")
        
        # AI ile durum analizi
        context_analysis = await self.think(
            f"Bu kullanıcı durumunu analiz et: '{user_input}'. "
            "Şu bilgileri çıkar:\n"
            "1. Lokasyon (şehir)\n"
            "2. Yaşam durumu (öğrenci, iş, ev vb.)\n"
            "3. Zaman faktörü (mevsim, dönem)\n"
            "4. Özel ihtiyaçlar\n"
            "5. Bütçe durumu\n"
            "6. Öncelikler"
        )
        
        # Lokasyon çıkarma
        location = self._extract_location(user_input)
        location_data = self.city_data.get(location, {})
        
        # Yaşam durumu çıkarma
        situation = self._extract_situation(user_input)
        situation_data = self.life_situations.get(situation, {})
        
        # Mevsim analizi
        seasonal_needs = self._analyze_seasonal_needs(user_input, location)
        
        result = {
            "success": True,
            "context_analysis": {
                "user_input": user_input,
                "location": {
                    "city": location,
                    "climate": location_data.get("climate"),
                    "temperature_range": location_data.get("winter_temp"),
                    "special_needs": location_data.get("special_needs", [])
                },
                "situation": {
                    "type": situation,
                    "needs": situation_data.get("needs", []),
                    "budget": situation_data.get("budget"),
                    "priorities": situation_data.get("priorities", [])
                },
                "seasonal_needs": seasonal_needs,
                "ai_analysis": context_analysis
            },
            "agent_id": self.agent_id,
            "timestamp": datetime.now().isoformat()
        }
        
        return result
    
    async def _extract_needs(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """İhtiyaçları çıkar"""
        context_analysis = task.get("context_analysis", {})
        
        # Temel ihtiyaçlar
        basic_needs = []
        
        # Lokasyon bazlı ihtiyaçlar
        location_needs = context_analysis.get("location", {}).get("special_needs", [])
        basic_needs.extend(location_needs)
        
        # Durum bazlı ihtiyaçlar
        situation_needs = context_analysis.get("situation", {}).get("needs", [])
        basic_needs.extend(situation_needs)
        
        # Mevsimsel ihtiyaçlar
        seasonal_needs = context_analysis.get("seasonal_needs", [])
        basic_needs.extend(seasonal_needs)
        
        # AI ile ihtiyaç analizi
        needs_analysis = await self.think(
            f"Bu durum için ihtiyaç analizi yap: {context_analysis}. "
            "Hangi ürün kategorileri gerekli?"
        )
        
        result = {
            "success": True,
            "extracted_needs": {
                "basic_needs": list(set(basic_needs)),  # Tekrarları kaldır
                "location_specific": location_needs,
                "situation_specific": situation_needs,
                "seasonal": seasonal_needs,
                "ai_analysis": needs_analysis
            },
            "agent_id": self.agent_id,
            "timestamp": datetime.now().isoformat()
        }
        
        return result
    
    async def _generate_context_map(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Bağlam haritası oluştur"""
        context_analysis = task.get("context_analysis", {})
        extracted_needs = task.get("extracted_needs", {})
        
        # Zihin haritası yapısı
        mind_map = {
            "central_topic": "Kullanıcı İhtiyaçları",
            "main_branches": [
                {
                    "name": "Kış Hazırlığı",
                    "items": ["mont", "bot", "atkı", "eldiven", "kalın çorap"],
                    "priority": "high"
                },
                {
                    "name": "Üniversite Malzemeleri",
                    "items": ["laptop", "çanta", "defter", "kalem", "kırtasiye"],
                    "priority": "high"
                },
                {
                    "name": "Ev Eşyaları",
                    "items": ["battaniye", "ısıtıcı", "nemlendirici", "klima"],
                    "priority": "medium"
                },
                {
                    "name": "Kişisel Bakım",
                    "items": ["nemlendirici", "güneş kremi", "şampuan", "diş fırçası"],
                    "priority": "medium"
                }
            ]
        }
        
        # AI ile harita analizi
        map_analysis = await self.think(
            f"Bu bağlam için zihin haritası oluştur: {context_analysis}. "
            "Hangi kategoriler ve alt öğeler gerekli?"
        )
        
        result = {
            "success": True,
            "context_map": {
                "mind_map": mind_map,
                "context_summary": context_analysis,
                "needs_summary": extracted_needs,
                "ai_analysis": map_analysis
            },
            "agent_id": self.agent_id,
            "timestamp": datetime.now().isoformat()
        }
        
        return result
    
    async def _general_context_analysis(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Genel bağlam analizi"""
        return await self._analyze_user_context(task)
    
    def _extract_location(self, text: str) -> str:
        """Metinden lokasyon çıkar"""
        text_lower = text.lower()
        
        for city in self.city_data.keys():
            if city in text_lower:
                return city
        
        return "unknown"
    
    def _extract_situation(self, text: str) -> str:
        """Metinden yaşam durumu çıkar"""
        text_lower = text.lower()
        
        if "üniversite" in text_lower or "okul" in text_lower or "öğrenci" in text_lower:
            return "university_student"
        elif "iş" in text_lower or "çalışma" in text_lower or "kariyer" in text_lower:
            return "new_job"
        elif "ev" in text_lower or "taşınma" in text_lower or "yeni ev" in text_lower:
            return "new_home"
        
        return "unknown"
    
    def _analyze_seasonal_needs(self, text: str, location: str) -> List[str]:
        """Mevsimsel ihtiyaçları analiz et"""
        text_lower = text.lower()
        seasonal_needs = []
        
        # Kış ihtiyaçları
        if any(word in text_lower for word in ["kış", "soğuk", "kar", "don"]):
            seasonal_needs.extend(["kalın mont", "bot", "atkı", "eldiven", "ısıtıcı"])
        
        # Yaz ihtiyaçları
        if any(word in text_lower for word in ["yaz", "sıcak", "güneş"]):
            seasonal_needs.extend(["hafif kıyafet", "güneş kremi", "şapka", "klima"])
        
        # Lokasyon bazlı mevsimsel ihtiyaçlar
        if location == "adana":
            seasonal_needs.extend(["nemlendirici", "hafif mont"])
        elif location == "ankara":
            seasonal_needs.extend(["çok kalın mont", "ısıtıcı"])
        
        return list(set(seasonal_needs))  # Tekrarları kaldır 