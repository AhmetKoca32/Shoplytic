"""
LLMNode: LangChain ile entegre çalışan LangGraph LLM Node'u
"""
import logging
from typing import Dict, Any, Optional
from app.config.settings import Settings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage, SystemMessage
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from langchain.schema.output_parser import StrOutputParser
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
        self.api_key = settings.GEMINI_API_KEY
        if not self.api_key:
            logger.error("Gemini API anahtarı bulunamadı. Lütfen .env dosyasına GEMINI_API_KEY ekleyin.")
        
        # LangChain Gemini modeli
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-pro",
            google_api_key=self.api_key,
            temperature=0.7,
            max_output_tokens=2048
        )
        
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

    async def get_model_info(self) -> Dict[str, Any]:
        """Model bilgilerini döndür"""
        return {
            "model_name": "gemini-pro",
            "provider": "google",
            "max_tokens": 2048,
            "temperature": 0.7,
            "supports_streaming": True,
            "supports_tools": True
        }
