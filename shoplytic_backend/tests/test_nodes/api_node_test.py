import sys
import os
import pytest
from unittest.mock import Mock, patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from app.langgraph.nodes.api_node import APINode

@pytest.mark.asyncio
async def test_api_node_success_shopify():
    node = APINode()
    state = {
        "workflow_type": "mind_map_generation",
        "execution_steps": []
    }
    result = await node.execute(state)
    assert "api_results" in result
    assert result["error"] is None

@pytest.mark.asyncio
async def test_api_node_missing_type():
    node = APINode()
    state = {"execution_steps": []}
    result = await node.execute(state)
    assert "api_results" in result
    assert result["error"] is None

@pytest.mark.asyncio
async def test_api_node_unsupported_type():
    node = APINode()
    state = {"workflow_type": "unsupported_type", "execution_steps": []}
    result = await node.execute(state)
    assert "api_results" in result
    assert result["error"] is None
