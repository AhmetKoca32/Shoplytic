"""
AgentNode: AI Agent'ları çalıştıran LangGraph Node'u
"""
import logging
from typing import Dict, Any
from datetime import datetime
import sys
import os

# Agent modüllerini import et
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from app.agents.agent_manager import AgentManager

logger = logging.getLogger(__name__)

class AgentNode:
    """AI Agent'ları çalıştıran node"""
    
    def __init__(self):
        self.name = "agent_node"
        self.agent_manager = AgentManager()
        logger.info("Agent Node başlatıldı")
    
    async def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        return await self.run(state)
    
    async def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Agent'ları çalıştır"""
        
        workflow_type = state.get("workflow_type", "")
        processed_data = state.get("processed_data", {})
        llm_output = state.get("llm_output", {})
        
        try:
            # Workflow tipine göre agent seçimi
            if workflow_type == "product_classification":
                result = await self._run_product_agent(processed_data, llm_output)
            elif workflow_type == "customer_segmentation":
                result = await self._run_customer_agent(processed_data, llm_output)
            elif workflow_type == "integrated_analysis":
                result = await self._run_integrated_agents(processed_data, llm_output)
            else:
                result = await self._run_general_agents(processed_data, llm_output)
            
            # Agent sonuçlarını state'e ekle
            state["agent_results"] = result
            state["agent_error"] = None
            
            logger.info(f"AgentNode: {workflow_type} işlemi başarıyla tamamlandı.")
            
        except Exception as e:
            logger.exception(f"AgentNode: {workflow_type} işlemi başarısız.")
            state["agent_results"] = {}
            state["agent_error"] = str(e)
        
        return state
    
    async def _run_product_agent(self, data: Dict[str, Any], llm_output: Dict[str, Any]) -> Dict[str, Any]:
        """Product Agent'ı çalıştır"""
        
        # Ürün verilerini hazırla
        product_data = {
            "product_data": {
                "title": data.get("product_title", ""),
                "description": data.get("product_description", ""),
                "price": data.get("price", 0),
                "id": data.get("product_id", "unknown")
            }
        }
        
        # Product analysis workflow'unu çalıştır
        result = await self.agent_manager.execute_workflow("product_analysis", product_data)
        
        return {
            "agent_type": "product_analysis",
            "result": result,
            "agents_used": ["product_agent_001"],
            "timestamp": datetime.now().isoformat()
        }
    
    async def _run_customer_agent(self, data: Dict[str, Any], llm_output: Dict[str, Any]) -> Dict[str, Any]:
        """Customer Agent'ı çalıştır"""
        
        # Müşteri verilerini hazırla
        customer_data = {
            "customer_data": {
                "id": data.get("customer_id", "unknown"),
                "total_spend": data.get("total_spend", 0),
                "visit_count": data.get("visit_count", 0),
                "loyalty_score": data.get("loyalty_score", 0.0),
                "avg_order_value": data.get("avg_order_value", 0),
                "purchase_history": data.get("purchase_history", []),
                "days_since_last_purchase": data.get("days_since_last_purchase", 0),
                "complaint_count": data.get("complaint_count", 0)
            }
        }
        
        # Customer analysis workflow'unu çalıştır
        result = await self.agent_manager.execute_workflow("customer_analysis", customer_data)
        
        return {
            "agent_type": "customer_analysis",
            "result": result,
            "agents_used": ["customer_agent_001"],
            "timestamp": datetime.now().isoformat()
        }
    
    async def _run_integrated_agents(self, data: Dict[str, Any], llm_output: Dict[str, Any]) -> Dict[str, Any]:
        """Entegre agent analizi çalıştır"""
        
        # Hem ürün hem müşteri verilerini hazırla
        integrated_data = {
            "product_data": {
                "title": data.get("product_title", ""),
                "description": data.get("product_description", ""),
                "price": data.get("price", 0),
                "id": data.get("product_id", "unknown")
            },
            "customer_data": {
                "id": data.get("customer_id", "unknown"),
                "total_spend": data.get("total_spend", 0),
                "visit_count": data.get("visit_count", 0),
                "loyalty_score": data.get("loyalty_score", 0.0),
                "avg_order_value": data.get("avg_order_value", 0),
                "purchase_history": data.get("purchase_history", []),
                "days_since_last_purchase": data.get("days_since_last_purchase", 0),
                "complaint_count": data.get("complaint_count", 0)
            }
        }
        
        # Integrated analysis workflow'unu çalıştır
        result = await self.agent_manager.execute_workflow("integrated_analysis", integrated_data)
        
        return {
            "agent_type": "integrated_analysis",
            "result": result,
            "agents_used": ["product_agent_001", "customer_agent_001"],
            "timestamp": datetime.now().isoformat()
        }
    
    async def _run_general_agents(self, data: Dict[str, Any], llm_output: Dict[str, Any]) -> Dict[str, Any]:
        """Genel agent analizi çalıştır"""
        
        # General workflow'unu çalıştır
        result = await self.agent_manager.execute_workflow("general", data)
        
        return {
            "agent_type": "general",
            "result": result,
            "agents_used": list(self.agent_manager.agents.keys()),
            "timestamp": datetime.now().isoformat()
        }
    
    def get_agent_status(self) -> Dict[str, Any]:
        """Agent durumlarını döndür"""
        return self.agent_manager.get_agent_status()
    
    def get_available_workflows(self) -> list:
        """Kullanılabilir workflow'ları döndür"""
        return self.agent_manager.get_available_workflows()
    
    def get_workflow_history(self, limit: int = 5) -> list:
        """Workflow geçmişini döndür"""
        return self.agent_manager.get_workflow_history(limit) 