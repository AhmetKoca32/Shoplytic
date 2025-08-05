"""
Customer Agent - Müşteri analizi ve segmentasyon uzmanı
"""
import logging
from typing import Dict, Any, List
from datetime import datetime
from .base_agent import BaseAgent, AgentMessage

logger = logging.getLogger(__name__)

class CustomerAgent(BaseAgent):
    """Müşteri analizi ve segmentasyon agent'ı"""
    
    def __init__(self, agent_id: str = "customer_agent_001"):
        super().__init__(agent_id, "CustomerAnalyst")
        
        # Müşteri segmentleri
        self.customer_segments = {
            "premium": {
                "criteria": {"min_spend": 1000, "loyalty_score": 0.8},
                "characteristics": ["yüksek gelir", "kalite odaklı", "marka sadık"]
            },
            "regular": {
                "criteria": {"min_spend": 500, "loyalty_score": 0.6},
                "characteristics": ["orta gelir", "fiyat duyarlı", "çeşitlilik arayan"]
            },
            "budget": {
                "criteria": {"max_spend": 300, "loyalty_score": 0.4},
                "characteristics": ["düşük gelir", "indirim odaklı", "temel ihtiyaç"]
            },
            "new": {
                "criteria": {"visit_count": 1, "loyalty_score": 0.2},
                "characteristics": ["yeni müşteri", "keşif aşamasında", "rehberlik gerekli"]
            }
        }
        
        logger.info(f"Customer Agent {agent_id} başlatıldı")
    
    def get_capabilities(self) -> List[str]:
        """Agent'ın yeteneklerini döndür"""
        return [
            "customer_segmentation",
            "behavior_analysis",
            "preference_analysis",
            "loyalty_scoring",
            "recommendation_engine",
            "churn_prediction",
            "lifetime_value_calculation"
        ]
    
    async def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Ana görev işleme"""
        task_type = task.get("type", "unknown")
        
        try:
            if task_type == "segment_customer":
                return await self._segment_customer(task)
            elif task_type == "analyze_behavior":
                return await self._analyze_behavior(task)
            elif task_type == "predict_churn":
                return await self._predict_churn(task)
            elif task_type == "calculate_ltv":
                return await self._calculate_lifetime_value(task)
            elif task_type == "generate_recommendations":
                return await self._generate_recommendations(task)
            else:
                return await self._general_customer_analysis(task)
                
        except Exception as e:
            logger.error(f"Customer Agent task işleme hatası: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "agent_id": self.agent_id
            }
    
    async def _segment_customer(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Müşteri segmentasyonu"""
        customer_data = task.get("customer_data", {})
        
        # Segmentasyon kriterleri
        total_spend = customer_data.get("total_spend", 0)
        visit_count = customer_data.get("visit_count", 0)
        loyalty_score = customer_data.get("loyalty_score", 0.0)
        avg_order_value = customer_data.get("avg_order_value", 0)
        
        # Segment belirleme
        segment = "new"
        confidence = 0.0
        
        if total_spend >= 1000 and loyalty_score >= 0.8:
            segment = "premium"
            confidence = 0.9
        elif total_spend >= 500 and loyalty_score >= 0.6:
            segment = "regular"
            confidence = 0.8
        elif total_spend <= 300 or loyalty_score <= 0.4:
            segment = "budget"
            confidence = 0.7
        elif visit_count <= 2:
            segment = "new"
            confidence = 0.6
        
        # AI ile segmentasyon doğrulama
        ai_analysis = await self.think(
            f"Müşteri verileri: Toplam harcama={total_spend}, Ziyaret={visit_count}, "
            f"Sadakat={loyalty_score}, Ortalama sipariş={avg_order_value}. "
            f"Bu müşteri hangi segmentte olmalı? Segmentler: {list(self.customer_segments.keys())}"
        )
        
        result = {
            "success": True,
            "segment": segment,
            "confidence": confidence,
            "characteristics": self.customer_segments[segment]["characteristics"],
            "ai_analysis": ai_analysis,
            "agent_id": self.agent_id,
            "timestamp": datetime.now().isoformat()
        }
        
        # Hafızaya kaydet
        self.update_memory(f"segment_{customer_data.get('id', 'unknown')}", result)
        
        return result
    
    async def _analyze_behavior(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Müşteri davranış analizi"""
        customer_data = task.get("customer_data", {})
        purchase_history = customer_data.get("purchase_history", [])
        
        # Davranış analizi
        behavior_insights = {
            "preferred_categories": self._get_preferred_categories(purchase_history),
            "purchase_frequency": self._calculate_purchase_frequency(purchase_history),
            "price_sensitivity": self._analyze_price_sensitivity(purchase_history),
            "seasonal_patterns": self._analyze_seasonal_patterns(purchase_history)
        }
        
        # AI davranış analizi
        ai_behavior_analysis = await self.think(
            f"Müşteri davranış analizi yap: {purchase_history}. "
            "Bu müşterinin alışveriş alışkanlıkları neler?"
        )
        
        result = {
            "success": True,
            "behavior_insights": behavior_insights,
            "ai_analysis": ai_behavior_analysis,
            "agent_id": self.agent_id,
            "timestamp": datetime.now().isoformat()
        }
        
        return result
    
    async def _predict_churn(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Müşteri kaybı tahmini"""
        customer_data = task.get("customer_data", {})
        
        # Churn risk faktörleri
        last_purchase_days = customer_data.get("days_since_last_purchase", 0)
        complaint_count = customer_data.get("complaint_count", 0)
        loyalty_score = customer_data.get("loyalty_score", 0.0)
        
        # Risk hesaplama
        churn_risk = 0.0
        if last_purchase_days > 90:
            churn_risk += 0.4
        if complaint_count > 2:
            churn_risk += 0.3
        if loyalty_score < 0.3:
            churn_risk += 0.3
        
        churn_risk = min(churn_risk, 1.0)
        
        # AI churn tahmini
        ai_churn_analysis = await self.think(
            f"Bu müşteri kaybı riski analiz et: "
            f"Son alışveriş: {last_purchase_days} gün önce, "
            f"Şikayet sayısı: {complaint_count}, "
            f"Sadakat skoru: {loyalty_score}"
        )
        
        result = {
            "success": True,
            "churn_risk": churn_risk,
            "risk_factors": {
                "days_since_last_purchase": last_purchase_days,
                "complaint_count": complaint_count,
                "loyalty_score": loyalty_score
            },
            "ai_analysis": ai_churn_analysis,
            "agent_id": self.agent_id,
            "timestamp": datetime.now().isoformat()
        }
        
        return result
    
    async def _calculate_lifetime_value(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Müşteri yaşam boyu değeri hesaplama"""
        customer_data = task.get("customer_data", {})
        
        # LTV hesaplama
        avg_order_value = customer_data.get("avg_order_value", 0)
        purchase_frequency = customer_data.get("purchase_frequency", 1)
        customer_lifespan = customer_data.get("customer_lifespan_months", 12)
        
        ltv = avg_order_value * purchase_frequency * customer_lifespan
        
        # AI LTV analizi
        ai_ltv_analysis = await self.think(
            f"Müşteri yaşam boyu değeri analiz et: "
            f"Ortalama sipariş: {avg_order_value}, "
            f"Satın alma sıklığı: {purchase_frequency}, "
            f"Müşteri ömrü: {customer_lifespan} ay"
        )
        
        result = {
            "success": True,
            "lifetime_value": ltv,
            "calculation_factors": {
                "avg_order_value": avg_order_value,
                "purchase_frequency": purchase_frequency,
                "customer_lifespan": customer_lifespan
            },
            "ai_analysis": ai_ltv_analysis,
            "agent_id": self.agent_id,
            "timestamp": datetime.now().isoformat()
        }
        
        return result
    
    async def _generate_recommendations(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Kişiselleştirilmiş öneriler oluştur"""
        customer_data = task.get("customer_data", {})
        segment = customer_data.get("segment", "regular")
        
        # Segment bazlı öneriler
        recommendations = []
        
        if segment == "premium":
            recommendations = [
                {"type": "premium_products", "reason": "Yüksek kalite ürünler", "priority": "high"},
                {"type": "exclusive_offers", "reason": "Özel indirimler", "priority": "medium"},
                {"type": "loyalty_rewards", "reason": "Sadakat programı", "priority": "high"}
            ]
        elif segment == "regular":
            recommendations = [
                {"type": "popular_products", "reason": "Popüler ürünler", "priority": "high"},
                {"type": "seasonal_offers", "reason": "Sezonluk indirimler", "priority": "medium"},
                {"type": "cross_sell", "reason": "İlgili ürünler", "priority": "low"}
            ]
        elif segment == "budget":
            recommendations = [
                {"type": "discount_products", "reason": "İndirimli ürünler", "priority": "high"},
                {"type": "bundle_offers", "reason": "Paket teklifleri", "priority": "high"},
                {"type": "clearance_sales", "reason": "Temizlik satışları", "priority": "medium"}
            ]
        
        # AI öneri analizi
        ai_recommendation_analysis = await self.think(
            f"Bu müşteri için öneri stratejisi oluştur: Segment={segment}, "
            f"Tercihler={customer_data.get('preferences', {})}"
        )
        
        result = {
            "success": True,
            "recommendations": recommendations,
            "ai_analysis": ai_recommendation_analysis,
            "agent_id": self.agent_id,
            "timestamp": datetime.now().isoformat()
        }
        
        return result
    
    async def _general_customer_analysis(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Genel müşteri analizi"""
        return await self._segment_customer(task)
    
    def _get_preferred_categories(self, purchase_history: List[Dict[str, Any]]) -> List[str]:
        """Tercih edilen kategorileri bul"""
        category_counts = {}
        for purchase in purchase_history:
            category = purchase.get("category", "unknown")
            category_counts[category] = category_counts.get(category, 0) + 1
        
        # En çok alınan 3 kategori
        sorted_categories = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)
        return [cat for cat, count in sorted_categories[:3]]
    
    def _calculate_purchase_frequency(self, purchase_history: List[Dict[str, Any]]) -> float:
        """Satın alma sıklığını hesapla"""
        if not purchase_history:
            return 0.0
        
        total_days = 365  # Varsayılan 1 yıl
        return len(purchase_history) / (total_days / 30)  # Aylık ortalama
    
    def _analyze_price_sensitivity(self, purchase_history: List[Dict[str, Any]]) -> str:
        """Fiyat duyarlılığını analiz et"""
        if not purchase_history:
            return "unknown"
        
        avg_price = sum(p.get("price", 0) for p in purchase_history) / len(purchase_history)
        
        if avg_price > 500:
            return "low"  # Düşük fiyat duyarlılığı
        elif avg_price > 200:
            return "medium"  # Orta fiyat duyarlılığı
        else:
            return "high"  # Yüksek fiyat duyarlılığı
    
    def _analyze_seasonal_patterns(self, purchase_history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Sezonluk alışveriş kalıplarını analiz et"""
        monthly_counts = {}
        for purchase in purchase_history:
            month = purchase.get("month", 1)
            monthly_counts[month] = monthly_counts.get(month, 0) + 1
        
        return {
            "peak_months": [m for m, c in monthly_counts.items() if c > 2],
            "slow_months": [m for m, c in monthly_counts.items() if c <= 1],
            "monthly_distribution": monthly_counts
        } 