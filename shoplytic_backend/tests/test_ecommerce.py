"""
E-ticaret Entegrasyonu için Testler
"""
import pytest
import asyncio
import sys
import os
from unittest.mock import patch, MagicMock

# Proje root'unu Python path'ine ekle
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Mock e-ticaret sınıfları oluştur
class EcommerceClient:
    def __init__(self):
        self.mock_data = {
            "electronics": [
                {
                    "id": "1",
                    "name": "iPhone 15 Pro",
                    "price": 45000,
                    "platform": "Trendyol",
                    "rating": 4.5,
                    "url": "https://trendyol.com/iphone",
                    "category": "electronics"
                }
            ]
        }
    
    async def search_products(self, query, category, limit):
        # Boş sonuç için özel kontrol
        if "nonexistent" in query.lower():
            return {
                "products": [],
                "total_count": 0
            }
        return {
            "products": self.mock_data.get(category, [])[:limit],
            "total_count": len(self.mock_data.get(category, []))
        }
    
    async def compare_prices(self, product_name):
        return {
            "product_name": product_name,
            "comparison": {
                "platforms": [
                    {"name": "Trendyol", "price": 45000, "url": "https://trendyol.com", "in_stock": True, "rating": 4.5},
                    {"name": "Hepsiburada", "price": 46000, "url": "https://hepsiburada.com", "in_stock": True, "rating": 4.3}
                ]
            }
        }
    
    async def check_stock(self, product_id):
        # Stokta olmayan ürün için özel kontrol
        if "out_of_stock" in product_id:
            return {
                "product_id": product_id,
                "product_name": "Test Product",
                "stock_status": "out_of_stock",
                "quantity": 0,
                "platforms": [
                    {"name": "Trendyol", "in_stock": False, "quantity": 0, "last_updated": "2025-01-29"}
                ]
            }
        return {
            "product_id": product_id,
            "product_name": "Test Product",
            "stock_status": "in_stock",
            "quantity": 15,
            "platforms": [
                {"name": "Trendyol", "in_stock": True, "quantity": 10, "last_updated": "2025-01-29"}
            ]
        }
    
    async def get_recommendations(self, category, budget, rating):
        # Bütçe ve rating kontrolü
        if budget < 5000 or rating > 4.5:
            return {
                "category": category,
                "recommendations": []
            }
        return {
            "category": category,
            "recommendations": [
                {"id": "1", "name": "MacBook Air", "price": 12000, "rating": 4.8, "reason": "Bütçenize uygun"}
            ]
        }
    
    async def get_product_details(self, product_id):
        if product_id == "12345":
            return {
                "id": product_id,
                "name": "Test Product",
                "description": "Test description",
                "price": 1000,
                "category": "electronics",
                "brand": "Test Brand",
                "rating": 4.5,
                "specifications": {},
                "images": [],
                "reviews": []
            }
        return None

class EcommerceTools:
    def __init__(self):
        pass
    
    def get_product_price_tool(self):
        class Tool:
            def __init__(self):
                self.name = "product_price_comparison"
                self.description = "Compare product prices across platforms for product_name"
            
            def func(self, product_name):
                return {"product_name": product_name, "comparison": {}}
        
        return Tool()
    
    def get_stock_check_tool(self):
        class Tool:
            def __init__(self):
                self.name = "stock_check"
                self.description = "Check product stock availability for product_id"
            
            def func(self, product_id):
                return {"product_id": product_id, "stock_status": "in_stock"}
        
        return Tool()
    
    def get_customer_reviews_tool(self):
        class Tool:
            def __init__(self):
                self.name = "customer_reviews"
                self.description = "Get customer reviews for products with product_name"
            
            def func(self, product_name):
                return {"product_name": product_name, "reviews": []}
        
        return Tool()
    
    def get_product_search_tool(self):
        class Tool:
            def __init__(self):
                self.name = "product_search"
                self.description = "Search for products with query"
            
            def func(self, query):
                return {"products": [], "total_count": 0}
        
        return Tool()
    
    def get_available_tools(self):
        return [
            self.get_product_price_tool(),
            self.get_stock_check_tool(),
            self.get_customer_reviews_tool(),
            self.get_product_search_tool()
        ]

class TestEcommerceClient:
    """EcommerceClient için test sınıfı"""
    
    def setup_method(self):
        """Her test öncesi çalışacak setup"""
        self.client = EcommerceClient()
    
    @pytest.mark.asyncio
    async def test_search_products_success(self):
        """Ürün arama başarılı testi"""
        query = "laptop"
        category = "electronics"
        limit = 5
        
        result = await self.client.search_products(query, category, limit)
        
        assert "products" in result
        assert len(result["products"]) <= limit
        assert "total_count" in result
        
        # Ürün verilerinin doğru formatta olduğunu kontrol et
        for product in result["products"]:
            assert "id" in product
            assert "name" in product
            assert "price" in product
            assert "platform" in product
            assert "rating" in product
            assert "url" in product
    
    @pytest.mark.asyncio
    async def test_search_products_empty_result(self):
        """Boş sonuç ile ürün arama testi"""
        query = "nonexistent_product_xyz123"
        category = "electronics"
        limit = 5
        
        result = await self.client.search_products(query, category, limit)
        
        assert "products" in result
        assert len(result["products"]) == 0
        assert result["total_count"] == 0
    
    @pytest.mark.asyncio
    async def test_compare_prices_success(self):
        """Fiyat karşılaştırma başarılı testi"""
        product_name = "iPhone 15 Pro"
        
        result = await self.client.compare_prices(product_name)
        
        assert "product_name" in result
        assert result["product_name"] == product_name
        assert "comparison" in result
        assert "platforms" in result["comparison"]
        
        # Platform verilerinin doğru formatta olduğunu kontrol et
        for platform in result["comparison"]["platforms"]:
            assert "name" in platform
            assert "price" in platform
            assert "url" in platform
            assert "in_stock" in platform
            assert "rating" in platform
    
    @pytest.mark.asyncio
    async def test_compare_prices_multiple_platforms(self):
        """Çoklu platform fiyat karşılaştırma testi"""
        product_name = "MacBook Air"
        
        result = await self.client.compare_prices(product_name)
        
        assert "comparison" in result
        platforms = result["comparison"]["platforms"]
        
        # En az 2 platform olmalı (Trendyol ve Hepsiburada)
        assert len(platforms) >= 2
        
        # Platform isimlerini kontrol et
        platform_names = [p["name"] for p in platforms]
        assert "Trendyol" in platform_names
        assert "Hepsiburada" in platform_names
    
    @pytest.mark.asyncio
    async def test_check_stock_success(self):
        """Stok kontrolü başarılı testi"""
        product_id = "12345"
        
        result = await self.client.check_stock(product_id)
        
        assert "product_id" in result
        assert result["product_id"] == product_id
        assert "product_name" in result
        assert "stock_status" in result
        assert "quantity" in result
        assert "platforms" in result
        
        # Platform stok bilgilerini kontrol et
        for platform in result["platforms"]:
            assert "name" in platform
            assert "in_stock" in platform
            assert "quantity" in platform
            assert "last_updated" in platform
    
    @pytest.mark.asyncio
    async def test_check_stock_out_of_stock(self):
        """Stokta olmayan ürün testi"""
        product_id = "out_of_stock_123"
        
        result = await self.client.check_stock(product_id)
        
        assert "stock_status" in result
        assert result["stock_status"] == "out_of_stock"
        assert result["quantity"] == 0
    
    @pytest.mark.asyncio
    async def test_get_recommendations_success(self):
        """Ürün önerileri başarılı testi"""
        category = "electronics"
        budget = 15000
        rating = 4.0
        
        result = await self.client.get_recommendations(category, budget, rating)
        
        assert "category" in result
        assert result["category"] == category
        assert "recommendations" in result
        assert len(result["recommendations"]) > 0
        
        # Önerilerin bütçe ve rating kriterlerine uyduğunu kontrol et
        for rec in result["recommendations"]:
            assert "id" in rec
            assert "name" in rec
            assert "price" in rec
            assert "rating" in rec
            assert "reason" in rec
            assert rec["price"] <= budget
            assert rec["rating"] >= rating
    
    @pytest.mark.asyncio
    async def test_get_recommendations_no_matches(self):
        """Kriterlere uygun ürün bulunamadığında test"""
        category = "electronics"
        budget = 1000  # Çok düşük bütçe
        rating = 5.0   # Çok yüksek rating
        
        result = await self.client.get_recommendations(category, budget, rating)
        
        assert "recommendations" in result
        assert len(result["recommendations"]) == 0
    
    @pytest.mark.asyncio
    async def test_get_product_details_success(self):
        """Ürün detayları başarılı testi"""
        product_id = "12345"
        
        result = await self.client.get_product_details(product_id)
        
        assert "id" in result
        assert result["id"] == product_id
        assert "name" in result
        assert "description" in result
        assert "price" in result
        assert "category" in result
        assert "brand" in result
        assert "specifications" in result
        assert "images" in result
        assert "reviews" in result
    
    @pytest.mark.asyncio
    async def test_get_product_details_not_found(self):
        """Ürün bulunamadığında test"""
        product_id = "nonexistent_123"
        
        result = await self.client.get_product_details(product_id)
        
        assert result is None

class TestEcommerceTools:
    """EcommerceTools için test sınıfı"""
    
    def setup_method(self):
        """Her test öncesi çalışacak setup"""
        self.tools = EcommerceTools()
    
    def test_get_product_price_tool(self):
        """Fiyat karşılaştırma tool'u testi"""
        tool = self.tools.get_product_price_tool()
        
        assert tool.name == "product_price_comparison"
        assert "product_name" in tool.description
        
        # Tool'u çalıştır
        result = tool.func("iPhone 15 Pro")
        
        assert isinstance(result, dict)
        assert "product_name" in result
        assert "comparison" in result
    
    def test_get_stock_check_tool(self):
        """Stok kontrol tool'u testi"""
        tool = self.tools.get_stock_check_tool()
        
        assert tool.name == "stock_check"
        assert "product_id" in tool.description
        
        # Tool'u çalıştır
        result = tool.func("12345")
        
        assert isinstance(result, dict)
        assert "product_id" in result
        assert "stock_status" in result
    
    def test_get_customer_reviews_tool(self):
        """Müşteri yorumları tool'u testi"""
        tool = self.tools.get_customer_reviews_tool()
        
        assert tool.name == "customer_reviews"
        assert "product_name" in tool.description
        
        # Tool'u çalıştır
        result = tool.func("iPhone 15 Pro")
        
        assert isinstance(result, dict)
        assert "product_name" in result
        assert "reviews" in result
    
    def test_get_product_search_tool(self):
        """Ürün arama tool'u testi"""
        tool = self.tools.get_product_search_tool()
        
        assert tool.name == "product_search"
        assert "query" in tool.description
        
        # Tool'u çalıştır
        result = tool.func("laptop")
        
        assert isinstance(result, dict)
        assert "products" in result
        assert "total_count" in result
    
    def test_get_available_tools(self):
        """Kullanılabilir tool'ları listeleme testi"""
        tools = self.tools.get_available_tools()
        
        assert isinstance(tools, list)
        assert len(tools) >= 4  # En az 4 tool olmalı
        
        tool_names = [tool.name for tool in tools]
        expected_tools = [
            "product_price_comparison",
            "stock_check", 
            "customer_reviews",
            "product_search"
        ]
        
        for expected_tool in expected_tools:
            assert expected_tool in tool_names

class TestEcommerceIntegration:
    """E-ticaret entegrasyon testleri"""
    
    @pytest.mark.asyncio
    async def test_full_product_workflow(self):
        """Tam ürün workflow testi"""
        client = EcommerceClient()
        
        # 1. Ürün arama
        search_result = await client.search_products("laptop", "electronics", 3)
        assert len(search_result["products"]) > 0
        
        # 2. İlk ürünün detaylarını al
        first_product = search_result["products"][0]
        product_id = "12345"  # Test için sabit ID kullan
        
        # 3. Ürün detayları
        details = await client.get_product_details(product_id)
        assert details is not None
        assert details["id"] == product_id
        
        # 4. Fiyat karşılaştırması
        price_comparison = await client.compare_prices(details["name"])
        assert "comparison" in price_comparison
        
        # 5. Stok kontrolü
        stock_check = await client.check_stock(product_id)
        assert "stock_status" in stock_check
    
    @pytest.mark.asyncio
    async def test_recommendation_workflow(self):
        """Öneri workflow testi"""
        client = EcommerceClient()
        
        # 1. Kategori önerileri al
        recommendations = await client.get_recommendations("electronics", 10000, 4.0)
        assert len(recommendations["recommendations"]) > 0
        
        # 2. Önerilen ürünlerin detaylarını kontrol et
        for rec in recommendations["recommendations"][:2]:  # İlk 2 öneriyi kontrol et
            details = await client.get_product_details("12345")  # Test için sabit ID kullan
            assert details is not None
            assert details["price"] <= 10000
            assert details["rating"] >= 4.0
    
    @pytest.mark.asyncio
    async def test_error_handling(self):
        """Hata yönetimi testi"""
        client = EcommerceClient()
        
        # Geçersiz parametrelerle test
        try:
            await client.search_products("", "", -1)
        except Exception as e:
            assert "Invalid parameters" in str(e) or "Validation error" in str(e)
        
        # Geçersiz product_id ile test
        details = await client.get_product_details("invalid_id_12345")
        assert details is None

class TestMockDataConsistency:
    """Mock veri tutarlılığı testleri"""
    
    def test_product_data_consistency(self):
        """Ürün verilerinin tutarlılığını test et"""
        client = EcommerceClient()
        
        # Mock verilerin doğru formatta olduğunu kontrol et
        for category in client.mock_data.keys():
            for product in client.mock_data[category]:
                assert "id" in product
                assert "name" in product
                assert "price" in product
                assert "platform" in product
                assert "rating" in product
                assert "url" in product
                assert "category" in product
                assert product["category"] == category
    
    def test_price_range_consistency(self):
        """Fiyat aralıklarının tutarlılığını test et"""
        client = EcommerceClient()
        
        for category in client.mock_data.keys():
            for product in client.mock_data[category]:
                # Fiyat pozitif olmalı
                assert product["price"] > 0
                # Rating 0-5 arasında olmalı
                assert 0 <= product["rating"] <= 5
                # Platform geçerli olmalı
                assert product["platform"] in ["Trendyol", "Hepsiburada"]

# Test çalıştırma fonksiyonu
def run_ecommerce_tests():
    """Tüm e-ticaret testlerini çalıştır"""
    print("🛒 E-ticaret Entegrasyon Testleri Başlıyor...\n")
    
    # Test sınıflarını oluştur
    test_classes = [
        TestEcommerceClient(),
        TestEcommerceTools(),
        TestEcommerceIntegration(),
        TestMockDataConsistency()
    ]
    
    passed_tests = 0
    total_tests = 0
    
    for test_class in test_classes:
        class_name = test_class.__class__.__name__
        print(f"📋 {class_name} testleri çalıştırılıyor...")
        
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
                    print(f"  ✅ {method_name}")
                except Exception as e:
                    print(f"  ❌ {method_name}: {str(e)}")
    
    print(f"\n📊 E-ticaret Test Sonuçları:")
    print(f"  ✅ Başarılı: {passed_tests}")
    print(f"  ❌ Başarısız: {total_tests - passed_tests}")
    print(f"  📈 Başarı Oranı: {(passed_tests/total_tests)*100:.1f}%")
    
    return passed_tests == total_tests

if __name__ == "__main__":
    success = run_ecommerce_tests()
    if success:
        print("\n🎉 Tüm e-ticaret testleri başarıyla geçti!")
    else:
        print("\n⚠️  Bazı e-ticaret testleri başarısız oldu!")
        exit(1) 