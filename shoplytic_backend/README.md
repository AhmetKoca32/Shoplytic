# 🧠 Shoplytic Backend - Dosya Yapısı ve İşlevler

## 📁 Proje Yapısı

```
shoplytic_backend/
├── app/                          # Ana uygulama klasörü
│   ├── agents/                   # AI Agent'lar
│   ├── api/                      # FastAPI endpoint'leri
│   ├── config/                   # Konfigürasyon dosyaları
│   ├── langgraph/                # LangGraph workflow sistemi
│   └── utils/                    # Yardımcı fonksiyonlar
├── tests/                        # Test dosyaları
├── main.py                       # Uygulama giriş noktası
├── requirements.txt              # Python bağımlılıkları
└── docker_compose.yml           # Docker konfigürasyonu
```

## 🔧 Ana Dosyalar

### **main.py**
**İşlev**: FastAPI uygulamasının giriş noktası
- CORS middleware kurulumu
- API router'larının dahil edilmesi
- Health check endpoint'i
- Uygulama başlatma konfigürasyonu

### **requirements.txt**
**İşlev**: Python paket bağımlılıkları
- LangGraph, LangChain, FastAPI
- Google Gemini AI entegrasyonu
- Gerekli utility kütüphaneleri

### **docker_compose.yml**
**İşlev**: Docker container konfigürasyonu
- Backend servis tanımları
- Port mapping
- Environment variables

## 🤖 AI Agent Sistemi (`app/agents/`)

### **base_agent.py**
**İşlev**: Tüm AI agent'lar için temel sınıf
- `BaseAgent` abstract class
- `AgentState` ve `AgentMessage` modelleri
- Ortak metodlar: `process_task()`, `think()`, `connect_agent()`
- Hafıza yönetimi ve mesajlaşma sistemi

### **context_analysis_agent.py**
**İşlev**: Kullanıcı durumu analizi
- Lokasyon tespiti (şehir, iklim)
- Yaşam durumu analizi (öğrenci, iş, ev)
- Mevsimsel ihtiyaç analizi
- Bütçe ve öncelik belirleme

**Özellikler**:
```python
city_data = {
    "adana": {"climate": "subtropical", "winter_temp": "5-15°C"}
}
life_situations = {
    "university_student": {"needs": ["laptop", "çanta"]}
}
```

### **mind_map_agent.py**
**İşlev**: Zihin haritası oluşturma
- Kategori organizasyonu
- Öncelik sıralaması
- Görsel yapı oluşturma
- Dinamik güncelleme

**Çıktı Formatı**:
```json
{
    "central_topic": "Adana Üniversite Hazırlığı",
    "main_categories": [
        {"name": "Akademik Malzemeler", "items": ["laptop", "çanta"]}
    ]
}
```

### **product_agent.py**
**İşlev**: Ürün analizi ve önerileri
- Ürün kategorilendirme
- Özellik çıkarma
- Rakip analizi
- Trend analizi

### **customer_agent.py**
**İşlev**: Müşteri segmentasyonu
- Müşteri davranış analizi
- Churn tahmini
- Lifetime value hesaplama
- Kişiselleştirilmiş öneriler

### **agent_manager.py**
**İşlev**: AI agent'ların yönetimi
- Agent lifecycle yönetimi
- Workflow orchestration
- Agent'lar arası iletişim
- Mesaj kuyruğu yönetimi

**Desteklenen Workflow'lar**:
- `product_analysis`
- `customer_analysis`
- `integrated_analysis`
- `mind_map_generation`

## 🔄 LangGraph Workflow Sistemi (`app/langgraph/`)

### **graph_builder.py**
**İşlev**: Ana workflow builder
- `WorkflowState` modeli
- `WorkflowGraph` sınıfı
- Node'ların bağlantıları
- Workflow execution logic

**Workflow Akışı**:
```
Entry → Memory → Prompt → LLM → Tool → Agent → Process → Output
```

### **nodes/entry_node.py**
**İşlev**: Workflow giriş noktası
- Giriş verilerini alır
- Workflow ID oluşturur
- Başlangıç state'ini hazırlar

### **nodes/prompt_node.py**
**İşlev**: Dinamik prompt oluşturma
- Kullanıcı girişine göre prompt üretir
- Context-aware prompt generation
- Template-based prompt sistemi

### **nodes/llm_node.py**
**İşlev**: LangChain LLM entegrasyonu
- Google Gemini AI çağrıları
- Pydantic output parsing
- Structured output handling
- Error handling ve retry logic

**Desteklenen Çıktı Formatları**:
- `ProductClassification`
- `ProductRecommendation`
- `GeneralTask`

### **nodes/tool_node.py**
**İşlev**: LangChain araçları
- Web search (DuckDuckGo)
- Wikipedia queries
- E-ticaret araçları
- Custom tool implementations

**Araçlar**:
- `DuckDuckGoSearchRun`
- `WikipediaQueryRun`
- `EcommerceTools` (fiyat, stok, yorumlar)

### **nodes/agent_node.py**
**İşlev**: AI Agent interface
- AgentManager ile entegrasyon
- Workflow routing
- Agent sonuçlarını toplama
- State management

### **nodes/memory_node.py**
**İşlev**: MCP (MessageContextPersistence)
- Konuşma geçmişi yönetimi
- Kullanıcı tercihleri
- Benzer workflow'ları hatırlama
- Context preservation

### **nodes/process_node.py**
**İşlev**: Veri işleme
- Agent sonuçlarını birleştirme
- Veri formatlama
- Error handling
- Execution steps tracking

### **nodes/output_node.py**
**İşlev**: Sonuç formatlama
- Final output oluşturma
- Response formatting
- Metadata ekleme
- Success/error handling

## 🌐 API Sistemi (`app/api/`)

### **routes.py**
**İşlev**: FastAPI endpoint'leri
- REST API tanımları
- Request/response modelleri
- Dependency injection
- Error handling

**Endpoint'ler**:
- `POST /workflow/execute` - Genel workflow execution
- `POST /ai/generate-mindmap` - Zihin haritası oluşturma
- `GET /ecommerce/search` - Ürün arama
- `GET /ecommerce/recommendations/{category}` - Kategori önerileri
- `GET /ecommerce/compare/{product_name}` - Fiyat karşılaştırması
- `GET /ecommerce/stock/{product_id}` - Stok kontrolü
- `GET /system/status` - Sistem durumu

**Pydantic Modelleri**:
- `WorkflowRequest` / `WorkflowResponse`
- `MindMapGenerationRequest`

## 🛒 E-ticaret Entegrasyonu (`app/utils/`)

### **ecommerce_client.py**
**İşlev**: E-ticaret platformları entegrasyonu
- Ürün arama ve filtreleme
- Fiyat karşılaştırması
- Stok kontrolü
- Kategori bazlı öneriler

**Özellikler**:
```python
# Ürün arama
await client.search_products("laptop", "electronics", 5)

# Fiyat karşılaştırması
await client.compare_prices("laptop")

# Stok kontrolü
await client.check_stock("product_id")

# Kategori önerileri
await client.get_recommendations("laptop", 15000)
```

**Desteklenen Platformlar**:
- **Trendyol**: Türkiye'nin en büyük e-ticaret sitesi
- **Hepsiburada**: Güvenilir alışveriş platformu

**Mock Veri Sistemi**:
- Gerçekçi ürün verileri
- Fiyat, rating, stok bilgileri
- Platform karşılaştırması
- Test edilebilir yapı

## ⚙️ Konfigürasyon (`app/config/`)

### **settings.py**
**İşlev**: Uygulama ayarları
- Environment variables
- API key'ler
- Database konfigürasyonu
- Logging ayarları

**Gerekli Environment Variables**:
```env
GEMINI_API_KEY=your_gemini_api_key
SHOPIFY_API_KEY=your_shopify_api_key
STRIPE_SECRET_KEY=your_stripe_secret_key
```

## 🛠️ Yardımcı Araçlar (`app/utils/`)

### **helpers.py**
**İşlev**: Genel yardımcı fonksiyonlar
- Veri formatlama
- Validation fonksiyonları
- Utility methods

### **logger.py**
**İşlev**: Logging sistemi
- Structured logging
- Log levels
- Error tracking

## 🧪 Test Sistemi (`tests/`)

### **test_nodes/**
**İşlev**: LangGraph node testleri
- Her node için unit testler
- Integration testleri
- Mock data ile testler

### **test_services/**
**İşlev**: Service testleri
- AI service testleri
- E-ticaret entegrasyon testleri

## 🔄 Veri Akışı

### **1. Kullanıcı Girişi**
```
POST /api/v1/ai/generate-mindmap
{
    "user_input": "Adana'da üniversite kazandım"
}
```

### **2. Workflow Execution**
```
EntryNode → MemoryNode → PromptNode → LLMNode → ToolNode → AgentNode → ProcessNode → OutputNode
```

### **3. AI Agent Çalışması**
```
ContextAnalysisAgent → MindMapAgent → ProductAgent → CustomerAgent
```

### **4. E-ticaret Entegrasyonu**
```
ProductAgent → EcommerceClient → E-ticaret API'leri
```

### **5. Sonuç Döndürme**
```
EcommerceClient → LangGraph → FastAPI → Flutter App
```

## 🚀 Çalıştırma

### **Geliştirme Ortamı**
```bash
pip install -r requirements.txt
python main.py
```

### **Docker ile**
```bash
docker-compose up -d
```

### **Test Çalıştırma**
```bash
pytest tests/
```

## 🔧 Özelleştirme

### **Yeni Agent Ekleme**
1. `BaseAgent`'dan inherit et
2. `AgentManager`'a ekle
3. Workflow'da kullan

### **Yeni Kategori Ekleme**
1. `MindMapAgent`'da `category_templates` güncelle
2. `ContextAnalysisAgent`'da `life_situations` güncelle

### **Yeni Şehir Ekleme**
1. `ContextAnalysisAgent`'da `city_data` güncelle
2. İklim ve özel ihtiyaçları tanımla

### **E-ticaret Platformu Ekleme**
1. `EcommerceClient`'da yeni platform ekle
2. API entegrasyonu yap
3. Mock verileri güncelle

## 🎨 Frontend Entegrasyonu

### **Zihin Haritası Görselleştirme**
- Flutter'da interaktif mind map
- Kategori tıklama
- Ürün detayları

### **Ürün Satın Alma**
- E-ticaret platformlarına yönlendirme
- Fiyat karşılaştırması
- Stok kontrolü
- Direkt satın alma

## 🔮 Gelecek Özellikler

- [ ] Gerçek e-ticaret API entegrasyonu
- [ ] Ödeme sistemi entegrasyonu
- [ ] Fiyat takip sistemi
- [ ] Bildirim sistemi
- [ ] Sesli komut desteği
- [ ] Görsel AI analizi
- [ ] Sosyal medya entegrasyonu
- [ ] Blockchain tabanlı ödeme
- [ ] AR/VR ürün deneyimi
- [ ] Çoklu dil desteği

## 📝 Notlar

- **LangChain**: AI model entegrasyonu için
- **LangGraph**: Workflow yönetimi için
- **AI Agent'lar**: Uzmanlaşmış görevler için
- **MCP**: Hafıza ve bağlam yönetimi için
- **EcommerceClient**: E-ticaret entegrasyonu için (n8n yerine)

Bu yapı sayesinde kullanıcılar **kişiselleştirilmiş zihin haritaları** oluşturabilir ve **direkt satın alma** yapabilir! 🎯🛒 