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

class ChatMessageRequest(BaseModel):
    """Chat mesaj isteği"""
    message: str
    user_id: Optional[str] = None
    conversation_id: Optional[str] = None
    context: Optional[Dict[str, Any]] = None

class ChatMessageResponse(BaseModel):
    """Chat mesaj yanıtı"""
    success: bool
    response: str
    conversation_id: str
    timestamp: str
    context: Optional[Dict[str, Any]] = None

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

@router.post("/ai/chat", response_model=ChatMessageResponse)
async def chat_with_ai(
    request: ChatMessageRequest,
    workflow_graph: WorkflowGraph = Depends(get_workflow_graph)
):
    """AI ile sohbet et"""
    try:
        import uuid
        from datetime import datetime
        
        print(f"💬 Chat isteği alındı: {request.message}")
        
        # Conversation ID oluştur
        conversation_id = request.conversation_id or str(uuid.uuid4())
        
        result = await workflow_graph.execute(
            input_data={
                "message": request.message,
                "user_id": request.user_id,
                "conversation_id": conversation_id,
                "context": request.context or {}
            },
            workflow_type="chat_conversation"
        )
        
        print(f"📊 Workflow result: {result}")
        
        # Final output'tan response'u al
        final_output = result.get("output", {})
        output = final_output.get("output", {})
        
        print(f"📤 Final output: {final_output}")
        print(f"📤 Output: {output}")
        
        # Response'u al, yoksa fallback mesajı kullan
        response = output.get("response", "Üzgünüm, şu anda yanıt veremiyorum.")
        context = output.get("context")
        
        print(f"💭 Response: {response}")
        
        return ChatMessageResponse(
            success=True,
            response=response,
            conversation_id=conversation_id,
            timestamp=datetime.now().isoformat(),
            context=context
        )
    except Exception as e:
        print(f"❌ Chat hatası: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Chat failed: {str(e)}")

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

@router.post("/ecommerce/search-by-category")
async def search_products_by_category(
    category: str,
    products: List[str],
    limit: int = 5
):
    """Kategori ve ürün listesine göre arama"""
    try:
        from app.services.ecommerce_service import EcommerceService
        
        ecommerce_service = EcommerceService()
        found_products = await ecommerce_service.search_products_by_category(
            category, products, limit
        )
        await ecommerce_service.close()
        
        return {
            "success": True,
            "products": found_products,
            "category": category,
            "searched_products": products
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Category search failed: {str(e)}")

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

# Test endpoint'i
@router.get("/test")
async def test_endpoint():
    """Test endpoint'i - bağlantı kontrolü için"""
    return {
        "message": "Backend bağlantısı başarılı!",
        "status": "connected",
        "timestamp": "2025-01-29T17:33:30Z"
    }

# Health check endpoint'i
@router.get("/health")
async def health_check():
    """Health check endpoint'i"""
    return {
        "status": "healthy",
        "timestamp": "2025-01-29T17:33:30Z",
        "version": "1.0.0"
    }

# Test ürün resim endpoint'i
@router.get("/test/products-with-images")
async def test_products_with_images():
    """Test ürünleri resimlerle birlikte döndür"""
    test_products = [
        {
            "id": "test_1",
            "name": "Test Laptop",
            "price": 15999.99,
            "platform": "Test Platform",
            "rating": 4.5,
            "stock": True,
            "url": "https://test.com/laptop",
            "image": "https://source.unsplash.com/300x300/?laptop",
            "category": "Elektronik",
            "description": "Test laptop ürünü"
        },
        {
            "id": "test_2",
            "name": "Test Mont",
            "price": 899.99,
            "platform": "Test Platform",
            "rating": 4.3,
            "stock": True,
            "url": "https://test.com/mont",
            "image": "https://source.unsplash.com/300x300/?winter+coat",
            "category": "Giyim",
            "description": "Test mont ürünü"
        }
    ]
    
    return {
        "success": True,
        "products": test_products,
        "message": "Test ürünleri resimlerle birlikte döndürüldü"
    }