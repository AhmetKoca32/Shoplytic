"""
ToolNode: LangChain tool'larını kullanan LangGraph Node'u
"""
import logging
from typing import Dict, Any, List
from langchain_core.tools import Tool
# Agent import'larını geçici olarak devre dışı bırak
# from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_core.messages import BaseMessage
from langchain_community.tools import DuckDuckGoSearchRun, WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
import json
import requests

logger = logging.getLogger(__name__)

class EcommerceTools:
    """E-ticaret özel tool'ları"""
    
    @staticmethod
    def get_product_price_tool() -> Tool:
        """Ürün fiyat karşılaştırma tool'u"""
        def get_product_price(product_name: str) -> str:
            """Ürün fiyatını farklı platformlardan karşılaştır"""
            try:
                # Mock fiyat verisi (gerçek uygulamada API çağrıları yapılır)
                prices = {
                    "iphone": {"amazon": 999, "trendyol": 1050, "hepsiburada": 980},
                    "samsung": {"amazon": 899, "trendyol": 920, "hepsiburada": 890},
                    "laptop": {"amazon": 1500, "trendyol": 1550, "hepsiburada": 1480}
                }
                
                product_lower = product_name.lower()
                for key in prices:
                    if key in product_lower:
                        return json.dumps(prices[key], ensure_ascii=False)
                
                return f"'{product_name}' için fiyat bilgisi bulunamadı."
            except Exception as e:
                return f"Fiyat karşılaştırma hatası: {str(e)}"
        
        return Tool(
            name="get_product_price",
            description="Ürün fiyatını farklı e-ticaret platformlarından karşılaştırır",
            func=get_product_price
        )
    
    @staticmethod
    def get_stock_check_tool() -> Tool:
        """Stok kontrol tool'u"""
        def check_stock(product_id: str) -> str:
            """Ürün stok durumunu kontrol et"""
            try:
                # Mock stok verisi
                stock_data = {
                    "123": {"available": True, "quantity": 15, "location": "İstanbul"},
                    "456": {"available": False, "quantity": 0, "location": "Ankara"},
                    "789": {"available": True, "quantity": 8, "location": "İzmir"}
                }
                
                if product_id in stock_data:
                    return json.dumps(stock_data[product_id], ensure_ascii=False)
                else:
                    return f"'{product_id}' ürün ID'si bulunamadı."
            except Exception as e:
                return f"Stok kontrol hatası: {str(e)}"
        
        return Tool(
            name="check_stock",
            description="Ürün stok durumunu kontrol eder",
            func=check_stock
        )
    
    @staticmethod
    def get_customer_reviews_tool() -> Tool:
        """Müşteri yorumları tool'u"""
        def get_customer_reviews(product_name: str) -> str:
            """Ürün müşteri yorumlarını getir"""
            try:
                # Mock yorum verisi
                reviews = {
                    "iphone": [
                        {"rating": 5, "comment": "Harika ürün, çok memnunum"},
                        {"rating": 4, "comment": "İyi ama biraz pahalı"},
                        {"rating": 5, "comment": "Kesinlikle tavsiye ederim"}
                    ],
                    "samsung": [
                        {"rating": 4, "comment": "Kaliteli telefon"},
                        {"rating": 3, "comment": "Orta seviye performans"},
                        {"rating": 5, "comment": "Çok beğendim"}
                    ]
                }
                
                product_lower = product_name.lower()
                for key in reviews:
                    if key in product_lower:
                        return json.dumps(reviews[key], ensure_ascii=False)
                
                return f"'{product_name}' için yorum bulunamadı."
            except Exception as e:
                return f"Yorum getirme hatası: {str(e)}"
        
        return Tool(
            name="get_customer_reviews",
            description="Ürün müşteri yorumlarını getirir",
            func=get_customer_reviews
        )

class ToolNode:
    """LangChain tool'larını kullanan node"""
    
    def __init__(self):
        self.name = "tool_node"
        self.tools = []
        self.agent_executor = None
        self._setup_tools()
    
    def _setup_tools(self):
        """Tool'ları hazırla"""
        
        # E-ticaret özel tool'ları
        ecommerce_tools = EcommerceTools()
        self.tools.extend([
            ecommerce_tools.get_product_price_tool(),
            ecommerce_tools.get_stock_check_tool(),
            ecommerce_tools.get_customer_reviews_tool()
        ])
        
        # Genel tool'lar
        try:
            # Web arama tool'u
            search_tool = DuckDuckGoSearchRun()
            self.tools.append(Tool(
                name="web_search",
                description="Web'de arama yapar",
                func=search_tool.run
            ))
            
            # Wikipedia tool'u
            wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
            self.tools.append(Tool(
                name="wikipedia_search",
                description="Wikipedia'da arama yapar",
                func=wikipedia.run
            ))
            
        except Exception as e:
            logger.warning(f"Bazı tool'lar yüklenemedi: {str(e)}")
    
    async def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        return await self.run(state)
    
    async def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Tool'ları çalıştır"""
        
        workflow_type = state.get("workflow_type", "")
        llm_output = state.get("llm_output", {})
        processed_data = state.get("processed_data", {})
        
        try:
            # Workflow tipine göre tool seçimi
            if workflow_type == "product_analysis":
                result = await self._run_product_analysis_tools(processed_data, llm_output)
            elif workflow_type == "market_research":
                result = await self._run_market_research_tools(processed_data)
            elif workflow_type == "price_comparison":
                result = await self._run_price_comparison_tools(processed_data)
            else:
                result = await self._run_general_tools(processed_data)
            
            # Tool sonuçlarını state'e ekle
            state["tool_results"] = result
            state["tool_error"] = None
            
            logger.info(f"ToolNode: {workflow_type} işlemi başarıyla tamamlandı.")
            
        except Exception as e:
            logger.exception(f"ToolNode: {workflow_type} işlemi başarısız.")
            state["tool_results"] = {}
            state["tool_error"] = str(e)
        
        return state
    
    async def _run_product_analysis_tools(self, data: Dict[str, Any], llm_output: Dict[str, Any]) -> Dict[str, Any]:
        """Ürün analizi tool'larını çalıştır"""
        
        results = {}
        product_name = data.get("product_name", "")
        
        if product_name:
            # Fiyat karşılaştırma
            price_tool = next((tool for tool in self.tools if tool.name == "get_product_price"), None)
            if price_tool:
                results["price_comparison"] = price_tool.func(product_name)
            
            # Müşteri yorumları
            review_tool = next((tool for tool in self.tools if tool.name == "get_customer_reviews"), None)
            if review_tool:
                results["customer_reviews"] = review_tool.func(product_name)
            
            # Web arama
            search_tool = next((tool for tool in self.tools if tool.name == "web_search"), None)
            if search_tool:
                results["web_search"] = search_tool.func(f"{product_name} özellikleri fiyat")
        
        return results
    
    async def _run_market_research_tools(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Pazar araştırması tool'larını çalıştır"""
        
        results = {}
        search_term = data.get("search_term", "")
        
        if search_term:
            # Web arama
            search_tool = next((tool for tool in self.tools if tool.name == "web_search"), None)
            if search_tool:
                results["market_info"] = search_tool.func(f"{search_term} pazar analizi")
            
            # Wikipedia arama
            wiki_tool = next((tool for tool in self.tools if tool.name == "wikipedia_search"), None)
            if wiki_tool:
                results["wiki_info"] = wiki_tool.func(search_term)
        
        return results
    
    async def _run_price_comparison_tools(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Fiyat karşılaştırma tool'larını çalıştır"""
        
        results = {}
        products = data.get("products", [])
        
        for product in products:
            product_name = product.get("name", "")
            if product_name:
                price_tool = next((tool for tool in self.tools if tool.name == "get_product_price"), None)
                if price_tool:
                    results[product_name] = price_tool.func(product_name)
        
        return results
    
    async def _run_general_tools(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Genel tool'ları çalıştır"""
        
        results = {}
        task = data.get("task", "")
        
        if task:
            # Web arama
            search_tool = next((tool for tool in self.tools if tool.name == "web_search"), None)
            if search_tool:
                results["search_result"] = search_tool.func(task)
        
        return results
    
    def get_available_tools(self) -> List[str]:
        """Kullanılabilir tool'ların listesini döndür"""
        return [tool.name for tool in self.tools]
    
    def add_custom_tool(self, tool: Tool):
        """Özel tool ekle"""
        self.tools.append(tool)
        logger.info(f"Yeni tool eklendi: {tool.name}") 