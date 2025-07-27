# 🧠 AI-Assisted Smart E-commerce Workflow

Bu proje, yapay zeka destekli otomasyon senaryolarıyla zenginleştirilmiş, uçtan uca entegre bir e-ticaret akış sistemidir. LangGraph tabanlı düğüm mimarisi, n8n otomasyonları ve özel API bağlantıları ile sürdürülebilir, esnek ve akıllı bir alışveriş deneyimi sunar.

---

## 🚀 Özellikler

- ✅ LangGraph mimarisiyle kurgulanmış node tabanlı AI iş akışı  
- 🔌 n8n ile senkronize e-ticaret API entegrasyonları (Shopify, WooCommerce, vb.)  
- 📦 Ürün sınıflandırma, müşteri segmentasyonu ve öneri sistemleri için yapay zeka modelleri  
- 🧠 Prompt Engineering ile özelleştirilmiş LLM yönlendirmeleri  
- 🧪 Her modül için senaryo tabanlı testler  
- 🧱 MCP tabanlı hafıza yönetimi  
- 📊 Dashboard üzerinden izlenebilir akış verisi ve işlem günlükleri  

---

## 🧱 Mimari

Proje LangGraph ile oluşturulmuş bir düğüm (node) mimarisine sahiptir:

- **Giriş Node’u** → Kullanıcı girdisini veya sistem tetikleyicisini alır  
- **Prompt Node** → Dinamik olarak AI'a gönderilecek prompt'u üretir  
- **LLM Node** → LLM çağrısı yapılır (GPT-4 / Claude / Gemini destekli)  
- **API Call Node** → E-ticaret sistemlerine veri gönderimi veya çekimi yapılır  
- **Veri İşleme Node’u** → Gelen veriler analiz edilir, dönüştürülür  
- **Çıkış Node’u** → Sonuçlar dashboard’a veya kullanıcıya iletilir  

### Hafıza Yönetimi (MCP)

Proje içerisinde çok adımlı konuşma ve işlem geçmişi yönetimi için `MessageContextPersistence (MCP)` sistemi kullanılmıştır. Böylece AI kararlarında bağlam korunur.

---

## 🧠 Prompt Engineering

Sistemde kullanılan başlıca prompt şablonları:

```txt
📌 Kullanıcıdan gelen ürünü, kategoriye göre sınıflandır:

"Ürün açıklaması: {{description}} 
Hangi kategoriye ait olduğunu tahmin et (örnek: elektronik, kozmetik, moda, vb.):"
````

```txt
📌 Sepete ürün eklendiğinde, benzer ürün öner:

"Sepet içeriği: {{cart_items}} 
Bunlara benzer hangi ürünler önerilir? 3 örnekle açıkla."
```

---

## 🔌 API’ler

Proje, n8n üzerinden aşağıdaki sistemlerle senkronize çalışır:

* Shopify / WooCommerce / Stripe gibi e-ticaret altyapıları
* Postman mock API'ler üzerinden test ortamı desteği
* Zapier entegrasyonlarına açık yapı

### n8n Senaryo Örneği

* Webhook ile sepet güncellemesi tetiklenir
* LangGraph üzerinden AI çalıştırılır
* AI çıktısı, önerilen ürünlerle beraber veritabanına yazılır
* Mail API üzerinden kullanıcıya öneri gönderilir

---

## 🧪 Testler

Her bir modül için test senaryoları tanımlanmıştır:

| Modül                 | Test Edilen Nokta                    | Sonuç |
| --------------------- | ------------------------------------ | ----- |
| Prompt Node           | Prompt içeriği dinamik değişiyor mu? | ✅     |
| API Call Node         | API başarılı yanıt döndürüyor mu?    | ✅     |
| LLM Node              | Model doğru çıktılar üretiyor mu?    | ✅     |
| Hafıza Yönetimi (MCP) | Konu bağlamı korunuyor mu?           | ✅     |

---

## ⚙️ Kurulum ve Çalıştırma

1. **LangGraph kurulumu**

   ```bash
   pip install langgraph
   ```

2. **n8n kurulumu (Docker ile önerilir)**

   ```bash
   docker-compose up -d
   ```

3. **Config ayarları**

   `.env` dosyasına OpenAI key, API endpoint'leri ve diğer değişkenler eklenir.

---

## 📌 Katkıda Bulun

Proje açık kaynaklı değildir. Ancak teknik destek veya tanıtım amacıyla sunumlar hazırlanabilir.

---

## 👤 Geliştirici

**Ahmet Koca**
Süleyman Demirel Üniversitesi - Bilgisayar Mühendisliği
📫 [kocaahmetkoca32@gmail.com](mailto:kocaahmetkoca32@gmail.com)
🔗 [LinkedIn](https://www.linkedin.com/in/ahmetkocaa)
