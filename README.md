# 🧠 AI-Assisted Smart E-commerce Workflow (Shoplytic)

## 📋 Proje Özeti

Shoplytic, kullanıcıların hayatlarındaki yeni durumları paylaştığı ve AI agent'ların bu duruma göre kişiselleştirilmiş zihin haritası oluşturduğu akıllı e-ticaret platformudur.

### 🎯 Ana Senaryo
**"Adana'da yeni bir üniversite kazandım, kışın çok soğuk oluyor"** gibi bir kullanıcı girişi ile başlayan süreç:

1. **Kullanıcı durumu analiz edilir**
2. **Zihin haritası oluşturulur**
3. **Kategorilere göre ürünler önerilir**
4. **E-ticaret platformlarından ürünler sunulur**
5. **Fiyat karşılaştırması ve satın alma**

## 🏗️ Mimari Yapı

### Backend Teknolojileri
- **FastAPI**: REST API framework
- **LangGraph**: AI workflow yönetimi
- **LangChain**: LLM entegrasyonu ve araçlar
- **AI Agent'lar**: Uzmanlaşmış AI sistemleri
- **MCP (MessageContextPersistence)**: Hafıza yönetimi
- **E-ticaret Client**: Direkt API entegrasyonu (İlerleyen süreçte n8n kullanılacak)

### Frontend Teknolojileri
- **Flutter**: Cross-platform mobil uygulama
- **Dart**: Programlama dili

## 🤖 AI Agent Sistemi

### 1. ContextAnalysisAgent
**Görevi**: Kullanıcı durumunu analiz etmek
- Lokasyon analizi (şehir, iklim)
- Yaşam durumu tespiti (öğrenci, iş, ev)
- Mevsimsel ihtiyaç analizi
- Bütçe ve öncelik belirleme

**Özellikler**:
```python
# Şehir veritabanı
city_data = {
    "adana": {
        "climate": "subtropical",
        "winter_temp": "5-15°C",
        "special_needs": ["nemlendirici", "klima", "hafif mont"]
    }
}

# Yaşam durumu şablonları
life_situations = {
    "university_student": {
        "needs": ["laptop", "çanta", "defter"],
        "budget": "limited",
        "priorities": ["pratik", "uygun fiyat"]
    }
}
```

### 2. MindMapAgent
**Görevi**: Zihin haritası oluşturmak
- Kategori organizasyonu
- Öncelik sıralaması
- Görsel yapı oluşturma
- Dinamik güncelleme

**Örnek Çıktı**:
```json
{
    "central_topic": "Adana Üniversite Hazırlığı",
    "main_categories": [
        {
            "name": "Akademik Malzemeler",
            "items": ["laptop", "çanta", "defter"],
            "priority": "high"
        },
        {
            "name": "Kış Hazırlığı",
            "items": ["mont", "bot", "atkı"],
            "priority": "high"
        }
    ]
}
```

### 3. ProductAgent
**Görevi**: Ürün analizi ve önerileri
- Ürün kategorilendirme
- Özellik çıkarma
- Rakip analizi
- Trend analizi

### 4. CustomerAgent
**Görevi**: Müşteri segmentasyonu
- Müşteri davranış analizi
- Churn tahmini
- Lifetime value hesaplama
- Kişiselleştirilmiş öneriler

## 🔄 Workflow Sistemi

### LangGraph Workflow
```
Entry → Memory → Prompt → LLM → Tool → Agent → Process → Output
```

**Node'lar**:
1. **EntryNode**: Giriş verilerini alır
2. **MemoryNode**: MCP ile hafıza yönetimi
3. **PromptNode**: Dinamik prompt oluşturur
4. **LLMNode**: LangChain ile AI çağrıları
5. **ToolNode**: LangChain araçları (web search, Wikipedia)
6. **AgentNode**: AI agent'ları yönetir
7. **ProcessNode**: Veri işleme
8. **OutputNode**: Sonuç formatlama

### Mind Map Generation Workflow
```
1. ContextAnalysisAgent → Kullanıcı durumu analizi
2. ContextAnalysisAgent → İhtiyaç çıkarma
3. MindMapAgent → Zihin haritası oluşturma
4. ProductAgent → Her kategori için ürün önerileri
5. EcommerceClient → E-ticaret entegrasyonu
```

## 🛠️ API Endpoints

### AI Servisleri
```http
POST /api/v1/ai/generate-mindmap  # Zihin haritası oluşturma
POST /api/v1/workflow/execute     # Genel workflow execution
```

### E-ticaret Entegrasyonu
```http
GET /api/v1/ecommerce/search?query=laptop&category=electronics
GET /api/v1/ecommerce/recommendations/laptop?budget=15000
GET /api/v1/ecommerce/compare/laptop
GET /api/v1/ecommerce/stock/1
```

### Sistem Durumu
```http
GET /api/v1/system/status
```

## 📱 Kullanım Senaryosu

### 1. Kullanıcı Girişi
```json
POST /api/v1/ai/generate-mindmap
{
    "user_input": "Adana'da yeni bir üniversite kazandım, kışın çok soğuk oluyor"
}
```

### 2. AI Agent'ların Çalışması

**ContextAnalysisAgent Analizi**:
- Lokasyon: Adana (subtropical iklim)
- Durum: Üniversite öğrencisi
- Mevsim: Kış (5-15°C)
- Özel ihtiyaçlar: Nemlendirici, hafif mont

**MindMapAgent Çıktısı**:
- Merkez konu: "Adana Üniversite Hazırlığı"
- Kategoriler: Akademik, Kış Hazırlığı, Adana Özel, Ev Eşyaları

**ProductAgent Önerileri**:
- Her kategori için 3 ürün önerisi
- Fiyat-performans analizi
- Adana iklimine uygunluk

### 3. E-ticaret Entegrasyonu
```http
GET /api/v1/ecommerce/recommendations/laptop?budget=15000
```

**Yanıt**:
```json
{
    "success": true,
    "recommendations": [
        {
            "id": "1",
            "name": "Lenovo ThinkPad E15",
            "price": 15999.99,
            "platform": "Trendyol",
            "rating": 4.5,
            "stock": true,
            "url": "https://trendyol.com/laptop-1"
        }
    ]
}
```

### 4. Fiyat Karşılaştırması
```http
GET /api/v1/ecommerce/compare/laptop
```

### 5. Sonuç
```json
{
    "success": true,
    "mind_map": {
        "central_topic": "Adana Üniversite Hazırlığı",
        "main_categories": [
            {
                "name": "Akademik Malzemeler",
                "items": ["laptop", "çanta", "defter"],
                "products": [
                    {
                        "name": "Lenovo ThinkPad E15",
                        "price": 15999.99,
                        "platform": "Trendyol",
                        "rating": 4.5
                    }
                ]
            }
        ]
    }
}
```

## 🛒 E-ticaret Entegrasyonu

### EcommerceClient Özellikleri
- **Ürün Arama**: Kategori ve query bazlı arama
- **Fiyat Karşılaştırması**: Çoklu platform karşılaştırması
- **Stok Kontrolü**: Gerçek zamanlı stok durumu
- **Kategori Önerileri**: Bütçe ve rating bazlı öneriler

### Desteklenen Platformlar
- **Trendyol**: Türkiye'nin en büyük e-ticaret sitesi
- **Hepsiburada**: Güvenilir alışveriş platformu

### Mock Veri Sistemi
- Gerçekçi ürün verileri
- Fiyat, rating, stok bilgileri
- Platform karşılaştırması
- Test edilebilir yapı

## 🚀 Kurulum ve Çalıştırma

### Backend Kurulumu
```bash
cd shoplytic_backend
pip install -r requirements.txt
python main.py
```

### Frontend Kurulumu
```bash
cd shoplytic_ui
flutter pub get
flutter run
```

### Gerekli Ortam Değişkenleri
```env
GEMINI_API_KEY=your_gemini_api_key
SHOPIFY_API_KEY=your_shopify_api_key
STRIPE_SECRET_KEY=your_stripe_secret_key
```

## 📊 Veri Akışı

### 1. Kullanıcı Girişi
```
Flutter App → FastAPI → LangGraph Workflow
```

### 2. AI İşleme
```
ContextAnalysisAgent → MindMapAgent → ProductAgent
```

### 3. E-ticaret Entegrasyonu
```
ProductAgent → EcommerceClient → E-ticaret API'leri
```

### 4. Sonuç Döndürme
```
EcommerceClient → LangGraph → FastAPI → Flutter App
```

## 🔧 Özelleştirme

### Yeni Agent Ekleme
1. `BaseAgent`'dan inherit et
2. `AgentManager`'a ekle
3. Workflow'da kullan

### Yeni Kategori Ekleme
1. `MindMapAgent`'da `category_templates` güncelle
2. `ContextAnalysisAgent`'da `life_situations` güncelle

### Yeni Şehir Ekleme
1. `ContextAnalysisAgent`'da `city_data` güncelle
2. İklim ve özel ihtiyaçları tanımla

### E-ticaret Platformu Ekleme
1. `EcommerceClient`'da yeni platform ekle
2. API entegrasyonu yap
3. Mock verileri güncelle

## 🎨 Frontend Entegrasyonu

### Zihin Haritası Görselleştirme
- Flutter'da interaktif mind map
- Kategori tıklama
- Ürün detayları

### Ürün Satın Alma
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

Bu yapı sayesinde kullanıcılar **kişiselleştirilmiş** ve **bağlama uygun** ürün önerileri alabilir ve **direkt satın alma** yapabilir! 🎯🛒
