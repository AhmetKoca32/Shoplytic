import asyncio
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../app/langgraph/nodes'))
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from app.langgraph.nodes.entry_node import EntryNode

def test_entry_node():
    node = EntryNode()
    state = {
        "workflow_id": "test-001",
        "execution_steps": []
    }
    result = asyncio.run(node.execute(state))
    assert result["execution_steps"][-1]["step"] == "entry"
    assert result["error"] is None
