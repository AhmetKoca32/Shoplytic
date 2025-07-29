"""
APINode: E-ticaret API'lerine çağrı yapan LangGraph node'u
"""
import logging
from typing import Dict, Any
import requests

logger = logging.getLogger(__name__)

class APINode:
    async def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        return await self.run(state)

    async def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        api_type = state.get("api_type")  # Örn: 'shopify', 'woocommerce'
        api_payload = state.get("api_payload")
        if not api_type or not api_payload:
            state["api_error"] = "APINode: API tipi veya payload eksik."
            return state
        try:
            import requests
            if api_type == "shopify":
                url = api_payload.get("url")
                headers = api_payload.get("headers", {})
                data = api_payload.get("data", {})
                resp = requests.post(url, headers=headers, json=data)
                state["api_response"] = resp.json()
            elif api_type == "woocommerce":
                url = api_payload.get("url")
                headers = api_payload.get("headers", {})
                data = api_payload.get("data", {})
                resp = requests.post(url, headers=headers, json=data)
                state["api_response"] = resp.json()
            else:
                state["api_response"] = None
                state["api_error"] = f"APINode: Desteklenmeyen API tipi: {api_type}"
                return state
            state["api_error"] = None
        except Exception as e:
            state["api_response"] = None
            state["api_error"] = str(e)
        return state
        """
        İş akışından gelen işleme göre ilgili e-ticaret API'sine istek atar ve yanıtı state'e ekler.
        """
        api_type = state.get("api_type")  # Örn: 'shopify', 'woocommerce'
        api_payload = state.get("api_payload")
        if not api_type or not api_payload:
            logger.error("APINode: API tipi veya payload eksik!")
            state["api_error"] = "APINode: API tipi veya payload eksik."
            return state
        try:
            if api_type == "shopify":
                # Shopify API örneği (geliştirilebilir)
                url = api_payload.get("url")
                headers = api_payload.get("headers", {})
                data = api_payload.get("data", {})
                resp = requests.post(url, headers=headers, json=data)
                state["api_response"] = resp.json()
            elif api_type == "woocommerce":
                # WooCommerce API örneği (geliştirilebilir)
                url = api_payload.get("url")
                headers = api_payload.get("headers", {})
                data = api_payload.get("data", {})
                resp = requests.post(url, headers=headers, json=data)
                state["api_response"] = resp.json()
            else:
                logger.warning(f"APINode: Desteklenmeyen API tipi: {api_type}")
                state["api_response"] = None
                state["api_error"] = f"APINode: Desteklenmeyen API tipi: {api_type}"
                return state
            state["api_error"] = None
            logger.info(f"APINode: {api_type} API çağrısı başarılı.")
        except Exception as e:
            logger.exception("APINode: API çağrısı başarısız.")
            state["api_response"] = None
            state["api_error"] = str(e)
        return state
