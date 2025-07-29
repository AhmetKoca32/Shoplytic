import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from app.langgraph.nodes.memory_node import MemoryNode

@pytest.mark.asyncio
async def test_memory_node_basic():
    node = MemoryNode()
    state = {
        "user_id": "test_user",
        "workflow_type": "test_workflow",
        "processed_data": {"foo": "bar"},
        "memory_context": {},
        "execution_steps": []
    }
    result = await node.execute(state)
    # Hafıza bağlamı oluşturulmuş olmalı
    assert "memory_context" in result
    assert isinstance(result["memory_context"], dict)
    assert result.get("error") is None

@pytest.mark.asyncio
async def test_memory_node_no_user():
    node = MemoryNode()
    state = {"workflow_type": "test_workflow"}
    result = await node.execute(state)
    # user_id yoksa context boş dönmeli
    assert isinstance(result["memory_context"], dict)
    assert result.get("error") is None
