"""
LangChain entegrasyon test dosyası
"""
import asyncio
import sys
import os

# Proje root'unu Python path'ine ekle
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.langgraph.nodes.llm_node import LLMNode
from app.langgraph.nodes.tool_node import ToolNode, EcommerceTools

async def test_llm_node():
    """LLM Node'unu test et"""
    print("🧠 LLM Node Testi Başlıyor...")
    
    try:
        llm_node = LLMNode()
        
        # Test state'i oluştur
        test_state = {
            "workflow_type": "product_classification",
            "processed_data": {
                "product_title": "iPhone 15 Pro Max",
                "product_description": "Apple'ın en yeni akıllı telefonu, A17 Pro çip ile",
                "additional_info": {"brand": "Apple", "price": 45000}
            },
            "memory_context": {
                "conversation_history": [],
                "user_preferences": {"preferred_brands": ["Apple", "Samsung"]}
            }
        }
        
        # LLM Node'unu çalıştır
        result = await llm_node.run(test_state)
        
        print("✅ LLM Node Testi Başarılı!")
        print(f"📊 Sonuç: {result.get('llm_output', {}).get('category', 'N/A')}")
        print(f"🎯 Güven: {result.get('llm_output', {}).get('confidence', 'N/A')}")
        
    except Exception as e:
        print(f"❌ LLM Node Testi Başarısız: {str(e)}")

async def test_tool_node():
    """Tool Node'unu test et"""
    print("\n🔧 Tool Node Testi Başlıyor...")
    
    try:
        tool_node = ToolNode()
        
        # Test state'i oluştur
        test_state = {
            "workflow_type": "product_analysis",
            "processed_data": {
                "product_name": "iPhone"
            },
            "llm_output": {
                "category": "electronics",
                "confidence": 0.95
            }
        }
        
        # Tool Node'unu çalıştır
        result = await tool_node.run(test_state)
        
        print("✅ Tool Node Testi Başarılı!")
        print(f"🔍 Kullanılabilir Tool'lar: {tool_node.get_available_tools()}")
        print(f"📊 Tool Sonuçları: {list(result.get('tool_results', {}).keys())}")
        
    except Exception as e:
        print(f"❌ Tool Node Testi Başarısız: {str(e)}")

async def test_ecommerce_tools():
    """E-ticaret tool'larını test et"""
    print("\n🛒 E-ticaret Tool'ları Testi Başlıyor...")
    
    try:
        ecommerce_tools = EcommerceTools()
        
        # Fiyat karşılaştırma tool'u
        price_tool = ecommerce_tools.get_product_price_tool()
        price_result = price_tool.func("iPhone")
        print(f"💰 Fiyat Karşılaştırma: {price_result}")
        
        # Stok kontrol tool'u
        stock_tool = ecommerce_tools.get_stock_check_tool()
        stock_result = stock_tool.func("123")
        print(f"📦 Stok Kontrol: {stock_result}")
        
        # Müşteri yorumları tool'u
        review_tool = ecommerce_tools.get_customer_reviews_tool()
        review_result = review_tool.func("iPhone")
        print(f"⭐ Müşteri Yorumları: {review_result}")
        
        print("✅ E-ticaret Tool'ları Testi Başarılı!")
        
    except Exception as e:
        print(f"❌ E-ticaret Tool'ları Testi Başarısız: {str(e)}")

async def test_langchain_features():
    """LangChain özelliklerini test et"""
    print("\n🔗 LangChain Özellikleri Testi Başlıyor...")
    
    try:
        from langchain.prompts import ChatPromptTemplate
        from langchain.schema import HumanMessage, SystemMessage
        
        # Prompt template testi
        template = ChatPromptTemplate.from_messages([
            ("system", "Sen bir e-ticaret uzmanısın."),
            ("human", "Bu ürünü analiz et: {product_name}")
        ])
        
        messages = template.format_messages(product_name="Laptop")
        print(f"📝 Prompt Template: {len(messages)} mesaj oluşturuldu")
        
        # Output parser testi
        from langchain.output_parsers import PydanticOutputParser
        from pydantic import BaseModel, Field
        
        class TestOutput(BaseModel):
            result: str = Field(description="Test sonucu")
        
        parser = PydanticOutputParser(pydantic_object=TestOutput)
        format_instructions = parser.get_format_instructions()
        print(f"📋 Output Parser: Format talimatları oluşturuldu")
        
        print("✅ LangChain Özellikleri Testi Başarılı!")
        
    except Exception as e:
        print(f"❌ LangChain Özellikleri Testi Başarısız: {str(e)}")

async def main():
    """Ana test fonksiyonu"""
    print("🚀 LangChain Entegrasyon Testleri Başlıyor...\n")
    
    # Testleri sırayla çalıştır
    await test_langchain_features()
    await test_ecommerce_tools()
    await test_tool_node()
    await test_llm_node()
    
    print("\n🎉 Tüm testler tamamlandı!")

if __name__ == "__main__":
    # Environment variables'ları ayarla (test için)
    os.environ.setdefault("GEMINI_API_KEY", "test_key")
    
    # Testleri çalıştır
    asyncio.run(main()) 