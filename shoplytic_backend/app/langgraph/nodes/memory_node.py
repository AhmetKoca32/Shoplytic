from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import logging
import json
import hashlib

logger = logging.getLogger(__name__)

class MemoryNode:
    """MCP (MessageContextPersistence) hafıza yönetimi node'u"""
    
    def __init__(self):
        self.name = "memory_node"
        # Basit in-memory storage (production'da Redis/DB kullanılacak)
        self.memory_store = {}
        self.conversation_history = {}
        self.user_preferences = {}
        self.workflow_context = {}
    
    async def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        return await self.run(state)

    async def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Memory node'unu çalıştır"""
        logger.info(f"Memory node başlatıldı - Workflow ID: {state.get('workflow_id')}")
        
        try:
            # Execution step'i ekle
            execution_steps = state.get("execution_steps", [])
            execution_steps.append({
                "node": "memory",
                "timestamp": datetime.now().isoformat(),
                "status": "started"
            })
            
            user_id = state.get("user_id")
            workflow_type = state.get("workflow_type", "")
            processed_data = state.get("processed_data", {})
            
            # Hafıza bağlamını oluştur
            memory_context = await self._build_memory_context(
                user_id=user_id,
                workflow_type=workflow_type,
                current_data=processed_data
            )
            
            # Kullanıcı tercihlerini yükle
            user_preferences = await self._load_user_preferences(user_id)
            
            # Konverşasyon geçmişini yükle
            conversation_history = await self._load_conversation_history(user_id, limit=5)
            
            # Benzer workflow'ları bul
            similar_workflows = await self._find_similar_workflows(
                workflow_type=workflow_type,
                current_data=processed_data,
                user_id=user_id
            )
            
            # Memory context'i birleştir
            complete_memory_context = {
                "user_preferences": user_preferences,
                "conversation_history": conversation_history,
                "similar_workflows": similar_workflows,
                "workflow_patterns": memory_context.get("patterns", []),
                "contextual_insights": memory_context.get("insights", []),
                "last_updated": datetime.now().isoformat()
            }
            
            # Mevcut workflow'u hafızaya kaydet
            await self._store_current_workflow(
                user_id=user_id,
                workflow_id=state.get("workflow_id"),
                workflow_type=workflow_type,
                data=processed_data
            )
            
            # Başarılı tamamlanma
            execution_steps.append({
                "node": "memory",
                "timestamp": datetime.now().isoformat(),
                "status": "completed",
                "details": f"Memory context loaded: {len(conversation_history)} conversations, {len(similar_workflows)} similar workflows"
            })
            
            logger.info(f"Memory node tamamlandı - User: {user_id}, Context size: {len(str(complete_memory_context))}")
            
            return {
                **state,
                "memory_context": complete_memory_context,
                "execution_steps": execution_steps
            }
            
        except Exception as e:
            logger.error(f"Memory node hatası: {str(e)}")
            
            execution_steps.append({
                "node": "memory",
                "timestamp": datetime.now().isoformat(),
                "status": "error",
                "error": str(e)
            })
            
            # Hata durumunda boş context döndür
            return {
                **state,
                "memory_context": {
                    "user_preferences": {},
                    "conversation_history": [],
                    "similar_workflows": [],
                    "workflow_patterns": [],
                    "contextual_insights": [],
                    "error": str(e)
                },
                "execution_steps": execution_steps
            }
    
    async def _build_memory_context(
        self, 
        user_id: Optional[str], 
        workflow_type: str, 
        current_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Hafıza bağlamını oluştur"""
        
        context = {
            "patterns": [],
            "insights": []
        }
        
        if not user_id:
            return context
        
        # Kullanıcının geçmiş davranış desenlerini analiz et
        user_patterns = await self._analyze_user_patterns(user_id, workflow_type)
        context["patterns"] = user_patterns
        
        # Bağlamsal öngörüler oluştur
        insights = await self._generate_contextual_insights(
            user_id=user_id,
            workflow_type=workflow_type,
            current_data=current_data,
            patterns=user_patterns
        )
        context["insights"] = insights
        
        return context
    
    async def _load_user_preferences(self, user_id: Optional[str]) -> Dict[str, Any]:
        """Kullanıcı tercihlerini yükle"""
        if not user_id:
            return {}
        
        # Memory store'dan kullanıcı tercihlerini getir
        preferences = self.user_preferences.get(user_id, {})
        
        # Varsayılan tercihler
        default_preferences = {
            "preferred_categories": [],
            "price_range": {"min": 0, "max": 1000},
            "brand_preferences": [],
            "recommendation_style": "balanced",  # conservative, balanced, aggressive
            "language": "tr",
            "notification_preferences": {
                "email": True,
                "sms": False,
                "push": True
            }
        }
        
        # Mevcut tercihlerle varsayılanları birleştir
        return {**default_preferences, **preferences}
    
    async def _load_conversation_history(
        self, 
        user_id: Optional[str], 
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """Konverşasyon geçmişini yükle"""
        if not user_id:
            return []
        
        user_history = self.conversation_history.get(user_id, [])
        
        # Son N konverşasyonu döndür
        return user_history[-limit:] if user_history else []
    
    async def _find_similar_workflows(
        self,
        workflow_type: str,
        current_data: Dict[str, Any],
        user_id: Optional[str],
        limit: int = 3
    ) -> List[Dict[str, Any]]:
        """Benzer workflow'ları bul"""
        
        similar_workflows = []
        
        if not user_id:
            return similar_workflows
        
        user_workflows = self.workflow_context.get(user_id, [])
        
        # Aynı tipte workflow'ları bul
        same_type_workflows = [
            wf for wf in user_workflows 
            if wf.get("workflow_type") == workflow_type
        ]
        
        # Benzerlik skoruna göre sırala (basit implementasyon)
        for workflow in same_type_workflows[-limit:]:
            similarity_score = self._calculate_similarity(
                current_data, 
                workflow.get("data", {})
            )
            
            if similarity_score > 0.3:  # %30'dan fazla benzerlik
                similar_workflows.append({
                    "workflow_id": workflow.get("workflow_id"),
                    "workflow_type": workflow.get("workflow_type"),
                    "similarity_score": similarity_score,
                    "timestamp": workflow.get("timestamp"),
                    "summary": workflow.get("summary", "")
                })
        
        # Benzerlik skoruna göre sırala
        similar_workflows.sort(key=lambda x: x["similarity_score"], reverse=True)
        
        return similar_workflows
    
    def _calculate_similarity(
        self, 
        data1: Dict[str, Any], 
        data2: Dict[str, Any]
    ) -> float:
        """İki veri seti arasındaki benzerliği hesapla"""
        
        # Basit benzerlik hesaplama (production'da daha sofistike olacak)
        common_keys = set(data1.keys()) & set(data2.keys())
        
        if not common_keys:
            return 0.0
        
        similarity_scores = []
        
        for key in common_keys:
            val1, val2 = data1[key], data2[key]
            
            if isinstance(val1, str) and isinstance(val2, str):
                # String benzerliği
                similarity = len(set(val1.lower().split()) & set(val2.lower().split())) / max(len(val1.split()), len(val2.split()), 1)
                similarity_scores.append(similarity)
            
            elif val1 == val2:
                similarity_scores.append(1.0)
            else:
                similarity_scores.append(0.0)
        
        return sum(similarity_scores) / len(similarity_scores) if similarity_scores else 0.0
    
    async def _analyze_user_patterns(self, user_id: str, workflow_type: str) -> List[Dict[str, Any]]:
        """Kullanıcı davranış desenlerini analiz et"""
        
        patterns = []
        user_workflows = self.workflow_context.get(user_id, [])
        
        if len(user_workflows) < 2:
            return patterns
        
        # Zaman desenleri
        time_pattern = self._analyze_time_patterns(user_workflows)
        if time_pattern:
            patterns.append(time_pattern)
        
        # Kategori tercihleri
        category_pattern = self._analyze_category_patterns(user_workflows, workflow_type)
        if category_pattern:
            patterns.append(category_pattern)
        
        return patterns
    
    def _analyze_time_patterns(self, workflows: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Zaman desenlerini analiz et"""
        
        if len(workflows) < 3:
            return None
        
        # Son 3 workflow'un zamanlarını analiz et
        recent_workflows = workflows[-3:]
        hours = []
        
        for wf in recent_workflows:
            timestamp = wf.get("timestamp")
            if timestamp:
                try:
                    dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                    hours.append(dt.hour)
                except:
                    continue
        
        if len(hours) >= 2:
            avg_hour = sum(hours) / len(hours)
            return {
                "type": "time_preference",
                "pattern": f"Genellikle saat {int(avg_hour):02d}:00 civarında aktif",
                "confidence": 0.7,
                "data": {"average_hour": avg_hour, "sample_size": len(hours)}
            }
        
        return None
    
    def _analyze_category_patterns(self, workflows: List[Dict[str, Any]], current_workflow_type: str) -> Optional[Dict[str, Any]]:
        """Kategori tercih desenlerini analiz et"""
        
        # Workflow tiplerini say
        workflow_counts = {}
        for wf in workflows:
            wf_type = wf.get("workflow_type", "unknown")
            workflow_counts[wf_type] = workflow_counts.get(wf_type, 0) + 1
        
        if len(workflow_counts) > 1:
            most_common = max(workflow_counts, key=workflow_counts.get)
            
            return {
                "type": "workflow_preference",
                "pattern": f"En çok '{most_common}' tipinde işlemler yapıyor",
                "confidence": 0.8,
                "data": {
                    "most_common_type": most_common,
                    "usage_count": workflow_counts[most_common],
                    "total_workflows": len(workflows)
                }
            }
        
        return None
    
    async def _generate_contextual_insights(
        self,
        user_id: str,
        workflow_type: str,
        current_data: Dict[str, Any],
        patterns: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Bağlamsal öngörüler oluştur"""
        
        insights = []
        
        # Pattern bazlı öngörüler
        for pattern in patterns:
            if pattern["type"] == "workflow_preference":
                insights.append({
                    "type": "recommendation",
                    "message": f"Bu kullanıcı genellikle {pattern['data']['most_common_type']} işlemleri tercih ediyor",
                    "confidence": pattern["confidence"],
                    "actionable": True
                })
        
        # Workflow tipine özel öngörüler
        if workflow_type == "product_classification":
            insights.append({
                "type": "optimization",
                "message": "Daha hızlı sınıflandırma için ürün başlığı ve açıklaması net olmalı",
                "confidence": 0.9,
                "actionable": True
            })
        
        elif workflow_type == "product_recommendation":
            cart_size = len(current_data.get("cart_items", []))
            if cart_size > 3:
                insights.append({
                    "type": "insight",
                    "message": f"Sepette {cart_size} ürün var, çapraz satış fırsatı yüksek",
                    "confidence": 0.8,
                    "actionable": True
                })
        
        return insights
    
    async def _store_current_workflow(
        self,
        user_id: Optional[str],
        workflow_id: str,
        workflow_type: str,
        data: Dict[str, Any]
    ):
        """Mevcut workflow'u hafızaya kaydet"""
        
        if not user_id:
            return
        
        workflow_record = {
            "workflow_id": workflow_id,
            "workflow_type": workflow_type,
            "data": data,
            "timestamp": datetime.now().isoformat(),
            "summary": self._generate_workflow_summary(workflow_type, data)
        }
        
        # Kullanıcı workflow geçmişine ekle
        if user_id not in self.workflow_context:
            self.workflow_context[user_id] = []
        
        self.workflow_context[user_id].append(workflow_record)
        
        # Son 50 workflow'u sakla (memory management)
        if len(self.workflow_context[user_id]) > 50:
            self.workflow_context[user_id] = self.workflow_context[user_id][-50:]
    
    def _generate_workflow_summary(self, workflow_type: str, data: Dict[str, Any]) -> str:
        """Workflow özeti oluştur"""
        
        if workflow_type == "product_classification":
            title = data.get("product_title", "Bilinmeyen ürün")
            return f"Ürün sınıflandırma: {title[:50]}..."
        
        elif workflow_type == "product_recommendation":
            cart_size = len(data.get("cart_items", []))
            return f"Ürün önerisi: {cart_size} ürünlü sepet"
        
        elif workflow_type == "customer_segmentation":
            return "Müşteri segmentasyon analizi"
        
        else:
            return f"{workflow_type} işlemi"