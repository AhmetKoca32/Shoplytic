import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from app.langgraph.nodes.output_node import OutputNode

@pytest.mark.asyncio
async def test_output_node_with_api_response():
    node = OutputNode()
    state = {"api_response": {"result": 42}, "processed_output": "should not be used", "llm_output": "should not be used"}
    result = await node.execute(state)
    assert result["final_output"] == {"result": 42}
    assert result["output_error"] is None

@pytest.mark.asyncio
async def test_output_node_with_processed_output():
    node = OutputNode()
    state = {"processed_output": "işlenmiş çıktı", "llm_output": "should not be used"}
    result = await node.execute(state)
    assert result["final_output"] == "işlenmiş çıktı"
    assert result["output_error"] is None

@pytest.mark.asyncio
async def test_output_node_with_llm_output():
    node = OutputNode()
    state = {"llm_output": "llm yanıtı"}
    result = await node.execute(state)
    assert result["final_output"] == "llm yanıtı"
    assert result["output_error"] is None
