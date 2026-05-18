# Shoplytic Mobil Uygulama Tipografi ve Font Kullanım Kılavuzu

Bu döküman, **Shoplytic** mobil uygulamasındaki (`shoplytic_ui`) görsel hiyerarşiyi, okunabilirliği ve teknik marka kimliğini korumak adına hangi fontun, hangi ekranda, hangi bileşen için ve nasıl bir tasarımla (punto/kalınlık) kullanılacağını detaylandıran mimari bir kılavuzdur.

---

## 📐 Küresel Font Rol Dağılımı ve Parametreleri

Uygulama genelinde görsel tutarsızlığı engellemek amacıyla fontlar kesin rollerle sınırlandırılmıştır:

| Font Ailesi | Tasarımdaki Rolü | Tercih Edilen Kalınlıklar (Weight) | Temel Amacı |
| --- | --- | --- | --- |
| **Montserrat** | Görsel Vitrin & Başlık | `w600` (Semi-Bold), `w700` (Bold) | Kullanıcıya modern yapay zekâ ürünü hissini ilk bakışta vermek. |
| **Inter** | Gövde Metni & İçerik | `w400` (Regular), `w500` (Medium) | Chat akışları ve ürün kartlarında mobil okunabilirlik konforu sağlamak. |
| **JetBrains Mono** | Teknik Veri & Mevzuat | `w400` (Regular), `w500` (Medium) | API çıktıları, OCR sonuçları ve kanun maddelerinde mühendislik kimliğini öne çıkarmak. |

---

## 📱 Ekran ve Bileşen Bazlı Detaylı Kullanım Planı

### 1. Montserrat — Başlıklar ve Aksiyon Elemanları (Vitrindeki Rolü)

Montserrat fontu yalnızca kullanıcının odaklanması gereken üst düzey hiyerarşik alanlarda ve yönlendirmelerde kullanılır. Paragraf metinlerinde kullanımı kesinlikle yasaktır.

* **Uygulama Logosu ve Karşılama Ekranı (Splash/Onboarding):**
* 
**Bileşen:** Ana marka adı ve slogan metni.


* **Tasarım Parametreleri:** `32sp`, `FontWeight.w700` (Bold).
* 
**Nasıl Kullanılacak:** Uygulama ilk açıldığında "SHOPLYTIC" başlığının jilet gibi keskin ve kurumsal durması için merkezde konumlandırılacak.




* **Modül ve Sayfa Başlıkları (AppBar):**
* **Bileşen:** Sayfaların en üstünde yer alan navigasyon metinleri.
* **Tasarım Parametreleri:** `20sp`, `FontWeight.w700` (Bold).
* 
**Nasıl Kullanılacak:** "Zihin Haritası" , "Önerilen Ürünler" ve "Tüketici Hakları"  ekranlarının üst barlarında sabit başlık olarak atanacak.




* **Ana Aksiyon Butonları (Call to Action - CTA):**
* **Bileşen:** Form onaylama, tetikleme ve satın alma buton metinleri.
* **Tasarım Parametreleri:** `16sp`, `FontWeight.w600` (Semi-Bold).
* 
**Nasıl Kullanılacak:** "Zihin Haritası Oluştur" , "Şikayet Dilekçesi Hazırla" ve "Satın Alma İşlemini Tamamla"  gibi kritik butonların merkez metinlerinde tercih edilecek.





---

### 2. Inter — İçerik, Akış ve Kullanıcı Deneyimi (Okunabilirlik Rolü)

Inter fontu, uygulamanın veri yoğunluğunun en yüksek olduğu ve kullanıcının uzun süreler boyunca okuma yapacağı tüm dinamik arayüz elemanlarında varsayılan olarak kullanılır.

* **Yapay Zekâ Sohbet (Chat) Akışı ve Prompt Girişleri:**
* 
**Bileşen:** Kullanıcı girdi metinleri ve yapay zekâ ajanlarının ürettiği doğal dil yanıtları.


* **Tasarım Parametreleri:** `15sp`, `FontWeight.w400` (Regular).
* 
**Nasıl Kullanılacak:** Kullanıcının yazdığı "Adana'da yeni bir üniversite kazandım..." metni ile `ContextAnalysisAgent` tarafından üretilen analiz paragraflarının  sohbet balonları içinde gözü yormadan, doğal bir şekilde akması için kullanılacak.




* **Dinamik Zihin Haritası (Mind Map) Düğümleri (Nodes):**
* 
**Bileşen:** Grafik veya ağaç yapısı üzerinde dallanan kategori kutucuklarının metinleri.


* **Tasarım Parametreleri:** `14sp`, `FontWeight.w500` (Medium).
* 
**Nasıl Kullanılacak:** Haritanın merkezindeki "Adana Üniversite Hazırlığı" ana düğümü ile altındaki "Akademik Malzemeler" ve "Kış Hazırlığı"  gibi alt kırılımların kutu içi yazılarında net bir ayrım sunmak için tercih edilecek.




* **E-Ticaret Ürün Kartları Listesi:**
* 
**Bileşen:** Ürün adı, fiyatı, satıcı platformu ve kullanıcı değerlendirme puanları.


* **Tasarım Parametreleri:** Ürün adı için `14sp` / `w500` (Medium), fiyat bilgisi için `16sp` / `w600` (Semi-Bold).
* 
**Nasıl Kullanılacak:** "Lenovo ThinkPad E15" ürün ismi normal ağırlıkta tutulurken, "15999.99 TL" fiyat bilgisi ve "Trendyol"  platform etiketi kalınlaştırılarak kart hiyerarşisi Inter ile inşa edilecek.





---

### 3. JetBrains Mono — Teknik Veri, Loglar ve Hukuki Atıflar (Mühendislik Kimliği)

JetBrains Mono fontu, uygulamanın sıradan bir tasarım şablonundan sıyrılıp arkasında çalışan güçlü bir yazılım mimarisi ve yasal dayanak olduğunu jüriye kanıtlamak için kritik noktalarda izolasyon sağlar.

* **Sistem Durumu ve API Endpoint Göstergeleri:**
* 
**Bileşen:** Arka plan servislerinin durum dökümleri ve istek (request) logları.


* **Tasarım Parametreleri:** `12sp`, `FontWeight.w400` (Regular).
* 
**Nasıl Kullanılacak:** Geliştirici veya jüri için ekranda anlık gösterilebilecek `GET /api/v1/system/status` veya `POST /api/v1/ai/generate-mindmap`  gibi terminal benzeri log çıktılarında kod görünümü sunmak için kullanılacak.




* **Fatura OCR Analiz Sonuçları:**
* **Bileşen:** Görüntü işlemeden (PaddleOCR) dönen ham metin ve veri eşleşmeleri.
* **Tasarım Parametreleri:** `13sp`, `FontWeight.w500` (Medium).
* **Nasıl Kullanılacak:** Kullanıcının yüklediği faturadan çekilen vergi numarası, fatura tarihi ve ham metin bloklarının jüriye "bunu başarıyla parse ettik" mesajıyla ham veri formatında gösterilmesinde kullanılacak.


* **Hukuki Mevzuat Atıfları ve Kanun Maddeleri:**
* 
**Bileşen:** Tüketici Hakları Desteği altındaki kanuni dayanak referansları.


* **Tasarım Parametreleri:** `12sp`, `FontWeight.w400` (Regular / Italic).
* 
**Nasıl Kullanılacak:** Yapay zekanın hazırlayacağı otomatik şikayet dilekçesinin  dayandırıldığı yasal temelleri belirtirken, metin aralarındaki `6502 Sayılı Kanun` veya `Madde 48/A` gibi teknik hukuk terimlerini gövde metninden görsel olarak ayırmak amacıyla aralara serpiştirilecek.





---

## 🛑 Tasarım Kısıtları ve Uygulama Kuralları

* **Kural 1 (Hiyerarşi Kısıtı):** Bir ekran tasarlanırken başlık fontu (Montserrat) bittiği an gövde fontuna (Inter) geçiş keskin olmalıdır. Ara paragraflarda Montserrat'ın daha küçük puntoları kesinlikle denenmemelidir.
* **Kural 2 (Teknik Veri İzolasyonu):** Ekranda yer alan herhangi bir sayısal metrik (Örn: `200 OK`, `150ms`, `token: 412`) asla düz fontla yazılmamalı, doğrudan `JetBrains Mono` ile sarmalanmalıdır.
* **Kural 3 (Kalınlık Sınırı):** Kodlama esnasında fontların `w400`, `w500`, `w600` ve `w700` varyasyonları dışında kalan ekstrem kalınlıkları (Örn: `w100` veya `w900`) arayüz bütünlüğünü bozmamak adına projeye dahil edilmeyecektir.