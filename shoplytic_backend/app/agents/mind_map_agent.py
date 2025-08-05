"""
Mind Map Agent - Zihin haritası oluşturan uzman
"""
import logging
from typing import Dict, Any, List
from datetime import datetime
from .base_agent import BaseAgent, AgentMessage

logger = logging.getLogger(__name__)

class MindMapAgent(BaseAgent):
    """Zihin haritası oluşturma agent'ı"""
    
    def __init__(self, agent_id: str = "mindmap_agent_001"):
        super().__init__(agent_id, "MindMapGenerator")
        
        # Kategori şablonları
        self.category_templates = {
            "university_student": {
                "academic": ["laptop", "tablet", "çanta", "defter", "kalem", "kırtasiye"],
                "clothing": ["günlük kıyafet", "resmi kıyafet", "spor kıyafet", "ayakkabı"],
                "personal_care": ["şampuan", "diş fırçası", "nemlendirici", "parfüm"],
                "home": ["battaniye", "yastık", "havlu", "çarşaf", "ısıtıcı"],
                "technology": ["telefon", "kulaklık", "powerbank", "şarj aleti"],
                "food": ["su termosu", "yemek kutusu", "atıştırmalık"]
            },
            "new_job": {
                "professional": ["iş kıyafeti", "ayakkabı", "çanta", "aksesuar"],
                "technology": ["laptop", "telefon", "kulaklık", "tablet"],
                "office": ["kalem", "defter", "dosya", "organizatör"],
                "personal_care": ["makyaj", "parfüm", "saç bakım", "cilt bakım"]
            },
            "new_home": {
                "furniture": ["yatak", "dolap", "masa", "sandalye", "koltuk"],
                "kitchen": ["buzdolabı", "çamaşır makinesi", "mutfak eşyası"],
                "bathroom": ["havlu", "banyo takımı", "temizlik malzemesi"],
                "bedroom": ["çarşaf", "yastık", "battaniye", "perde"],
                "living": ["tv", "ses sistemi", "dekorasyon", "aydınlatma"]
            }
        }
        
        logger.info(f"Mind Map Agent {agent_id} başlatıldı")
    
    def get_capabilities(self) -> List[str]:
        """Agent'ın yeteneklerini döndür"""
        return [
            "mind_map_generation",
            "category_organization",
            "priority_ranking",
            "visual_structure",
            "interactive_nodes",
            "dynamic_updates"
        ]
    
    async def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Ana görev işleme"""
        task_type = task.get("type", "unknown")
        
        try:
            if task_type == "generate_mind_map":
                return await self._generate_mind_map(task)
            elif task_type == "update_mind_map":
                return await self._update_mind_map(task)
            elif task_type == "add_category":
                return await self._add_category(task)
            else:
                return await self._general_mind_map_task(task)
                
        except Exception as e:
            logger.error(f"Mind Map Agent task işleme hatası: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "agent_id": self.agent_id
            }
    
    async def _generate_mind_map(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Zihin haritası oluştur"""
        context_analysis = task.get("context_analysis", {})
        extracted_needs = task.get("extracted_needs", {})
        
        # Merkez konu
        central_topic = self._determine_central_topic(context_analysis)
        
        # Ana kategorileri oluştur
        main_categories = await self._create_main_categories(context_analysis, extracted_needs)
        
        # Alt kategorileri oluştur
        sub_categories = await self._create_sub_categories(main_categories, context_analysis)
        
        # Öncelik sıralaması
        prioritized_categories = self._prioritize_categories(main_categories, context_analysis)
        
        # AI ile harita analizi
        map_analysis = await self.think(
            f"Bu zihin haritası için analiz yap:\n"
            f"Merkez konu: {central_topic}\n"
            f"Ana kategoriler: {[cat['name'] for cat in main_categories]}\n"
            f"Bağlam: {context_analysis}\n"
            f"İhtiyaçlar: {extracted_needs}"
        )
        
        # Zihin haritası yapısı
        mind_map = {
            "id": f"mindmap_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "central_topic": central_topic,
            "main_categories": main_categories,
            "sub_categories": sub_categories,
            "prioritized_categories": prioritized_categories,
            "metadata": {
                "created_at": datetime.now().isoformat(),
                "context": context_analysis,
                "needs": extracted_needs,
                "ai_analysis": map_analysis
            }
        }
        
        result = {
            "success": True,
            "mind_map": mind_map,
            "agent_id": self.agent_id,
            "timestamp": datetime.now().isoformat()
        }
        
        return result
    
    async def _update_mind_map(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Zihin haritasını güncelle"""
        existing_map = task.get("existing_mind_map", {})
        new_context = task.get("new_context", {})
        
        # Mevcut haritayı güncelle
        updated_map = existing_map.copy()
        
        # Yeni kategoriler ekle
        if new_context:
            new_categories = await self._create_main_categories(new_context, {})
            updated_map["main_categories"].extend(new_categories)
        
        # Öncelikleri yeniden hesapla
        updated_map["prioritized_categories"] = self._prioritize_categories(
            updated_map["main_categories"], new_context
        )
        
        result = {
            "success": True,
            "updated_mind_map": updated_map,
            "agent_id": self.agent_id,
            "timestamp": datetime.now().isoformat()
        }
        
        return result
    
    async def _add_category(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Yeni kategori ekle"""
        category_name = task.get("category_name", "")
        category_items = task.get("category_items", [])
        priority = task.get("priority", "medium")
        
        new_category = {
            "name": category_name,
            "items": category_items,
            "priority": priority,
            "created_at": datetime.now().isoformat()
        }
        
        result = {
            "success": True,
            "new_category": new_category,
            "agent_id": self.agent_id,
            "timestamp": datetime.now().isoformat()
        }
        
        return result
    
    async def _general_mind_map_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Genel zihin haritası görevi"""
        return await self._generate_mind_map(task)
    
    def _determine_central_topic(self, context_analysis: Dict[str, Any]) -> str:
        """Merkez konuyu belirle"""
        situation = context_analysis.get("situation", {}).get("type", "")
        location = context_analysis.get("location", {}).get("city", "")
        
        if situation == "university_student":
            return f"{location.title()} Üniversite Hazırlığı"
        elif situation == "new_job":
            return f"{location.title()} İş Hayatı Hazırlığı"
        elif situation == "new_home":
            return f"{location.title()} Ev Hazırlığı"
        else:
            return "Kullanıcı İhtiyaçları"
    
    async def _create_main_categories(self, context_analysis: Dict[str, Any], extracted_needs: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Ana kategorileri oluştur"""
        situation = context_analysis.get("situation", {}).get("type", "")
        location = context_analysis.get("location", {}).get("city", "")
        seasonal_needs = context_analysis.get("seasonal_needs", [])
        
        categories = []
        
        # Durum bazlı kategoriler
        if situation in self.category_templates:
            for category_name, items in self.category_templates[situation].items():
                categories.append({
                    "name": self._format_category_name(category_name),
                    "items": items,
                    "priority": "high" if category_name in ["academic", "professional", "furniture"] else "medium",
                    "type": "situation_based"
                })
        
        # Lokasyon bazlı kategoriler
        if location:
            location_categories = self._get_location_categories(location, seasonal_needs)
            categories.extend(location_categories)
        
        # Mevsimsel kategoriler
        if seasonal_needs:
            categories.append({
                "name": "Mevsimsel İhtiyaçlar",
                "items": seasonal_needs,
                "priority": "high",
                "type": "seasonal"
            })
        
        return categories
    
    async def _create_sub_categories(self, main_categories: List[Dict[str, Any]], context_analysis: Dict[str, Any]) -> Dict[str, List[Dict[str, Any]]]:
        """Alt kategorileri oluştur"""
        sub_categories = {}
        
        for category in main_categories:
            category_name = category["name"]
            items = category["items"]
            
            # Her kategori için alt kategoriler
            sub_items = []
            for item in items:
                sub_items.append({
                    "name": item,
                    "type": "product",
                    "clickable": True,
                    "priority": category.get("priority", "medium")
                })
            
            sub_categories[category_name] = sub_items
        
        return sub_categories
    
    def _prioritize_categories(self, categories: List[Dict[str, Any]], context_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Kategorileri öncelik sırasına göre sırala"""
        # Öncelik puanı hesapla
        for category in categories:
            priority_score = 0
            
            # Yüksek öncelikli kategoriler
            if category.get("priority") == "high":
                priority_score += 10
            
            # Durum bazlı öncelik
            if category.get("type") == "situation_based":
                priority_score += 5
            
            # Mevsimsel öncelik
            if category.get("type") == "seasonal":
                priority_score += 8
            
            category["priority_score"] = priority_score
        
        # Öncelik skoruna göre sırala
        return sorted(categories, key=lambda x: x.get("priority_score", 0), reverse=True)
    
    def _format_category_name(self, category_name: str) -> str:
        """Kategori adını formatla"""
        name_mapping = {
            "academic": "Akademik Malzemeler",
            "clothing": "Giyim",
            "personal_care": "Kişisel Bakım",
            "home": "Ev Eşyaları",
            "technology": "Teknoloji",
            "food": "Yiyecek & İçecek",
            "professional": "Profesyonel Giyim",
            "office": "Ofis Malzemeleri",
            "furniture": "Mobilya",
            "kitchen": "Mutfak",
            "bathroom": "Banyo",
            "bedroom": "Yatak Odası",
            "living": "Oturma Odası"
        }
        
        return name_mapping.get(category_name, category_name.title())
    
    def _get_location_categories(self, location: str, seasonal_needs: List[str]) -> List[Dict[str, Any]]:
        """Lokasyon bazlı kategoriler"""
        categories = []
        
        if location == "adana":
            categories.append({
                "name": "Adana Özel İhtiyaçlar",
                "items": ["nemlendirici", "klima", "hafif mont", "güneş kremi"],
                "priority": "medium",
                "type": "location_specific"
            })
        elif location == "ankara":
            categories.append({
                "name": "Ankara Özel İhtiyaçlar",
                "items": ["çok kalın mont", "ısıtıcı", "nemlendirici", "kalın çorap"],
                "priority": "high",
                "type": "location_specific"
            })
        elif location == "istanbul":
            categories.append({
                "name": "İstanbul Özel İhtiyaçlar",
                "items": ["yağmurluk", "şemsiye", "kalın mont", "nemlendirici"],
                "priority": "medium",
                "type": "location_specific"
            })
        
        return categories 