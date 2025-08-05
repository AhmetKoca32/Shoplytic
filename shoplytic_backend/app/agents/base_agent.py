"""
Base Agent Class - Tüm AI Agent'lar için temel sınıf
"""
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from datetime import datetime
from langchain.schema import BaseMessage, HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

class AgentState(BaseModel):
    """Agent durumu"""
    agent_id: str
    agent_type: str
    current_task: str
    memory: Dict[str, Any] = Field(default_factory=dict)
    conversation_history: List[Dict[str, Any]] = Field(default_factory=list)
    last_updated: datetime = Field(default_factory=datetime.now)

class AgentMessage(BaseModel):
    """Agent'lar arası mesaj"""
    from_agent: str
    to_agent: str
    message_type: str  # "request", "response", "notification"
    content: Dict[str, Any]
    timestamp: datetime = Field(default_factory=datetime.now)
    priority: int = 1  # 1-5, 5 en yüksek

class BaseAgent(ABC):
    """Tüm AI Agent'lar için temel sınıf"""
    
    def __init__(self, agent_id: str, agent_type: str, llm_model: str = "gemini-pro"):
        self.agent_id = agent_id
        self.agent_type = agent_type
        self.state = AgentState(
            agent_id=agent_id,
            agent_type=agent_type,
            current_task="idle"
        )
        
        # LLM modeli
        self.llm = ChatGoogleGenerativeAI(
            model=llm_model,
            temperature=0.7,
            max_output_tokens=2048
        )
        
        # Agent hafızası
        self.memory = {}
        self.conversation_history = []
        
        # Diğer agent'larla iletişim
        self.connected_agents = {}
        
        logger.info(f"Agent {agent_id} ({agent_type}) başlatıldı")
    
    @abstractmethod
    async def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Ana görev işleme metodu - her agent implement eder"""
        pass
    
    @abstractmethod
    def get_capabilities(self) -> List[str]:
        """Agent'ın yeteneklerini döndür"""
        pass
    
    async def receive_message(self, message: AgentMessage) -> Optional[AgentMessage]:
        """Diğer agent'lardan mesaj al"""
        try:
            logger.info(f"Agent {self.agent_id} mesaj aldı: {message.from_agent} -> {message.content}")
            
            # Mesajı hafızaya kaydet
            self.conversation_history.append({
                "from": message.from_agent,
                "type": message.message_type,
                "content": message.content,
                "timestamp": message.timestamp.isoformat()
            })
            
            # Mesaj tipine göre işle
            if message.message_type == "request":
                return await self._handle_request(message)
            elif message.message_type == "response":
                return await self._handle_response(message)
            elif message.message_type == "notification":
                return await self._handle_notification(message)
            
        except Exception as e:
            logger.error(f"Agent {self.agent_id} mesaj işleme hatası: {str(e)}")
            return None
    
    async def send_message(self, to_agent: str, message_type: str, content: Dict[str, Any], priority: int = 1) -> AgentMessage:
        """Diğer agent'a mesaj gönder"""
        message = AgentMessage(
            from_agent=self.agent_id,
            to_agent=to_agent,
            message_type=message_type,
            content=content,
            priority=priority
        )
        
        logger.info(f"Agent {self.agent_id} mesaj gönderdi: {to_agent} -> {message_type}")
        return message
    
    async def _handle_request(self, message: AgentMessage) -> Optional[AgentMessage]:
        """İstek mesajlarını işle"""
        try:
            # İsteği işle
            result = await self.process_task(message.content)
            
            # Yanıt gönder
            return AgentMessage(
                from_agent=self.agent_id,
                to_agent=message.from_agent,
                message_type="response",
                content=result,
                priority=message.priority
            )
        except Exception as e:
            logger.error(f"Agent {self.agent_id} istek işleme hatası: {str(e)}")
            return None
    
    async def _handle_response(self, message: AgentMessage) -> None:
        """Yanıt mesajlarını işle"""
        # Yanıtı hafızaya kaydet
        self.memory[f"response_from_{message.from_agent}"] = {
            "content": message.content,
            "timestamp": message.timestamp.isoformat()
        }
    
    async def _handle_notification(self, message: AgentMessage) -> None:
        """Bildirim mesajlarını işle"""
        # Bildirimi hafızaya kaydet
        self.memory[f"notification_from_{message.from_agent}"] = {
            "content": message.content,
            "timestamp": message.timestamp.isoformat()
        }
    
    def connect_agent(self, agent_id: str, agent_type: str):
        """Başka bir agent'a bağlan"""
        self.connected_agents[agent_id] = {
            "type": agent_type,
            "connected_at": datetime.now().isoformat()
        }
        logger.info(f"Agent {self.agent_id} -> {agent_id} bağlantısı kuruldu")
    
    def get_state(self) -> AgentState:
        """Agent durumunu döndür"""
        self.state.memory = self.memory
        self.state.conversation_history = self.conversation_history
        self.state.last_updated = datetime.now()
        return self.state
    
    def update_memory(self, key: str, value: Any):
        """Hafızayı güncelle"""
        self.memory[key] = {
            "value": value,
            "timestamp": datetime.now().isoformat()
        }
    
    def get_memory(self, key: str) -> Optional[Any]:
        """Hafızadan veri al"""
        if key in self.memory:
            return self.memory[key]["value"]
        return None
    
    async def think(self, prompt: str) -> str:
        """Agent düşünme süreci"""
        try:
            messages = [
                SystemMessage(content=f"Sen {self.agent_type} uzmanısın. Görevin: {prompt}"),
                HumanMessage(content=f"Lütfen bu konuda düşün ve yanıt ver: {prompt}")
            ]
            
            response = await self.llm.ainvoke(messages)
            return response.content
            
        except Exception as e:
            logger.error(f"Agent {self.agent_id} düşünme hatası: {str(e)}")
            return f"Düşünme hatası: {str(e)}"
    
    def __str__(self):
        return f"Agent({self.agent_id}, {self.agent_type})"
    
    def __repr__(self):
        return self.__str__() 