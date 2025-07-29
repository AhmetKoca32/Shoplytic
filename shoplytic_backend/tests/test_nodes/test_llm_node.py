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
    from app.langgraph.nodes import llm_node
    monkeypatch.setattr(llm_node.genai.GenerativeModel, "generate_content", dummy_generate_content)
    node = LLMNode()
    state = {
        "prompt": "Test prompt",
    }
    result = await node.execute(state)
    assert result["llm_output"].startswith("YANIT: ")
    assert result["llm_error"] is None