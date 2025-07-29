from typing import Dict, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class PromptNode:
    """Dinamik AI prompt oluşturma node'u"""

    def __init__(self):
        self.name = "prompt_node"

    async def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        return await self.run(state)

    async def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        logger.info(f"Prompt node başlatıldı - Workflow ID: {state.get('workflow_id')}")
        try:
            execution_steps = state.get("execution_steps", [])
            execution_steps.append({
                "node": "prompt",
                "timestamp": datetime.now().isoformat(),
                "status": "started"
            })
            workflow_type = state.get("workflow_type", "")
            processed_data = state.get("processed_data", {})
            memory_context = state.get("memory_context", {})

            # Basit prompt üretimi (örnek)
            prompt = f"Workflow: {workflow_type}\nData: {processed_data}\nMemory: {memory_context}"

            execution_steps.append({
                "node": "prompt",
                "timestamp": datetime.now().isoformat(),
                "status": "completed"
            })
            logger.info(f"Prompt node tamamlandı - Type: {workflow_type}")
            state["prompt"] = prompt
            state["execution_steps"] = execution_steps
            state["error"] = None
        except Exception as e:
            logger.exception("Prompt node: hata oluştu.")
            state["prompt"] = ""
            state["error"] = str(e)
        return state
