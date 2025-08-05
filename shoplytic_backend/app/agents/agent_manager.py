"""
Agent Manager - Tüm AI Agent'ları yöneten merkezi sistem
"""
import logging
import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime
from .base_agent import BaseAgent, AgentMessage
from .product_agent import ProductAgent
from .customer_agent import CustomerAgent
from .context_analysis_agent import ContextAnalysisAgent
from .mind_map_agent import MindMapAgent

logger = logging.getLogger(__name__)

class AgentManager:
    """AI Agent'ları yöneten merkezi sistem"""
    
    def __init__(self):
        self.agents: Dict[str, BaseAgent] = {}
        self.message_queue: List[AgentMessage] = []
        self.workflow_history: List[Dict[str, Any]] = []
        
        # Agent'ları başlat
        self._initialize_agents()
        
        logger.info("Agent Manager başlatıldı")
    
    def _initialize_agents(self):
        """Agent'ları başlat ve bağlantıları kur"""
        try:
            # Product Agent
            product_agent = ProductAgent("product_agent_001")
            self.agents["product_agent_001"] = product_agent
            
            # Customer Agent
            customer_agent = CustomerAgent("customer_agent_001")
            self.agents["customer_agent_001"] = customer_agent
            
            # Context Analysis Agent
            context_agent = ContextAnalysisAgent("context_agent_001")
            self.agents["context_agent_001"] = context_agent
            
            # Mind Map Agent
            mindmap_agent = MindMapAgent("mindmap_agent_001")
            self.agents["mindmap_agent_001"] = mindmap_agent
            
            # Agent'ları birbirine bağla
            product_agent.connect_agent("customer_agent_001", "CustomerAnalyst")
            product_agent.connect_agent("context_agent_001", "ContextAnalyst")
            product_agent.connect_agent("mindmap_agent_001", "MindMapGenerator")
            
            customer_agent.connect_agent("product_agent_001", "ProductAnalyst")
            customer_agent.connect_agent("context_agent_001", "ContextAnalyst")
            customer_agent.connect_agent("mindmap_agent_001", "MindMapGenerator")
            
            context_agent.connect_agent("product_agent_001", "ProductAnalyst")
            context_agent.connect_agent("customer_agent_001", "CustomerAnalyst")
            context_agent.connect_agent("mindmap_agent_001", "MindMapGenerator")
            
            mindmap_agent.connect_agent("product_agent_001", "ProductAnalyst")
            mindmap_agent.connect_agent("customer_agent_001", "CustomerAnalyst")
            mindmap_agent.connect_agent("context_agent_001", "ContextAnalyst")
            
            logger.info(f"{len(self.agents)} agent başlatıldı ve bağlandı")
            
        except Exception as e:
            logger.error(f"Agent başlatma hatası: {str(e)}")
    
    async def execute_workflow(self, workflow_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Agent workflow'unu çalıştır"""
        try:
            workflow_id = f"workflow_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            logger.info(f"Workflow başlatılıyor: {workflow_type} (ID: {workflow_id})")
            
            # Workflow tipine göre agent'ları seç
            if workflow_type == "product_analysis":
                result = await self._product_analysis_workflow(data, workflow_id)
            elif workflow_type == "customer_analysis":
                result = await self._customer_analysis_workflow(data, workflow_id)
            elif workflow_type == "integrated_analysis":
                result = await self._integrated_analysis_workflow(data, workflow_id)
            elif workflow_type == "mind_map_generation":
                result = await self._mind_map_generation_workflow(data, workflow_id)
            else:
                result = await self._general_workflow(data, workflow_id)
            
            # Workflow geçmişine kaydet
            self.workflow_history.append({
                "workflow_id": workflow_id,
                "type": workflow_type,
                "data": data,
                "result": result,
                "timestamp": datetime.now().isoformat()
            })
            
            return {
                "success": True,
                "workflow_id": workflow_id,
                "result": result,
                "agents_used": list(self.agents.keys())
            }
            
        except Exception as e:
            logger.error(f"Workflow çalıştırma hatası: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "workflow_id": workflow_id if 'workflow_id' in locals() else None
            }
    
    async def _product_analysis_workflow(self, data: Dict[str, Any], workflow_id: str) -> Dict[str, Any]:
        """Ürün analizi workflow'u"""
        product_agent = self.agents["product_agent_001"]
        
        # 1. Ürün sınıflandırma
        classification_task = {
            "type": "classify_product",
            "product_data": data.get("product_data", {})
        }
        classification_result = await product_agent.process_task(classification_task)
        
        # 2. Ürün analizi
        analysis_task = {
            "type": "analyze_product",
            "product_data": data.get("product_data", {})
        }
        analysis_result = await product_agent.process_task(analysis_task)
        
        # 3. Özellik çıkarma
        feature_task = {
            "type": "extract_features",
            "product_data": data.get("product_data", {})
        }
        feature_result = await product_agent.process_task(feature_task)
        
        return {
            "workflow_type": "product_analysis",
            "classification": classification_result,
            "analysis": analysis_result,
            "features": feature_result,
            "workflow_id": workflow_id
        }
    
    async def _customer_analysis_workflow(self, data: Dict[str, Any], workflow_id: str) -> Dict[str, Any]:
        """Müşteri analizi workflow'u"""
        customer_agent = self.agents["customer_agent_001"]
        
        # 1. Müşteri segmentasyonu
        segmentation_task = {
            "type": "segment_customer",
            "customer_data": data.get("customer_data", {})
        }
        segmentation_result = await customer_agent.process_task(segmentation_task)
        
        # 2. Davranış analizi
        behavior_task = {
            "type": "analyze_behavior",
            "customer_data": data.get("customer_data", {})
        }
        behavior_result = await customer_agent.process_task(behavior_task)
        
        # 3. Churn tahmini
        churn_task = {
            "type": "predict_churn",
            "customer_data": data.get("customer_data", {})
        }
        churn_result = await customer_agent.process_task(churn_task)
        
        return {
            "workflow_type": "customer_analysis",
            "segmentation": segmentation_result,
            "behavior": behavior_result,
            "churn_prediction": churn_result,
            "workflow_id": workflow_id
        }
    
    async def _integrated_analysis_workflow(self, data: Dict[str, Any], workflow_id: str) -> Dict[str, Any]:
        """Entegre analiz workflow'u - Agent'lar arası işbirliği"""
        product_agent = self.agents["product_agent_001"]
        customer_agent = self.agents["customer_agent_001"]
        
        # 1. Ürün analizi
        product_result = await self._product_analysis_workflow(data, f"{workflow_id}_product")
        
        # 2. Müşteri analizi
        customer_result = await self._customer_analysis_workflow(data, f"{workflow_id}_customer")
        
        # 3. Agent'lar arası işbirliği
        # Product Agent -> Customer Agent: "Bu ürün hangi müşteri segmentine uygun?"
        product_to_customer_msg = await product_agent.send_message(
            "customer_agent_001",
            "request",
            {
                "type": "product_customer_match",
                "product_category": product_result["classification"].get("category"),
                "product_features": product_result["features"].get("extracted_features", [])
            }
        )
        
        # Customer Agent yanıt ver
        customer_response = await customer_agent.receive_message(product_to_customer_msg)
        
        # 4. Entegre öneriler
        integrated_recommendations = await self._generate_integrated_recommendations(
            product_result, customer_result, customer_response
        )
        
        return {
            "workflow_type": "integrated_analysis",
            "product_analysis": product_result,
            "customer_analysis": customer_result,
            "agent_collaboration": {
                "product_to_customer": product_to_customer_msg.dict(),
                "customer_response": customer_response.dict() if customer_response else None
            },
            "integrated_recommendations": integrated_recommendations,
            "workflow_id": workflow_id
        }
    
    async def _general_workflow(self, data: Dict[str, Any], workflow_id: str) -> Dict[str, Any]:
        """Genel workflow"""
        results = {}
        
        # Tüm agent'lara görev gönder
        for agent_id, agent in self.agents.items():
            try:
                result = await agent.process_task(data)
                results[agent_id] = result
            except Exception as e:
                logger.error(f"Agent {agent_id} görev hatası: {str(e)}")
                results[agent_id] = {"success": False, "error": str(e)}
        
        return {
            "workflow_type": "general",
            "agent_results": results,
            "workflow_id": workflow_id
        }
    
    async def _generate_integrated_recommendations(
        self, 
        product_result: Dict[str, Any], 
        customer_result: Dict[str, Any], 
        customer_response: Optional[AgentMessage]
    ) -> Dict[str, Any]:
        """Entegre öneriler oluştur"""
        
        # Ürün ve müşteri verilerini birleştir
        product_category = product_result["classification"].get("category", "unknown")
        customer_segment = customer_result["segmentation"].get("segment", "regular")
        
        # Segment-kategori uyumluluğu
        segment_category_match = {
            "premium": ["electronics", "fashion", "home"],
            "regular": ["electronics", "fashion", "home", "books", "sports"],
            "budget": ["books", "sports", "toys", "beauty"],
            "new": ["books", "toys", "beauty"]  # Yeni müşteriler için güvenli kategoriler
        }
        
        is_match = product_category in segment_category_match.get(customer_segment, [])
        
        # Öneri stratejisi
        if is_match:
            recommendation_strategy = "high_priority"
            confidence = 0.9
        else:
            recommendation_strategy = "low_priority"
            confidence = 0.3
        
        return {
            "product_customer_match": is_match,
            "recommendation_strategy": recommendation_strategy,
            "confidence": confidence,
            "reasoning": f"Ürün kategorisi ({product_category}) müşteri segmenti ({customer_segment}) ile uyumlu: {is_match}",
            "agent_collaboration_insights": customer_response.content if customer_response else None
        }
    
    def get_agent_status(self) -> Dict[str, Any]:
        """Tüm agent'ların durumunu döndür"""
        status = {}
        for agent_id, agent in self.agents.items():
            status[agent_id] = {
                "agent_type": agent.agent_type,
                "capabilities": agent.get_capabilities(),
                "state": agent.get_state().dict(),
                "connected_agents": list(agent.connected_agents.keys())
            }
        return status
    
    def get_workflow_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Workflow geçmişini döndür"""
        return self.workflow_history[-limit:]
    
    async def send_message_to_agent(self, to_agent: str, message: AgentMessage) -> Optional[AgentMessage]:
        """Belirli bir agent'a mesaj gönder"""
        if to_agent in self.agents:
            return await self.agents[to_agent].receive_message(message)
        else:
            logger.error(f"Agent bulunamadı: {to_agent}")
            return None
    
    def add_agent(self, agent: BaseAgent):
        """Yeni agent ekle"""
        self.agents[agent.agent_id] = agent
        logger.info(f"Yeni agent eklendi: {agent.agent_id}")
    
    def remove_agent(self, agent_id: str):
        """Agent kaldır"""
        if agent_id in self.agents:
            del self.agents[agent_id]
            logger.info(f"Agent kaldırıldı: {agent_id}")
        else:
            logger.warning(f"Kaldırılacak agent bulunamadı: {agent_id}")
    
    def get_available_workflows(self) -> List[str]:
        """Kullanılabilir workflow'ları döndür"""
        return [
            "product_analysis",
            "customer_analysis", 
            "integrated_analysis",
            "mind_map_generation",
            "general"
        ]
    
    async def _mind_map_generation_workflow(self, data: Dict[str, Any], workflow_id: str) -> Dict[str, Any]:
        """Zihin haritası oluşturma workflow'u"""
        context_agent = self.agents["context_agent_001"]
        mindmap_agent = self.agents["mindmap_agent_001"]
        product_agent = self.agents["product_agent_001"]
        
        # 1. Kullanıcı durumunu analiz et
        context_task = {
            "type": "analyze_user_context",
            "user_input": data.get("user_input", "")
        }
        context_result = await context_agent.process_task(context_task)
        
        # 2. İhtiyaçları çıkar
        needs_task = {
            "type": "extract_needs",
            "context_analysis": context_result.get("context_analysis", {})
        }
        needs_result = await context_agent.process_task(needs_task)
        
        # 3. Zihin haritası oluştur
        mindmap_task = {
            "type": "generate_mind_map",
            "context_analysis": context_result.get("context_analysis", {}),
            "extracted_needs": needs_result.get("extracted_needs", {})
        }
        mindmap_result = await mindmap_agent.process_task(mindmap_task)
        
        # 4. Her kategori için ürün önerileri oluştur
        product_recommendations = {}
        mind_map = mindmap_result.get("mind_map", {})
        
        for category in mind_map.get("main_categories", []):
            category_name = category["name"]
            items = category["items"]
            
            # Her ürün için öneri oluştur
            category_products = []
            for item in items[:3]:  # İlk 3 ürün için öneri
                product_task = {
                    "type": "analyze_product",
                    "product_data": {
                        "title": item,
                        "description": f"{category_name} kategorisinde {item}",
                        "category": category_name
                    }
                }
                product_result = await product_agent.process_task(product_task)
                category_products.append({
                    "product_name": item,
                    "analysis": product_result
                })
            
            product_recommendations[category_name] = category_products
        
        return {
            "workflow_type": "mind_map_generation",
            "context_analysis": context_result,
            "needs_analysis": needs_result,
            "mind_map": mindmap_result,
            "product_recommendations": product_recommendations,
            "workflow_id": workflow_id
        } 