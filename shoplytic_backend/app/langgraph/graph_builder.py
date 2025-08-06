# LangGraph mock - gerçek langgraph yüklenene kadar
class StateGraph:
    def __init__(self, state_type):
        self.state_type = state_type
        self.nodes = {}
        self.edges = {}
        self.entry_point = None
        self.conditional_edges = {}
    
    def add_node(self, name, func):
        self.nodes[name] = func
    
    def add_edge(self, from_node, to_node):
        self.edges[from_node] = to_node
    
    def set_entry_point(self, node):
        self.entry_point = node
    
    def add_conditional_edges(self, node, condition_func, edges):
        self.conditional_edges[node] = (condition_func, edges)
    
    def compile(self):
        return self

END = "END"

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
        """Workflow'u çalıştır (Mock versiyon)"""
        start_time = time.time()
        workflow_id = str(uuid.uuid4())
        
        try:
            # Mock workflow execution
            if workflow_type == "mind_map_generation":
                # Zihin haritası oluştur
                categories = [
                    {
                        "name": "Ev Eşyaları",
                        "priority": 1,
                        "products": ["Yatak", "Çalışma Masası", "Mutfak Gereçleri"]
                    },
                    {
                        "name": "Teknoloji", 
                        "priority": 2,
                        "products": ["Laptop", "Tablet", "Kulaklık"]
                    },
                    {
                        "name": "Kıyafet",
                        "priority": 3, 
                        "products": ["Günlük Kıyafetler", "Spor Kıyafetleri"]
                    }
                ]
                
                final_output = {
                    "mind_map": {
                        "categories": categories,
                        "user_input": input_data.get("user_input", ""),
                        "generated_at": datetime.now().isoformat()
                    }
                }
            else:
                final_output = {
                    "message": f"Workflow {workflow_type} completed",
                    "input": input_data
                }
            
            execution_time = time.time() - start_time
            
            return {
                "workflow_id": workflow_id,
                "output": final_output,
                "execution_time": execution_time,
                "steps": ["entry", "memory", "prompt", "llm", "tool", "agent", "process", "output"],
                "success": True
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