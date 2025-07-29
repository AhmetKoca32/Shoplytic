import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from app.langgraph.nodes.process_node import ProcessNode

@pytest.mark.asyncio
async def test_process_node_json():
    node = ProcessNode()
    state = {"llm_output": '{"foo": "bar"}'}
    result = await node.execute(state)
    assert result["processed_output"] == {"foo": "bar"}
    assert result["process_error"] is None

@pytest.mark.asyncio
async def test_process_node_plain_text():
    node = ProcessNode()
    state = {"llm_output": "sadece metin"}
    result = await node.execute(state)
    assert result["processed_output"] == "sadece metin"
    assert result["process_error"] is None
