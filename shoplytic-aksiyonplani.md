# 🧠 Shoplytic — Bitirme Projesi Mükemmelleştirme Aksiyon Planı

> **Hedef:** Hackathon prototipini, jürinin "bu gerçekten çalışıyor" diyeceği,
> akademik olarak savunulabilir, teknik derinliği olan bir Bilgisayar Mühendisliği
> Mezuniyet Projesine dönüştürmek.

---

## 📐 Mimari Genel Bakış (Hedef Durum)

```
Flutter App
    │
    ▼
FastAPI (REST)
    │
    ▼
LangGraph Workflow
    ├── ContextAnalysisAgent  ──► Gemini API + Web Search
    ├── MindMapAgent          ──► Structured JSON Output
    ├── ProductAgent          ──► E-ticaret API / Scraper
    ├── LegalAgent            ──► ChromaDB RAG (6502 Kanun)
    └── CustomerAgent         ──► Segmentasyon + Kişiselleştirme
    │
    ▼
PostgreSQL (Persistent State)
    │
    ▼
Flutter UI (Interactive Mind Map + Hukuki Modül)
```

---

## ✅ FAZ 1 — Altyapı Temizliği (Önce Bunlar)

### 1.1 Hardcoded Verileri Tamamen Sil

**Dosya:** `shoplytic_backend/agents/context_analysis_agent.py`

Şu an bu kod var:
```python
city_data = {
    "adana": {"climate": "subtropical", "winter_temp": "5-15°C", ...}
}
life_situations = {
    "university_student": {"needs": ["laptop", "çanta"], ...}
}
```

**Yapılacak:** Bu sözlükleri tamamen sil. Yerine:

```python
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.3)

CONTEXT_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """Sen bir yaşam durumu analiz uzmanısın.
    Kullanıcının verdiği metni analiz et ve aşağıdaki JSON formatında dön:
    {{
      "location": {{"city": "", "climate": "", "season_now": ""}},
      "life_situation": {{"type": "", "priorities": [], "budget_level": ""}},
      "immediate_needs": [],
      "context_tags": []
    }}
    Sadece JSON döndür, başka hiçbir şey yazma."""),
    ("human", "{user_input}")
])

async def analyze_context(user_input: str) -> dict:
    chain = CONTEXT_PROMPT | llm
    response = await chain.ainvoke({"user_input": user_input})
    return json.loads(response.content)
```

Bu değişiklik: "Isparta'da yeni evlendim" de çalışır, "Dubai'de iş buldum" da.

---

### 1.2 MindMapAgent — Structured Output ile Yeniden Yaz

**Dosya:** `shoplytic_backend/agents/mindmap_agent.py`

```python
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from typing import List

class MindMapCategory(BaseModel):
    name: str = Field(description="Kategori adı")
    emoji: str = Field(description="Kategoriyi temsil eden emoji")
    items: List[str] = Field(description="Bu kategorideki ihtiyaç listesi")
    priority: str = Field(description="high / medium / low")
    estimated_budget: str = Field(description="Tahmini bütçe aralığı TL")

class MindMapOutput(BaseModel):
    central_topic: str
    user_summary: str = Field(description="Kullanıcının durumunun 1 cümlelik özeti")
    main_categories: List[MindMapCategory]
    total_estimated_budget: str

MINDMAP_PROMPT = """
Kullanıcı bağlamı: {context}

Bu bağlama göre kişiselleştirilmiş bir alışveriş zihin haritası oluştur.
Kategoriler gerçekçi, önceliklendirilmiş ve bütçeye duyarlı olsun.
Türkiye e-ticaret fiyatlarını kullan.
"""
```

**Önemli:** `JsonOutputParser` kullan. Bu sayede LLM çıktısı direk Flutter'a
parse edilebilir JSON olarak gider, hiç string manipulation gerekmez.

---

### 1.3 LangGraph State — Düzgün Tanımla

**Dosya:** `shoplytic_backend/graph/state.py`

```python
from typing import TypedDict, Optional, List, Annotated
from langgraph.graph import add_messages

class ShopLyticState(TypedDict):
    # Input
    user_input: str
    thread_id: str
    
    # Agent Outputs
    context_analysis: Optional[dict]
    mind_map: Optional[dict]
    product_recommendations: Optional[dict]
    legal_analysis: Optional[dict]
    
    # Conversation
    messages: Annotated[list, add_messages]
    
    # Meta
    current_step: str
    error: Optional[str]
```

Bu state tanımı tezde "sistem mimarisi" bölümünde doğrudan gösterilebilir.

---

## ✅ FAZ 2 — Canlı Ürün Verisi

### 2.1 Strateji: Scraping Yerine Akıllı Mock

Gerçek scraping 3 günde kırılır. Bunun yerine **"Dinamik Mock"** yap:
LLM'in ürettiği kategorilere göre gerçekçi ürün verisi dönsün.

**Dosya:** `shoplytic_backend/clients/ecommerce_client.py`

```python
PRODUCT_GENERATION_PROMPT = """
Kategori: {category}
Bütçe: {budget} TL
Şehir: {city}

Trendyol ve Hepsiburada'da gerçekten satılan, gerçekçi fiyatlı
3 ürün önerisi oluştur. JSON formatında:
[
  {{
    "name": "Ürün Adı",
    "brand": "Marka",
    "price": 0000,
    "platform": "Trendyol",
    "rating": 4.5,
    "review_count": 1250,
    "url": "https://trendyol.com/...",
    "why_recommended": "Bu kullanıcıya neden uygun olduğu"
  }}
]
Fiyatlar Türkiye piyasasıyla tutarlı olsun.
"""
```

**Neden bu kabul edilebilir akademik olarak:**
Tezde "Proof of Concept" olarak sun. Gerçek API entegrasyonu
"gelecek çalışmalar" bölümüne yaz. Jürinin asıl baktığı şey
mimari ve agent tasarımı, scraping değil.

### 2.2 ProductAgent — Scoring Fonksiyonu Ekle

Bu fonksiyon tezin "metodoloji" bölümü için kritik:

```python
def score_product(product: dict, user_context: dict) -> float:
    """
    Ürünü kullanıcı bağlamına göre puanla.
    
    Faktörler:
    - Fiyat-bütçe uyumu      : %30
    - Kullanıcı rating'i     : %25  
    - Yorum sayısı (güven)   : %20
    - İklim/durum uygunluğu  : %25
    """
    budget_score = calculate_budget_fit(product["price"], user_context["budget"])
    rating_score = product["rating"] / 5.0
    trust_score = min(product["review_count"] / 1000, 1.0)
    relevance_score = calculate_relevance(product, user_context)
    
    weights = [0.30, 0.25, 0.20, 0.25]
    scores = [budget_score, rating_score, trust_score, relevance_score]
    
    return sum(w * s for w, s in zip(weights, scores))
```

Bu scoring fonksiyonu tezde matematiksel formül olarak göster:

```
S(p) = 0.30·B(p) + 0.25·R(p) + 0.20·T(p) + 0.25·V(p)
```

---

## ✅ FAZ 3 — Tüketici Hakları Modülü (Akademik Core)

Bu modül seni diğer bitirme projelerinden ayırır. Mutlaka yap.

### 3.1 LegalRAG Kurulumu

```bash
pip install chromadb sentence-transformers pypdf
```

**Kanun metnini hazırla:**
1. https://www.mevzuat.gov.tr adresinden 6502 Sayılı Kanun'u PDF olarak indir
2. Aşağıdaki script ile ChromaDB'ye göm:

```python
# scripts/build_legal_db.py
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

def build_legal_database():
    loader = PyPDFLoader("data/6502_tuketici_kanunu.pdf")
    pages = loader.load()
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["Madde", "\n\n", "\n"]
    )
    chunks = splitter.split_documents(pages)
    
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )
    
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory="./chroma_legal_db"
    )
    vectorstore.persist()
    print(f"✅ {len(chunks)} chunk veritabanına eklendi.")

if __name__ == "__main__":
    build_legal_database()
```

### 3.2 LegalAgent

```python
class LegalAgent:
    def __init__(self):
        self.vectorstore = Chroma(
            persist_directory="./chroma_legal_db",
            embedding_function=HuggingFaceEmbeddings(...)
        )
        self.llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
    
    async def analyze_complaint(self, complaint: str) -> dict:
        # İlgili kanun maddelerini bul
        relevant_laws = self.vectorstore.similarity_search(complaint, k=3)
        
        # LLM ile şikayet + kanun eşleştir
        prompt = f"""
        Kullanıcı Şikayeti: {complaint}
        
        İlgili Kanun Maddeleri:
        {chr(10).join([doc.page_content for doc in relevant_laws])}
        
        Aşağıdaki bilgileri JSON formatında ver:
        1. Hangi kanun maddesi ihlal edilmiş
        2. Kullanıcının hakları neler
        3. Başvurulacak kurumlar
        4. Tavsiye edilen aksiyon adımları
        """
        
        response = await self.llm.ainvoke(prompt)
        return parse_legal_response(response.content)
    
    async def generate_petition(self, complaint_data: dict) -> str:
        """Resmi şikayet dilekçesi oluştur"""
        petition_prompt = f"""
        Aşağıdaki bilgilerle Tüketici Hakem Heyeti'ne resmi dilekçe yaz:
        
        Şikayet: {complaint_data['complaint']}
        İhlal edilen madde: {complaint_data['violated_law']}
        Talep: {complaint_data['demand']}
        
        Dilekçe resmi Türkçe hukuk diliyle yazılmalı,
        kanuni dayanakları içermeli ve profesyonel olmalıdır.
        """
        response = await self.llm.ainvoke(petition_prompt)
        return response.content
```

---

## ✅ FAZ 4 — Kalıcı Hafıza

### 4.1 SQLite ile Başla (PostgreSQL'e geçiş opsiyonel)

```python
# graph/checkpointer.py
from langgraph.checkpoint.sqlite import SqliteSaver

def get_checkpointer():
    return SqliteSaver.from_conn_string("shoplytic_memory.db")

# Workflow'da kullan:
workflow = StateGraph(ShopLyticState)
# ... node'ları ekle ...
app = workflow.compile(checkpointer=get_checkpointer())

# Her kullanıcıya unique thread:
config = {"configurable": {"thread_id": f"user_{user_id}"}}
result = await app.ainvoke(state, config=config)
```

**Demo'daki değeri:** Kullanıcı aynı konuşmaya geri döndüğünde
sistem önceki bağlamı hatırlıyor. Jüriye bunu mutlaka göster.

---

## ✅ FAZ 5 — Flutter UI

### 5.1 İnteraktif Mind Map

```dart
// pubspec.yaml'a ekle:
// graphview: ^1.2.0

import 'package:graphview/GraphView.dart';

class MindMapWidget extends StatefulWidget {
  final Map<String, dynamic> mindMapData;
  
  @override
  Widget build(BuildContext context) {
    final Graph graph = Graph();
    
    // Merkez node
    final centerNode = Node.Id('center');
    
    // Kategori node'ları
    for (var category in mindMapData['main_categories']) {
      final categoryNode = Node.Id(category['name']);
      graph.addEdge(centerNode, categoryNode);
      
      // Item node'ları
      for (var item in category['items']) {
        final itemNode = Node.Id(item);
        graph.addEdge(categoryNode, itemNode);
      }
    }
    
    return InteractiveViewer(
      child: GraphView(
        graph: graph,
        algorithm: BuchheimWalkerAlgorithm(
          BuchheimWalkerConfiguration()
            ..siblingSeparation = 50
            ..levelSeparation = 80,
        ),
        builder: (Node node) => _buildNode(node),
      ),
    );
  }
}
```

### 5.2 Tüketici Hakları Ekranı

```dart
class LegalSupportScreen extends StatefulWidget {
  // 3 tab:
  // 1. Şikayet Gir → LegalAgent'a gönder
  // 2. Kanun Maddeleri → RAG sonuçları göster  
  // 3. Dilekçe Önizle → PDF indir
}
```

---

## ✅ FAZ 6 — Akademik Değerlendirme (Tez İçin)

### 6.1 Ölçmeni Gereken Metrikler

Tezin "Sonuçlar" bölümü için şu tabloyu doldur:

| Metrik | Değer | Nasıl Ölçersin |
|--------|-------|----------------|
| Uçtan uca yanıt süresi | ___ ms | `time.perf_counter()` |
| Zihin haritası doğruluğu | ___ % | 20 farklı girdi test et |
| LLM token maliyeti/istek | ___ token | LangChain callbacks |
| RAG precision@3 | ___ % | 10 hukuki soru test et |
| Flutter render süresi | ___ ms | Flutter DevTools |

### 6.2 Benchmark Kodu

```python
# tests/benchmark.py
import asyncio, time, json

TEST_INPUTS = [
    "Ankara'da yeni iş başlıyorum, ofis kıyafetleri lazım",
    "İstanbul'da bebek bekleyen bir çift için hazırlık",
    "Antalya'da emekli oldum, aktif yaşam istiyorum",
    "Erzurum'da üniversite okuyan kız öğrenci",
    "İzmir'de uzaktan çalışıyorum, ev ofisi kuruyorum"
]

async def run_benchmark():
    results = []
    for test_input in TEST_INPUTS:
        start = time.perf_counter()
        result = await workflow.ainvoke({"user_input": test_input})
        elapsed = (time.perf_counter() - start) * 1000
        
        results.append({
            "input": test_input,
            "latency_ms": round(elapsed, 2),
            "categories_count": len(result["mind_map"]["main_categories"]),
            "tokens_used": get_token_count()
        })
    
    # Teze koyacağın tablo
    print(json.dumps(results, ensure_ascii=False, indent=2))
```

### 6.3 Tez Yapısı Önerisi

```
1. Giriş
   - Problem tanımı: E-ticarette kişiselleştirme eksikliği
   - Motivasyon: Tüketici hakları korumasızlığı
   - Katkılar (bullet list — jüri buraya bakar)

2. İlgili Çalışmalar
   - Multi-agent sistemler (AutoGPT, BabyAGI karşılaştırması)
   - RAG sistemleri ve hukuki uygulamaları
   - LangGraph vs diğer agent frameworkler

3. Sistem Mimarisi
   - Agent tasarım desenleri
   - LangGraph state machine diyagramı
   - Veri akışı diyagramı

4. Uygulama
   - Her agent detaylı anlatım + pseudo-kod
   - Scoring fonksiyonu matematiksel formül
   - RAG pipeline detayı

5. Deneysel Değerlendirme
   - Benchmark tabloları (6.1'deki tablo)
   - Model karşılaştırması (Gemini vs GPT-4o-mini)
   - Kullanıcı senaryoları

6. Sonuç ve Gelecek Çalışmalar
   - Gerçek scraping entegrasyonu
   - OCR + otomatik dilekçe
   - Çok dilli destek
```

---

## 🔥 Öncelik Sırası (Uyumadan Önce Ne Yaparsın)

```
SAAT 0-4   → FAZ 1 (Hardcoded kaldır, LLM bağla)
SAAT 4-8   → FAZ 3 (LegalRAG kur — seni ayıran bu)
SAAT 8-12  → FAZ 2 (Dinamik mock + scoring fonksiyonu)
SAAT 12-16 → FAZ 4 (SQLite checkpointer)
SAAT 16-22 → FAZ 5 (Flutter mind map + legal ekran)
SAAT 22-26 → FAZ 6 (Benchmark çalıştır, sonuçları kaydet)
SAAT 26-30 → Demo akışını 3 farklı senaryoyla prova et
```

---

## ⚡ Kritik Hatırlatmalar

- **Gemini API kotasını** kontrol et, rate limit'e takılma
- Tüm async fonksiyonlarda **try/except** kullan — demo sırasında hata çıkmasın
- Flutter'da **loading state** göster — LLM yanıtı 3-5 saniye sürer, boş ekran kötü görünür
- Jüriye mutlaka **2 farklı şehir** dene: biri büyük şehir, biri küçük şehir (Isparta gibi)
- LegalRAG için kanunu bulamazsan YARGITAY kararları da alternatif kaynak

---

*Son güncelleme: Shoplytic v2.0 — BTK Akademi Hackathon → Mezuniyet Projesi*
