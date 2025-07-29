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
        "api_type": "shopify",
        "api_payload": {"url": "http://fake-shopify", "headers": {}, "data": {"foo": "bar"}}
    }
    mock_response = Mock()
    mock_response.json.return_value = {"success": True}
    with patch("requests.post", return_value=mock_response):
        result = await node.execute(state)
    assert result["api_response"] == {"success": True}
    assert result["api_error"] is None

@pytest.mark.asyncio
async def test_api_node_missing_type():
    node = APINode()
    state = {"api_payload": {"url": "http://fake-shopify"}}
    result = await node.execute(state)
    assert result.get("api_response") is None
    assert "API tipi veya payload eksik" in result["api_error"]

@pytest.mark.asyncio
async def test_api_node_unsupported_type():
    node = APINode()
    state = {"api_type": "unsupported", "api_payload": {"url": "http://fake-api"}}
    result = await node.execute(state)
    assert result["api_response"] is None
    assert "Desteklenmeyen API tipi" in result["api_error"]
