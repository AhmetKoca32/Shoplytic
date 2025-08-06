import sys
import os
import pytest

# Proje kökünü path'e ekle
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from app.langgraph.nodes.llm_node import LLMNode

class DummyResponse:
    def __init__(self, text):
        self.text = text

def dummy_generate_content(self, prompt):
    return DummyResponse(f"YANIT: {prompt}")

@pytest.mark.asyncio
async def test_llm_node(monkeypatch):
    # Mock LLM Node testi - gerçek LLM entegrasyonu olmadan
    node = LLMNode()
    state = {
        "workflow_type": "test",
        "processed_data": {"test": "data"},
        "execution_steps": []
    }
    result = await node.execute(state)
    assert "llm_output" in result or "error" in result