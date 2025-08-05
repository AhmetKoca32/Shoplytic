from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
from app.langgraph.graph_builder import WorkflowGraph

from app.config.settings import get_settings, Settings
from app.utils.ecommerce_client import EcommerceClient

# Router oluştur
router = APIRouter()

# Pydantic modelleri
class WorkflowRequest(BaseModel):
    """İş akışı isteği modeli"""
    input_data: Dict[str, Any]
    workflow_type: str = "product_classification"
    user_id: Optional[str] = None

class WorkflowResponse(BaseModel):
    """İş akışı yanıt modeli"""
    success: bool
    result: Dict[str, Any]
    workflow_id: str
    execution_time: float



class MindMapGenerationRequest(BaseModel):
    """Zihin haritası oluşturma isteği"""
    user_input: str
    user_preferences: Optional[Dict[str, Any]] = None

# Dependency injection
def get_workflow_graph() -> WorkflowGraph:
    return WorkflowGraph()

def get_ecommerce_client() -> EcommerceClient:
    return EcommerceClient()

# Ana workflow endpoint'i
@router.post("/workflow/execute", response_model=WorkflowResponse)
async def execute_workflow(
    request: WorkflowRequest,
    workflow_graph: WorkflowGraph = Depends(get_workflow_graph)
):
    """Ana AI iş akışını çalıştır"""
    try:
        result = await workflow_graph.execute(
            input_data=request.input_data,
            workflow_type=request.workflow_type,
            user_id=request.user_id
        )
        
        return WorkflowResponse(
            success=True,
            result=result["output"],
            workflow_id=result["workflow_id"],
            execution_time=result["execution_time"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Workflow execution failed: {str(e)}")

# Ürün sınıflandırma endpoint'i


@router.post("/ai/generate-mindmap")
async def generate_mindmap(
    request: MindMapGenerationRequest,
    workflow_graph: WorkflowGraph = Depends(get_workflow_graph)
):
    """Zihin haritası oluştur"""
    try:
        result = await workflow_graph.execute(
            input_data={
                "user_input": request.user_input,
                "user_preferences": request.user_preferences or {}
            },
            workflow_type="mind_map_generation"
        )
        
        return {
            "success": True,
            "mind_map": result.get("output", {}),
            "workflow_id": result.get("workflow_id")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Mind map generation failed: {str(e)}")

# E-ticaret endpoint'leri
@router.get("/ecommerce/search")
async def search_products(
    query: str,
    category: str = None,
    limit: int = 5,
    ecommerce_client: EcommerceClient = Depends(get_ecommerce_client)
):
    """Ürün arama"""
    try:
        products = await ecommerce_client.search_products(query, category, limit)
        return {
            "success": True,
            "products": products,
            "query": query,
            "category": category
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Product search failed: {str(e)}")

@router.get("/ecommerce/recommendations/{category}")
async def get_recommendations(
    category: str,
    budget: float = None,
    ecommerce_client: EcommerceClient = Depends(get_ecommerce_client)
):
    """Kategori bazlı öneriler"""
    try:
        recommendations = await ecommerce_client.get_recommendations(category, budget)
        return {
            "success": True,
            "recommendations": recommendations,
            "category": category,
            "budget": budget
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Recommendations failed: {str(e)}")

@router.get("/ecommerce/compare/{product_name}")
async def compare_prices(
    product_name: str,
    ecommerce_client: EcommerceClient = Depends(get_ecommerce_client)
):
    """Fiyat karşılaştırması"""
    try:
        comparison = await ecommerce_client.compare_prices(product_name)
        return {
            "success": True,
            "comparison": comparison,
            "product_name": product_name
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Price comparison failed: {str(e)}")

@router.get("/ecommerce/stock/{product_id}")
async def check_stock(
    product_id: str,
    ecommerce_client: EcommerceClient = Depends(get_ecommerce_client)
):
    """Stok kontrolü"""
    try:
        stock_info = await ecommerce_client.check_stock(product_id)
        return {
            "success": True,
            "stock_info": stock_info
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Stock check failed: {str(e)}")

# Sistem durumu endpoint'leri
@router.get("/system/status")
async def get_system_status():
    """Sistem durumunu kontrol et"""
    return {
        "api_status": "healthy",
        "ai_service": "available",
        "langgraph": "ready",
        "timestamp": "2025-01-29T17:33:30Z"
    }