import asyncio
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../app/langgraph/nodes'))
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from app.langgraph.nodes.prompt_node import PromptNode

def test_prompt_node():
    node = PromptNode()
    state = {
        "workflow_id": "test-002",
        "workflow_type": "product_recommendation",
        "processed_data": {
            "user_id": "123",
            "cart_items": [
                {"name": "Ayakkabı", "category": "Giyim", "price": 500, "quantity": 1}
            ]
        },
        "memory_context": {},
        "execution_steps": []
    }
    result = asyncio.run(node.execute(state))
    assert "prompt" in result
    assert result["prompt"] != ""
    assert result["error"] is None
