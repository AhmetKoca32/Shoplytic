from typing import Dict, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class EntryNode:
    """Workflow'un giriş noktası - veri doğrulama ve hazırlama"""

    def __init__(self):
        self.name = "entry_node"

    async def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        return await self.run(state)

    async def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Entry node'unu çalıştır"""
        logger.info(f"Entry node başlatıldı - Workflow ID: {state.get('workflow_id')}")
        try:
            execution_steps = state.get("execution_steps", [])
            execution_steps.append({
                "step": "entry",
                "timestamp": datetime.now().isoformat(),
                "info": "Entry node çalıştı."
            })
            state["execution_steps"] = execution_steps
            state["error"] = None
        except Exception as e:
            logger.exception("Entry node: hata oluştu.")
            state["error"] = str(e)
        return state
