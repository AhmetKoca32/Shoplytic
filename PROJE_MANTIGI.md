# Shoplytic — Proje Mantığı

## 🎯 Nedir?

Shoplytic, kullanıcının hayatındaki bir değişikliği (ör: "Üniversiteye başlıyorum") alıp AI ile analiz ederek **kişiselleştirilmiş alışveriş deneyimi** sunan bir mobil uygulamadır.

---

## 🔄 Ana Akış

```
Splash → Onboard(5 sayfa) → Home
                                 │
                  ┌──────────────┼──────────────┐
                  ▼              ▼              ▼
             Ana Sayfa      Zihin Haritası    Sohbet       Profil
             (prompt)       (görsel+ürünler)  (AI asistan)  (ayarlar)
```

## 🧠 Temel Konsept

1. **Kullanıcı bir prompt girer** — "Üniversiteye başlıyorum, yurda eşya alacağım"
2. **AI zihin haritası oluşturur** — Kategorilere ayrılmış görsel bir harita (Akademik Malzemeler, Kırtasiye, Teknoloji vb.)
3. **Her kategori içinde ürünler** — Trendyol, Hepsiburada gibi platformlardan ürünler, fiyat karşılaştırması, stok durumu
4. **AI Sohbet** — Kullanıcı soru sorar, AI alışveriş konusunda yardımcı olur

---

## 🏗 Mimari

```
lib/
├── main.dart                  → Uygulama giriş noktası
├── app.dart                   → MaterialApp, Provider, routing
├── theme/                     → Tasarım sistemi (renkler, glass efektleri)
├── services/
│   └── api_service.dart       → Backend API iletişimi (Dio) + Mock veri fallback
├── providers/
│   ├── mind_map_provider.dart  → Zihin haritası state yönetimi
│   ├── chat_provider.dart      → Sohbet state yönetimi
│   ├── auth_provider.dart      → (Kullanılmıyor)
│   ├── home_provider.dart      → (Kullanılmıyor)
│   └── onboard_provider.dart   → (Kullanılmıyor)
└── views/
    ├── auth/
    │   └── splash_screen.dart  → Splash (3sn sonra /home'a yönlenir)
    ├── onboard/
    │   └── onboard_screen.dart → 5 sayfalık onboarding
    └── home/
        ├── home_screen.dart    → Ana ekran (prompt + floating navbar)
        ├── chat/
        │   └── chat_screen.dart → AI sohbet ekranı
        ├── mind_map/
        │   └── mind_map_screen.dart → Zihin haritası (görsel + ürün listesi)
        └── profile/
            └── profile_screen.dart → Profil (settings/history/favorites/help inline)
```

## 📡 Backend API (FastAPI — localhost:8000/api/v1)

| Endpoint | HTTP | Amaç |
|---|---|---|
| `/health` | GET | Sağlık kontrolü |
| `/test` | GET | Bağlantı testi |
| `/system/status` | GET | Sistem durumu |
| `/ai/generate-mindmap` | POST | Zihin haritası oluşturma |
| `/ai/chat` | POST | AI sohbet |
| `/workflow/execute` | POST | Workflow çalıştırma |
| `/ecommerce/search` | GET | Ürün arama |
| `/ecommerce/compare/{name}` | GET | Fiyat karşılaştırma |
| `/ecommerce/stock/{id}` | GET | Stok kontrolü |
| `/ecommerce/recommendations/{cat}` | GET | Ürün önerileri |

> Backend çalışmıyorsa, uygulama **mock veri** ile devam eder.

## 🧩 State Yönetimi

- **Provider** (ChangeNotifier) kullanılır
- Sadece `MindMapProvider` ve `ChatProvider` aktif olarak kullanılıyor
- `MultiProvider` ile app.dart'ta enjekte edilir

## 🎨 Tasarım

- **Koyu tema** (siyah-mor gradient arka plan)
- **Liquid glass navbar** — BackdropFilter blur ile havada uçar
- Glass kartlar, gradient butonlar, smooth animasyonlar
- Accent renkler: Pembe (`#FF6B9D`) + Mor (`#7C4DFF`)

## 📦 Bağımlılıklar

| Paket | Kullanım |
|---|---|
| `provider` | State management |
| `dio` | HTTP istekleri |
| `google_fonts` | Poppins font (zihin haritası) |
| `cached_network_image` | Resim önbellekleme |
| `shared_preferences` | (Hazır, kullanılmıyor) |
| `flutter_svg` | (Hazır, kullanılmıyor) |

---

## 🔜 Yapılacaklar

- [ ] Auth flow tamamlama (şu an login yok, direkt home'a gidiyor)
- [ ] Kullanılmayan provider'ları temizleme (`AuthProvider`, `HomeProvider`, `OnboardProvider`)
- [ ] Kullanılmayan paketleri kaldırma (`http`, `flutter_svg`, `cupertino_icons`)
- [ ] Backend'e gerçek bağlantı
- [ ] Veri kalıcılığı (SharedPreferences)
