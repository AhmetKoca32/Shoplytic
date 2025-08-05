from langgraph.graph import StateGraph, END
from typing import Dict, Any, TypedDict, Optional
import uuid
import time
from datetime import datetime

# Node'ları import et
from .nodes.entry_node import EntryNode
from .nodes.prompt_node import PromptNode
from .nodes.llm_node import LLMNode

from .nodes.process_node import ProcessNode
from .nodes.memory_node import MemoryNode
from .nodes.output_node import OutputNode
from .nodes.tool_node import ToolNode
from .nodes.agent_node import AgentNode

class WorkflowState(TypedDict):
    """Workflow state modeli"""
    workflow_id: str
    workflow_type: str
    user_id: Optional[str]
    input_data: Dict[str, Any]
    processed_data: Dict[str, Any]
    prompt: str
    llm_response: str
    llm_output: Dict[str, Any]  # LangChain çıktısı için
    tool_results: Dict[str, Any]  # Tool sonuçları için
    agent_results: Dict[str, Any]  # Agent sonuçları için
    memory_context: Dict[str, Any]
    final_output: Dict[str, Any]
    execution_steps: list
    error: Optional[str]
    timestamp: str

class WorkflowGraph:
    """Ana LangGraph workflow builder sınıfı"""
    
    def __init__(self):
        self.graph = None
        self.nodes = {
            'entry': EntryNode(),
            'prompt': PromptNode(),
            'llm': LLMNode(),

            'process': ProcessNode(),
            'memory': MemoryNode(),
            'tool': ToolNode(),  # LangChain tool'ları için
            'agent': AgentNode(),  # AI Agent'ları için
            'output': OutputNode()
        }
        self._build_graph()
    
    def _build_graph(self):
        """LangGraph workflow'unu oluştur"""
        # StateGraph oluştur
        workflow = StateGraph(WorkflowState)
        
        # Node'ları ekle
        workflow.add_node("entry", self.nodes['entry'].execute)
        workflow.add_node("prompt", self.nodes['prompt'].execute)
        workflow.add_node("llm", self.nodes['llm'].execute)

        workflow.add_node("process", self.nodes['process'].execute)
        workflow.add_node("memory", self.nodes['memory'].execute)
        workflow.add_node("tool", self.nodes['tool'].execute)  # Tool node'u ekle
        workflow.add_node("agent", self.nodes['agent'].execute)  # Agent node'u ekle
        workflow.add_node("output", self.nodes['output'].execute)
        
        # Başlangıç noktasını belirle
        workflow.set_entry_point("entry")
        
        # Edge'leri (bağlantıları) tanımla
        workflow.add_edge("entry", "memory")  # Önce hafızayı kontrol et
        workflow.add_edge("memory", "prompt")  # Sonra prompt oluştur
        workflow.add_edge("prompt", "llm")     # LLM'e gönder
        workflow.add_edge("llm", "tool")       # Tool'ları çalıştır
        workflow.add_edge("tool", "agent")     # Agent'ları çalıştır
        workflow.add_edge("agent", "process")  # Yanıtı işle
        
        # Koşullu edge'ler
        workflow.add_conditional_edges(
            "process",
            self._should_call_api,
            {
                "output": "output"
            }
        )
        workflow.add_edge("output", END)       # Son
        
        # Graph'ı compile et
        self.graph = workflow.compile()
    
    def _should_call_api(self, state: WorkflowState) -> str:
        """API çağrısı gerekip gerekmediğini belirle"""
        # Artık sadece output'a yönlendir
        return "output"
    
    async def execute(
        self, 
        input_data: Dict[str, Any], 
        workflow_type: str = "product_classification",
        user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Workflow'u çalıştır"""
        start_time = time.time()
        workflow_id = str(uuid.uuid4())
        
        # Başlangıç state'ini oluştur
        initial_state = WorkflowState(
            workflow_id=workflow_id,
            workflow_type=workflow_type,
            user_id=user_id,
            input_data=input_data,
            processed_data={},
            prompt="",
            llm_response="",
            llm_output={},
            tool_results={},
            agent_results={},
            memory_context={},
            final_output={},
            execution_steps=[],
            error=None,
            timestamp=datetime.now().isoformat()
        )
        
        try:
            # Workflow'u çalıştır
            result = await self.graph.ainvoke(initial_state)
            
            execution_time = time.time() - start_time
            
            return {
                "workflow_id": workflow_id,
                "output": result.get("final_output", {}),
                "execution_time": execution_time,
                "steps": result.get("execution_steps", []),
                "success": result.get("error") is None
            }
            
        except Exception as e:
            execution_time = time.time() - start_time
            return {
                "workflow_id": workflow_id,
                "output": {},
                "execution_time": execution_time,
                "steps": [],
                "success": False,
                "error": str(e)
            }
    
    def get_workflow_types(self) -> list:
        """Desteklenen workflow tiplerini döndür"""
        return [
            "product_classification",
            "product_recommendation",
            "customer_segmentation",
            "mind_map_generation"
        ]