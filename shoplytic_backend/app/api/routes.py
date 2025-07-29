from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
from app.langgraph.graph_builder import WorkflowGraph
from app.services.ai_service import AIService
from app.services.ecommerce_service import EcommerceService
from app.config.settings import get_settings, Settings

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

class ProductClassificationRequest(BaseModel):
    """Ürün sınıflandırma isteği"""
    product_description: str
    product_title: str
    additional_info: Optional[Dict[str, Any]] = None

class ProductRecommendationRequest(BaseModel):
    """Ürün öneri isteği"""
    cart_items: List[Dict[str, Any]]
    user_preferences: Optional[Dict[str, Any]] = None
    limit: int = 5

class CustomerSegmentationRequest(BaseModel):
    """Müşteri segmentasyon isteği"""
    customer_data: Dict[str, Any]
    purchase_history: List[Dict[str, Any]]

# Dependency injection
def get_ai_service(settings: Settings = Depends(get_settings)) -> AIService:
    return AIService(settings)

def get_ecommerce_service(settings: Settings = Depends(get_settings)) -> EcommerceService:
    return EcommerceService(settings)

def get_workflow_graph() -> WorkflowGraph:
    return WorkflowGraph()

# Ana workflow endpoint'i
@router.post("/workflow/execute", response_model=WorkflowResponse)
async def execute_workflow(
    request: WorkflowRequest,
    workflow_graph: WorkflowGraph = Depends(get_workflow_graph),
    ai_service: AIService = Depends(get_ai_service)
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
@router.post("/ai/classify-product")
async def classify_product(
    request: ProductClassificationRequest,
    ai_service: AIService = Depends(get_ai_service)
):
    """Ürünü AI ile sınıflandır"""
    try:
        classification = await ai_service.classify_product(
            title=request.product_title,
            description=request.product_description,
            additional_info=request.additional_info
        )
        
        return {
            "success": True,
            "classification": classification
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Product classification failed: {str(e)}")

# Ürün öneri endpoint'i
@router.post("/ai/recommend-products")
async def recommend_products(
    request: ProductRecommendationRequest,
    ai_service: AIService = Depends(get_ai_service)
):
    """Sepet içeriğine göre ürün öner"""
    try:
        recommendations = await ai_service.recommend_products(
            cart_items=request.cart_items,
            user_preferences=request.user_preferences,
            limit=request.limit
        )
        
        return {
            "success": True,
            "recommendations": recommendations
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Product recommendation failed: {str(e)}")

# Müşteri segmentasyon endpoint'i
@router.post("/ai/segment-customer")
async def segment_customer(
    request: CustomerSegmentationRequest,
    ai_service: AIService = Depends(get_ai_service)
):
    """Müşteriyi AI ile segmentlere ayır"""
    try:
        segmentation = await ai_service.segment_customer(
            customer_data=request.customer_data,
            purchase_history=request.purchase_history
        )
        
        return {
            "success": True,
            "segmentation": segmentation
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Customer segmentation failed: {str(e)}")

# E-ticaret entegrasyon endpoint'leri
@router.get("/ecommerce/products")
async def get_products(
    platform: str = "shopify",
    limit: int = 50,
    ecommerce_service: EcommerceService = Depends(get_ecommerce_service)
):
    """E-ticaret platformundan ürünleri getir"""
    try:
        products = await ecommerce_service.get_products(platform=platform, limit=limit)
        return {
            "success": True,
            "products": products,
            "platform": platform
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch products: {str(e)}")

@router.post("/ecommerce/webhook")
async def handle_webhook(
    payload: Dict[str, Any],
    platform: str = "shopify",
    workflow_graph: WorkflowGraph = Depends(get_workflow_graph)
):
    """E-ticaret webhook'larını işle"""
    try:
        # Webhook'u workflow'a yönlendir
        result = await workflow_graph.handle_webhook(
            payload=payload,
            platform=platform
        )
        
        return {
            "success": True,
            "message": "Webhook processed successfully",
            "result": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Webhook processing failed: {str(e)}")

# n8n entegrasyon endpoint'i
@router.post("/n8n/trigger")
async def trigger_n8n_workflow(
    workflow_data: Dict[str, Any],
    workflow_id: str,
    ecommerce_service: EcommerceService = Depends(get_ecommerce_service)
):
    """n8n workflow'unu tetikle"""
    try:
        result = await ecommerce_service.trigger_n8n_workflow(
            workflow_id=workflow_id,
            data=workflow_data
        )
        
        return {
            "success": True,
            "n8n_result": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"n8n workflow trigger failed: {str(e)}")

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