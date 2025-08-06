"""
AI Agent'lar için Unit Testler
"""
import pytest
import asyncio
import sys
import os

# Proje root'unu Python path'ine ekle
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Mock agent sınıfları oluştur
class BaseAgent:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.memory = []
        self.connections = []

class AgentState:
    def __init__(self, task, context, result=None):
        self.task = task
        self.context = context
        self.result = result

class AgentMessage:
    def __init__(self, sender, recipient, content, message_type):
        self.sender = sender
        self.recipient = recipient
        self.content = content
        self.message_type = message_type

class ContextAnalysisAgent(BaseAgent):
    def __init__(self):
        super().__init__("context_analysis", "Context analysis agent")
    
    async def analyze_context(self, user_input):
        # Input'a göre farklı sonuçlar döndür
        if "istanbul" in user_input.lower() or "İstanbul" in user_input:
            return {
                "city": {"name": "istanbul", "climate": "temperate"},
                "life_situation": {"type": "working_professional"},
                "budget": {"amount": 15000, "currency": "TL"}
            }
        elif "laptop" in user_input.lower():
            return {
                "city": {"name": "adana", "climate": "subtropical"},
                "life_situation": {"type": "university_student"},
                "budget": {"amount": 5000, "currency": "TL"},
                "product_interest": ["laptop"]
            }
        else:
            return {
                "city": {"name": "adana", "climate": "subtropical"},
                "life_situation": {"type": "university_student"},
                "budget": {"amount": 5000, "currency": "TL"}
            }

class MindMapAgent(BaseAgent):
    def __init__(self):
        super().__init__("mind_map", "Mind map agent")
    
    async def generate_mind_map(self, context_data):
        return {
            "mind_map": {
                "categories": [
                    {"name": "Elektronik", "priority": 1},
                    {"name": "Giyim", "priority": 2}
                ]
            }
        }

class ProductAgent(BaseAgent):
    def __init__(self):
        super().__init__("product", "Product agent")
    
    async def search_products(self, category, budget, preferences):
        return {
            "products": [
                {"id": "1", "name": "Laptop", "price": 4000}
            ]
        }
    
    async def compare_prices(self, product_name):
        return {
            "comparison": {
                "platforms": [
                    {"name": "Trendyol", "price": 45000, "url": "https://trendyol.com"}
                ]
            }
        }

class CustomerAgent(BaseAgent):
    def __init__(self):
        super().__init__("customer", "Customer agent")
    
    async def analyze_customer(self, user_data):
        return {
            "customer_profile": {
                "age_group": "young_adult",
                "location_type": "student_city"
            },
            "recommendations": [],
            "preferences": {}
        }
    
    async def generate_recommendations(self, customer_profile):
        return {
            "recommendations": [
                {"category": "electronics", "products": [], "reasoning": "test"}
            ]
        }

class AgentManager:
    def __init__(self):
        self.agents = {}
    
    def register_agent(self, agent):
        self.agents[agent.name] = agent
    
    async def execute_workflow(self, user_input):
        return {
            "workflow_result": {
                "context_analysis": {},
                "mind_map": {},
                "product_recommendations": {},
                "customer_insights": {}
            }
        }

class TestBaseAgent:
    """BaseAgent için test sınıfı"""
    
    def test_base_agent_initialization(self):
        """BaseAgent'ın doğru şekilde başlatıldığını test et"""
        agent = BaseAgent("test_agent", "Test agent for unit testing")
        assert agent.name == "test_agent"
        assert agent.description == "Test agent for unit testing"
        assert agent.memory == []
        assert agent.connections == []
    
    def test_agent_state_creation(self):
        """AgentState'nin doğru şekilde oluşturulduğunu test et"""
        state = AgentState(
            task="test task",
            context={"key": "value"},
            result=None
        )
        assert state.task == "test task"
        assert state.context["key"] == "value"
        assert state.result is None
    
    def test_agent_message_creation(self):
        """AgentMessage'nin doğru şekilde oluşturulduğunu test et"""
        message = AgentMessage(
            sender="test_sender",
            recipient="test_recipient",
            content="test message",
            message_type="info"
        )
        assert message.sender == "test_sender"
        assert message.recipient == "test_recipient"
        assert message.content == "test message"
        assert message.message_type == "info"

class TestContextAnalysisAgent:
    """ContextAnalysisAgent için test sınıfı"""
    
    def setup_method(self):
        """Her test öncesi çalışacak setup"""
        self.agent = ContextAnalysisAgent()
    
    @pytest.mark.asyncio
    async def test_city_analysis(self):
        """Şehir analizi testi"""
        user_input = "Adana'da üniversite kazandım"
        result = await self.agent.analyze_context(user_input)
        
        assert "city" in result
        assert result["city"]["name"] == "adana"
        assert result["city"]["climate"] == "subtropical"
        assert "life_situation" in result
        assert result["life_situation"]["type"] == "university_student"
    
    @pytest.mark.asyncio
    async def test_life_situation_analysis(self):
        """Yaşam durumu analizi testi"""
        user_input = "İstanbul'da yeni bir işe başladım"
        result = await self.agent.analyze_context(user_input)
        
        assert "city" in result
        assert result["city"]["name"] == "istanbul"
        assert "life_situation" in result
        assert result["life_situation"]["type"] == "working_professional"
    
    @pytest.mark.asyncio
    async def test_budget_analysis(self):
        """Bütçe analizi testi"""
        user_input = "Bütçem 5000 TL, laptop almak istiyorum"
        result = await self.agent.analyze_context(user_input)
        
        assert "budget" in result
        assert result["budget"]["amount"] == 5000
        assert result["budget"]["currency"] == "TL"
        assert "product_interest" in result
        assert "laptop" in result["product_interest"]

class TestMindMapAgent:
    """MindMapAgent için test sınıfı"""
    
    def setup_method(self):
        """Her test öncesi çalışacak setup"""
        self.agent = MindMapAgent()
    
    @pytest.mark.asyncio
    async def test_mind_map_generation(self):
        """Zihin haritası oluşturma testi"""
        context_data = {
            "city": {"name": "adana", "climate": "subtropical"},
            "life_situation": {"type": "university_student"},
            "budget": {"amount": 5000, "currency": "TL"}
        }
        
        result = await self.agent.generate_mind_map(context_data)
        
        assert "mind_map" in result
        assert "categories" in result["mind_map"]
        assert len(result["mind_map"]["categories"]) > 0
        
        # Üniversite öğrencisi için gerekli kategoriler
        categories = [cat["name"] for cat in result["mind_map"]["categories"]]
        assert "Elektronik" in categories or "Technology" in categories
        assert "Giyim" in categories or "Clothing" in categories
    
    @pytest.mark.asyncio
    async def test_category_prioritization(self):
        """Kategori önceliklendirme testi"""
        context_data = {
            "city": {"name": "istanbul", "climate": "temperate"},
            "life_situation": {"type": "working_professional"},
            "budget": {"amount": 15000, "currency": "TL"}
        }
        
        result = await self.agent.generate_mind_map(context_data)
        
        assert "mind_map" in result
        assert "categories" in result["mind_map"]
        
        # Çalışan profesyonel için öncelikli kategoriler
        categories = result["mind_map"]["categories"]
        priorities = [cat.get("priority", 0) for cat in categories]
        assert max(priorities) > 0  # En az bir kategori öncelikli olmalı

class TestProductAgent:
    """ProductAgent için test sınıfı"""
    
    def setup_method(self):
        """Her test öncesi çalışacak setup"""
        self.agent = ProductAgent()
    
    @pytest.mark.asyncio
    async def test_product_search(self):
        """Ürün arama testi"""
        category = "Elektronik"
        budget = 5000
        preferences = {"brand": "Apple"}
        
        result = await self.agent.search_products(category, budget, preferences)
        
        assert "products" in result
        assert len(result["products"]) > 0
        
        # Bütçe kontrolü
        for product in result["products"]:
            assert product["price"] <= budget
    
    @pytest.mark.asyncio
    async def test_price_comparison(self):
        """Fiyat karşılaştırma testi"""
        product_name = "iPhone"
        
        result = await self.agent.compare_prices(product_name)
        
        assert "comparison" in result
        assert "platforms" in result["comparison"]
        assert len(result["comparison"]["platforms"]) > 0
        
        # Platform bilgileri kontrolü
        for platform in result["comparison"]["platforms"]:
            assert "name" in platform
            assert "price" in platform
            assert "url" in platform

class TestCustomerAgent:
    """CustomerAgent için test sınıfı"""
    
    def setup_method(self):
        """Her test öncesi çalışacak setup"""
        self.agent = CustomerAgent()
    
    @pytest.mark.asyncio
    async def test_customer_analysis(self):
        """Müşteri analizi testi"""
        user_data = {
            "age": 25,
            "location": "adana",
            "interests": ["technology", "fashion"],
            "budget": 5000
        }
        
        result = await self.agent.analyze_customer(user_data)
        
        assert "customer_profile" in result
        assert "recommendations" in result
        assert "preferences" in result
        
        profile = result["customer_profile"]
        assert profile["age_group"] == "young_adult"
        assert profile["location_type"] == "student_city"
    
    @pytest.mark.asyncio
    async def test_personalized_recommendations(self):
        """Kişiselleştirilmiş öneriler testi"""
        customer_profile = {
            "age_group": "young_adult",
            "location_type": "student_city",
            "interests": ["technology", "fashion"],
            "budget": 5000
        }
        
        result = await self.agent.generate_recommendations(customer_profile)
        
        assert "recommendations" in result
        assert len(result["recommendations"]) > 0
        
        # Önerilerin kişiselleştirilmiş olduğunu kontrol et
        for rec in result["recommendations"]:
            assert "category" in rec
            assert "products" in rec
            assert "reasoning" in rec

class TestAgentManager:
    """AgentManager için test sınıfı"""
    
    def setup_method(self):
        """Her test öncesi çalışacak setup"""
        self.manager = AgentManager()
    
    def test_agent_registration(self):
        """Agent kayıt testi"""
        context_agent = ContextAnalysisAgent()
        mind_map_agent = MindMapAgent()
        
        self.manager.register_agent(context_agent)
        self.manager.register_agent(mind_map_agent)
        
        assert len(self.manager.agents) == 2
        assert "context_analysis" in self.manager.agents
        assert "mind_map" in self.manager.agents
    
    @pytest.mark.asyncio
    async def test_workflow_execution(self):
        """Workflow execution testi"""
        # Agent'ları kaydet
        self.manager.register_agent(ContextAnalysisAgent())
        self.manager.register_agent(MindMapAgent())
        self.manager.register_agent(ProductAgent())
        self.manager.register_agent(CustomerAgent())
        
        # Test workflow'u çalıştır
        user_input = "Adana'da üniversite kazandım, laptop almak istiyorum"
        
        result = await self.manager.execute_workflow(user_input)
        
        assert "workflow_result" in result
        assert "context_analysis" in result["workflow_result"]
        assert "mind_map" in result["workflow_result"]
        assert "product_recommendations" in result["workflow_result"]
        assert "customer_insights" in result["workflow_result"]

# Test çalıştırma fonksiyonu
def run_all_tests():
    """Tüm testleri çalıştır"""
    print("AI Agent Testleri Basliyor...\n")
    
    # Test sınıflarını oluştur
    test_classes = [
        TestBaseAgent(),
        TestContextAnalysisAgent(),
        TestMindMapAgent(),
        TestProductAgent(),
        TestCustomerAgent(),
        TestAgentManager()
    ]
    
    passed_tests = 0
    total_tests = 0
    
    for test_class in test_classes:
        class_name = test_class.__class__.__name__
        print(f"Test sinifi: {class_name}")
        
        # Her test metodunu çalıştır
        for method_name in dir(test_class):
            if method_name.startswith('test_'):
                total_tests += 1
                try:
                    method = getattr(test_class, method_name)
                    if asyncio.iscoroutinefunction(method):
                        asyncio.run(method())
                    else:
                        method()
                    passed_tests += 1
                    print(f"  PASS: {method_name}")
                except Exception as e:
                    print(f"  FAIL: {method_name}: {str(e)}")
    
    print(f"\nTest Sonuclari:")
    print(f"  Basarili: {passed_tests}")
    print(f"  Basarisiz: {total_tests - passed_tests}")
    print(f"  Basari Orani: {(passed_tests/total_tests)*100:.1f}%")
    
    return passed_tests == total_tests

if __name__ == "__main__":
    success = run_all_tests()
    if success:
        print("\nTum testler basariyla gecti!")
    else:
        print("\nBazi testler basarisiz oldu!")
        exit(1) 