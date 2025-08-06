from typing import Dict, Any, Optional, List
from app.agents.base_agent import BaseAgent
from app.utils.logger import get_logger

logger = get_logger(__name__)

class ChatAgent(BaseAgent):
    """AI Chat Agent - kullanıcı mesajlarını işler ve yanıt üretir"""
    
    def __init__(self):
        super().__init__(
            agent_id="chat_agent_001",
            agent_type="chat_assistant",
            llm_model="gemini-2.0-flash"
        )
        self.name = "chat_agent"
        self.description = "Kullanıcı mesajlarını anlar ve uygun yanıtlar üretir"
        
    def get_capabilities(self) -> List[str]:
        """Agent'ın yeteneklerini döndür"""
        return [
            "message_analysis",
            "response_generation", 
            "context_management",
            "sentiment_analysis",
            "intent_recognition",
            "conversation_history",
            "product_recommendations"
        ]
    
    async def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Ana görev işleme metodu"""
        return await self.process(task)
        
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Chat mesajını işle ve yanıt üret"""
        try:
            message = input_data.get("message", "")
            user_id = input_data.get("user_id")
            conversation_id = input_data.get("conversation_id")
            context = input_data.get("context", {})
            
            logger.info(f"Chat mesajı işleniyor: {message[:50]}...")
            
            # Basit ve etkili yanıt sistemi
            response = self._generate_simple_response(message, context)
            
            # Context güncelleme
            updated_context = self._update_simple_context(context, message, response)
            
            return {
                "output": {
                    "response": response,
                    "context": updated_context,
                    "conversation_id": conversation_id
                }
            }
            
        except Exception as e:
            logger.error(f"Chat işleme hatası: {str(e)}")
            return {
                "output": {
                    "response": "Üzgünüm, mesajınızı işlerken bir hata oluştu. Lütfen tekrar deneyin.",
                    "context": context,
                    "error": str(e)
                }
            }
    
    def _generate_simple_response(self, message: str, context: Dict[str, Any]) -> str:
        """Basit ve etkili yanıt üretimi"""
        print(f"🔍 _generate_simple_response çağrıldı: {message}")
        message_lower = message.lower()
        
        # Context'ten önceki mesajları kontrol et
        conversation_history = context.get('conversation_history', [])
        previous_messages = [msg.get('message', '').lower() for msg in conversation_history[-3:]]  # Son 3 mesaj
        print(f"🔍 Önceki mesajlar: {previous_messages}")
        
        # Monitör konuşması - mevcut mesajda veya önceki mesajlarda
        if ("monitör" in message_lower or "monitor" in message_lower or 
            any("monitör" in prev_msg or "monitor" in prev_msg for prev_msg in previous_messages)):
            print(f"🔍 Monitör konuşması tespit edildi")
            return self._handle_monitor_conversation(message, context)
        
        # Laptop konuşması - mevcut mesajda veya önceki mesajlarda
        elif ("laptop" in message_lower or "bilgisayar" in message_lower or
              any("laptop" in prev_msg or "bilgisayar" in prev_msg for prev_msg in previous_messages)):
            print(f"🔍 Laptop konuşması tespit edildi")
            return self._handle_laptop_conversation(message, context)
        
        # Telefon konuşması - mevcut mesajda veya önceki mesajlarda
        elif ("telefon" in message_lower or "phone" in message_lower or
              any("telefon" in prev_msg or "phone" in prev_msg for prev_msg in previous_messages)):
            print(f"🔍 Telefon konuşması tespit edildi")
            return self._handle_phone_conversation(message, context)
        
        # Tablet konuşması
        elif ("tablet" in message_lower or "ipad" in message_lower or
              any("tablet" in prev_msg or "ipad" in prev_msg for prev_msg in previous_messages)):
            print(f"🔍 Tablet konuşması tespit edildi")
            return self._handle_tablet_conversation(message, context)
        
        # Kulaklık konuşması
        elif ("kulaklık" in message_lower or "headphone" in message_lower or "airpods" in message_lower or
              any("kulaklık" in prev_msg or "headphone" in prev_msg for prev_msg in previous_messages)):
            print(f"🔍 Kulaklık konuşması tespit edildi")
            return self._handle_headphone_conversation(message, context)
        
        # Genel alışveriş
        elif any(word in message_lower for word in ["alışveriş", "satın al", "almak", "istiyorum"]):
            print(f"🔍 Genel alışveriş tespit edildi")
            return "Alışveriş konusunda size yardımcı olabilirim! Hangi ürün düşünüyorsunuz? (monitör, laptop, telefon, tablet, kulaklık, çanta, ayakkabı)"
        
        # Genel yanıt
        else:
            print(f"🔍 Genel yanıt döndürülüyor")
            return "Merhaba! Alışveriş konusunda size nasıl yardımcı olabilirim? Hangi ürün hakkında bilgi almak istiyorsunuz?"
    
    def _handle_monitor_conversation(self, message: str, context: Dict[str, Any]) -> str:
        """Monitör konuşmasını yönet"""
        message_lower = message.lower()
        
        # Hem boyut hem bütçe bilgisi varsa
        if (any(word in message_lower for word in ["inç", "inch", "27", "24", "32"]) and 
            any(word in message_lower for word in ["tl", "lira", "bütçe", "fiyat", "para"]) or
            any(char.isdigit() for char in message)):
            
            size = self._extract_size(message)
            budget = self._extract_number(message)
            context["monitor_size"] = size
            context["monitor_budget"] = budget
            
            print(f"🔍 Boyut: {size}, Bütçe: {budget}")
            
            if budget >= 15000:
                return f"Harika! {size} monitör ve {budget:,} TL bütçeniz var. Size premium monitör önerileri sunabilirim:\n\n🖥️ Samsung Odyssey G7 27\" 4K 240Hz - 28.999 TL (Trendyol)\n🖥️ LG 27GP950-B 27\" 4K Nano IPS 144Hz - 32.999 TL (Hepsiburada)\n🖥️ ASUS ROG Swift PG27AQ 27\" 4K 144Hz - 35.999 TL (Trendyol)\n🖥️ Dell Alienware AW2723DF 27\" QHD 280Hz - 24.999 TL (Hepsiburada)\n🖥️ MSI Optix MPG ARTYMIS 34\" Ultrawide - 18.999 TL (Trendyol)\n\nBu monitörler oyun ve profesyonel kullanım için mükemmel. Hangi özellikler önemli sizin için?"
            elif budget >= 8000:
                return f"Harika! {size} monitör ve {budget:,} TL bütçeniz var. Size orta segment monitör önerileri sunabilirim:\n\n🖥️ Samsung Odyssey G5 27\" QHD 144Hz - 8.999 TL (Trendyol)\n🖥️ LG 27GL850-B 27\" QHD Nano IPS 144Hz - 12.999 TL (Hepsiburada)\n🖥️ ASUS TUF Gaming VG27AQ 27\" QHD 165Hz - 9.999 TL (Trendyol)\n🖥️ AOC CQ27G2 27\" QHD 144Hz - 7.499 TL (Hepsiburada)\n🖥️ ViewSonic XG2405 24\" FHD 144Hz - 6.999 TL (Trendyol)\n\nBu monitörler hem oyun hem de iş için ideal. Hangi özellikler önemli sizin için?"
            else:
                return f"Harika! {size} monitör ve {budget:,} TL bütçeniz var. Size ekonomik monitör önerileri sunabilirim:\n\n🖥️ Samsung 24\" FHD 75Hz - 2.999 TL (Trendyol)\n🖥️ LG 24\" FHD IPS 75Hz - 3.499 TL (Hepsiburada)\n🖥️ ASUS 24\" FHD Gaming 144Hz - 3.999 TL (Trendyol)\n🖥️ AOC 24\" FHD 75Hz - 2.499 TL (Hepsiburada)\n🖥️ Philips 24\" FHD 75Hz - 2.799 TL (Trendyol)\n\nBu monitörler günlük kullanım için mükemmel. Hangi özellikler önemli sizin için?"
        
        # Sadece bütçe bilgisi
        elif any(word in message_lower for word in ["tl", "lira", "bütçe", "fiyat", "para"]) or any(char.isdigit() for char in message):
            budget = self._extract_number(message)
            context["monitor_budget"] = budget
            
            if budget >= 15000:
                return f"Harika! {budget:,} TL bütçeniz var. Size premium monitör önerileri sunabilirim:\n\n🖥️ Samsung Odyssey G7 27\" 4K 240Hz - 28.999 TL (Trendyol)\n🖥️ LG 27GP950-B 27\" 4K Nano IPS 144Hz - 32.999 TL (Hepsiburada)\n🖥️ ASUS ROG Swift PG27AQ 27\" 4K 144Hz - 35.999 TL (Trendyol)\n🖥️ Dell Alienware AW2723DF 27\" QHD 280Hz - 24.999 TL (Hepsiburada)\n🖥️ MSI Optix MPG ARTYMIS 34\" Ultrawide - 18.999 TL (Trendyol)\n\nBu monitörler oyun ve profesyonel kullanım için mükemmel. Hangi özellikler önemli sizin için?"
            elif budget >= 8000:
                return f"Harika! {budget:,} TL bütçeniz var. Size orta segment monitör önerileri sunabilirim:\n\n🖥️ Samsung Odyssey G5 27\" QHD 144Hz - 8.999 TL (Trendyol)\n🖥️ LG 27GL850-B 27\" QHD Nano IPS 144Hz - 12.999 TL (Hepsiburada)\n🖥️ ASUS TUF Gaming VG27AQ 27\" QHD 165Hz - 9.999 TL (Trendyol)\n🖥️ AOC CQ27G2 27\" QHD 144Hz - 7.499 TL (Hepsiburada)\n🖥️ ViewSonic XG2405 24\" FHD 144Hz - 6.999 TL (Trendyol)\n\nBu monitörler hem oyun hem de iş için ideal. Hangi özellikler önemli sizin için?"
            else:
                return f"Harika! {budget:,} TL bütçeniz var. Size ekonomik monitör önerileri sunabilirim:\n\n🖥️ Samsung 24\" FHD 75Hz - 2.999 TL (Trendyol)\n🖥️ LG 24\" FHD IPS 75Hz - 3.499 TL (Hepsiburada)\n🖥️ ASUS 24\" FHD Gaming 144Hz - 3.999 TL (Trendyol)\n🖥️ AOC 24\" FHD 75Hz - 2.499 TL (Hepsiburada)\n🖥️ Philips 24\" FHD 75Hz - 2.799 TL (Trendyol)\n\nBu monitörler günlük kullanım için mükemmel. Hangi özellikler önemli sizin için?"
        
        # Sadece boyut bilgisi
        elif any(word in message_lower for word in ["inç", "inch", "27", "24", "32"]):
            size = self._extract_size(message)
            context["monitor_size"] = size
            
            if "27" in size:
                return f"Mükemmel! {size} monitör seçiminiz çok iyi. Bu boyut hem oyun hem de iş için ideal. Bütçeniz nedir?"
            else:
                return f"Harika! {size} monitör seçiminiz çok iyi. Bütçeniz nedir?"
        
        # Özellik bilgisi
        elif any(word in message_lower for word in ["çözünürlük", "4k", "qhd", "full hd", "144hz", "gaming"]):
            features = self._extract_features(message)
            context["monitor_features"] = features
            
            if "4k" in features:
                return "4K çözünürlük harika bir seçim! Premium görüntü kalitesi için ideal. Bütçeniz nedir?"
            elif "qhd" in features:
                return "QHD çözünürlük çok iyi bir seçim! Hem performans hem kalite. Bütçeniz nedir?"
            else:
                return f"Harika! {', '.join(features)} özelliklerini tercih ediyorsunuz. Bütçeniz nedir?"
        
        # İlk monitör mesajı
        else:
            return "Monitör seçiminde size yardımcı olabilirim! Hangi boyut düşünüyorsunuz? (24\", 27\", 32\") Bütçeniz nedir?"
    
    def _handle_laptop_conversation(self, message: str, context: Dict[str, Any]) -> str:
        """Laptop konuşmasını yönet"""
        message_lower = message.lower()
        
        # Bütçe bilgisi (sayı içeren mesajlar)
        if any(word in message_lower for word in ["tl", "lira", "bütçe", "fiyat", "para"]) or any(char.isdigit() for char in message):
            budget = self._extract_number(message)
            context["laptop_budget"] = budget
            
            if budget >= 25000:
                return f"Harika! {budget:,} TL bütçeniz var. Size gaming laptop önerileri sunabilirim:\n\n💻 ASUS ROG Strix G15 Gaming RTX 4060 - 29.999 TL (Trendyol)\n💻 Lenovo Legion 5 Pro Gaming RTX 4070 - 32.999 TL (Hepsiburada)\n💻 MSI Katana GF66 Gaming RTX 4050 - 27.999 TL (Trendyol)\n💻 Dell G15 Gaming RTX 4060 - 31.999 TL (Hepsiburada)\n💻 HP Omen Gaming RTX 4060 - 28.999 TL (Trendyol)\n\nBu laptoplar oyun ve profesyonel kullanım için mükemmel. Hangi özellikler önemli sizin için?"
            elif budget >= 15000:
                return f"Harika! {budget:,} TL bütçeniz var. Size orta segment laptop önerileri sunabilirim:\n\n💻 Lenovo IdeaPad 5 15\" Ryzen 7 - 18.999 TL (Trendyol)\n💻 ASUS VivoBook 15\" Intel i7 - 19.999 TL (Hepsiburada)\n💻 HP Pavilion 15\" Intel i5 - 16.999 TL (Trendyol)\n💻 Dell Inspiron 15\" Intel i7 - 17.999 TL (Hepsiburada)\n💻 Acer Swift 3 14\" Ryzen 5 - 15.999 TL (Trendyol)\n\nBu laptoplar hem iş hem de günlük kullanım için ideal. Hangi özellikler önemli sizin için?"
            else:
                return f"Harika! {budget:,} TL bütçeniz var. Size ekonomik laptop önerileri sunabilirim:\n\n💻 Lenovo IdeaPad 3 15\" Intel i3 - 12.999 TL (Trendyol)\n💻 ASUS VivoBook 15\" Intel i3 - 13.999 TL (Hepsiburada)\n💻 HP 15\" Intel i3 - 11.999 TL (Trendyol)\n💻 Dell Inspiron 15\" Intel i3 - 12.499 TL (Hepsiburada)\n💻 Acer Aspire 3 15\" Intel i3 - 10.999 TL (Trendyol)\n\nBu laptoplar günlük kullanım ve eğitim için mükemmel. Hangi özellikler önemli sizin için?"
        
        # Özellik bilgisi
        elif any(word in message_lower for word in ["ram", "işlemci", "ssd", "oyun", "gaming"]):
            features = self._extract_laptop_features(message)
            context["laptop_features"] = features
            
            return f"Harika! {', '.join(features)} özelliklerini tercih ediyorsunuz. Bütçeniz nedir?"
        
        # İlk laptop mesajı
        else:
            return "Laptop seçiminde size yardımcı olabilirim! Hangi kullanım amaçlı? (oyun, iş, eğitim) Bütçeniz nedir?"
    
    def _handle_phone_conversation(self, message: str, context: Dict[str, Any]) -> str:
        """Telefon konuşmasını yönet"""
        message_lower = message.lower()
        
        # Bütçe bilgisi (sayı içeren mesajlar)
        if any(word in message_lower for word in ["tl", "lira", "bütçe", "fiyat", "para"]) or any(char.isdigit() for char in message):
            budget = self._extract_number(message)
            context["phone_budget"] = budget
            
            if budget >= 20000:
                return f"Harika! {budget:,} TL bütçeniz var. Size premium telefon önerileri sunabilirim:\n\n📱 iPhone 15 Pro 256GB - 49.999 TL (Trendyol)\n📱 Samsung Galaxy S24 Ultra 256GB - 44.999 TL (Hepsiburada)\n📱 Google Pixel 8 Pro 256GB - 39.999 TL (Trendyol)\n📱 iPhone 15 128GB - 34.999 TL (Hepsiburada)\n📱 Samsung Galaxy S24+ 256GB - 29.999 TL (Trendyol)\n\nBu telefonlar premium kullanıcılar için mükemmel. Hangi özellikler önemli sizin için?"
            elif budget >= 10000:
                return f"Harika! {budget:,} TL bütçeniz var. Size orta segment telefon önerileri sunabilirim:\n\n📱 Samsung Galaxy A55 256GB - 14.999 TL (Trendyol)\n📱 Xiaomi Redmi Note 13 Pro 256GB - 12.999 TL (Hepsiburada)\n📱 OPPO Reno 11 256GB - 16.999 TL (Trendyol)\n📱 Vivo V29 256GB - 13.999 TL (Hepsiburada)\n📱 Realme GT Neo 5 256GB - 11.999 TL (Trendyol)\n\nBu telefonlar hem performans hem de fiyat açısından ideal. Hangi özellikler önemli sizin için?"
            else:
                return f"Harika! {budget:,} TL bütçeniz var. Size ekonomik telefon önerileri sunabilirim:\n\n📱 Samsung Galaxy A15 128GB - 7.999 TL (Trendyol)\n📱 Xiaomi Redmi 13C 128GB - 6.999 TL (Hepsiburada)\n📱 OPPO A58 128GB - 8.499 TL (Trendyol)\n📱 Vivo Y27 128GB - 7.499 TL (Hepsiburada)\n📱 Realme C67 128GB - 5.999 TL (Trendyol)\n\nBu telefonlar günlük kullanım için mükemmel. Hangi özellikler önemli sizin için?"
        
        # İlk telefon mesajı
        else:
            return "Telefon seçiminde size yardımcı olabilirim! Hangi marka tercih ediyorsunuz? Bütçeniz nedir?"
    
    def _handle_tablet_conversation(self, message: str, context: Dict[str, Any]) -> str:
        """Tablet konuşmasını yönet"""
        message_lower = message.lower()
        
        # Bütçe bilgisi (sayı içeren mesajlar)
        if any(word in message_lower for word in ["tl", "lira", "bütçe", "fiyat", "para"]) or any(char.isdigit() for char in message):
            budget = self._extract_number(message)
            context["tablet_budget"] = budget
            
            if budget >= 15000:
                return f"Harika! {budget:,} TL bütçeniz var. Size premium tablet önerileri sunabilirim:\n\n📱 iPad Pro 12.9\" 256GB - 29.999 TL (Trendyol)\n📱 Samsung Galaxy Tab S9 Ultra 14.6\" 256GB - 24.999 TL (Hepsiburada)\n📱 iPad Air 10.9\" 256GB - 18.999 TL (Trendyol)\n📱 Samsung Galaxy Tab S9+ 12.4\" 256GB - 19.999 TL (Hepsiburada)\n📱 iPad 10.2\" 256GB - 12.999 TL (Trendyol)\n\nBu tabletlar profesyonel kullanım için mükemmel. Hangi özellikler önemli sizin için?"
            elif budget >= 8000:
                return f"Harika! {budget:,} TL bütçeniz var. Size orta segment tablet önerileri sunabilirim:\n\n📱 Samsung Galaxy Tab S9 11\" 128GB - 9.999 TL (Trendyol)\n📱 iPad 10.2\" 128GB - 8.999 TL (Hepsiburada)\n📱 Xiaomi Pad 6 11\" 128GB - 7.999 TL (Trendyol)\n📱 Lenovo Tab P11 11\" 128GB - 6.999 TL (Hepsiburada)\n📱 Huawei MatePad 10.4\" 128GB - 5.999 TL (Trendyol)\n\nBu tabletlar hem eğitim hem de eğlence için ideal. Hangi özellikler önemli sizin için?"
            else:
                return f"Harika! {budget:,} TL bütçeniz var. Size ekonomik tablet önerileri sunabilirim:\n\n📱 Samsung Galaxy Tab A8 10.5\" 64GB - 4.999 TL (Trendyol)\n📱 Lenovo Tab M10 10.1\" 64GB - 3.999 TL (Hepsiburada)\n📱 Huawei MatePad T10 10.1\" 64GB - 3.499 TL (Trendyol)\n📱 Alcatel 3T 10 10.1\" 32GB - 2.999 TL (Hepsiburada)\n📱 Prestigio MultiPad 10.1\" 32GB - 2.499 TL (Trendyol)\n\nBu tabletlar günlük kullanım için mükemmel. Hangi özellikler önemli sizin için?"
        
        # İlk tablet mesajı
        else:
            return "Tablet seçiminde size yardımcı olabilirim! Hangi kullanım amaçlı? (eğitim, oyun, iş) Bütçeniz nedir?"
    
    def _handle_headphone_conversation(self, message: str, context: Dict[str, Any]) -> str:
        """Kulaklık konuşmasını yönet"""
        message_lower = message.lower()
        
        # Bütçe bilgisi (sayı içeren mesajlar)
        if any(word in message_lower for word in ["tl", "lira", "bütçe", "fiyat", "para"]) or any(char.isdigit() for char in message):
            budget = self._extract_number(message)
            context["headphone_budget"] = budget
            
            if budget >= 3000:
                return f"Harika! {budget:,} TL bütçeniz var. Size premium kulaklık önerileri sunabilirim:\n\n🎧 Sony WH-1000XM5 - 8.999 TL (Trendyol)\n🎧 Apple AirPods Pro 2 - 6.999 TL (Hepsiburada)\n🎧 Bose QuietComfort 45 - 7.999 TL (Trendyol)\n🎧 Sennheiser Momentum 4 - 5.999 TL (Hepsiburada)\n🎧 Sony WF-1000XM5 - 4.999 TL (Trendyol)\n\nBu kulaklıklar premium ses kalitesi sunuyor. Hangi özellikler önemli sizin için?"
            elif budget >= 1000:
                return f"Harika! {budget:,} TL bütçeniz var. Size orta segment kulaklık önerileri sunabilirim:\n\n🎧 Sony WH-CH720N - 2.999 TL (Trendyol)\n🎧 JBL Tune 760NC - 1.999 TL (Hepsiburada)\n🎧 Samsung Galaxy Buds2 Pro - 2.499 TL (Trendyol)\n🎧 Anker Soundcore Q30 - 1.499 TL (Hepsiburada)\n🎧 Xiaomi Redmi Buds 4 Pro - 1.299 TL (Trendyol)\n\nBu kulaklıklar hem kalite hem de fiyat açısından ideal. Hangi özellikler önemli sizin için?"
            else:
                return f"Harika! {budget:,} TL bütçeniz var. Size ekonomik kulaklık önerileri sunabilirim:\n\n🎧 JBL Tune 500BT - 899 TL (Trendyol)\n🎧 Anker Soundcore Life Q20 - 699 TL (Hepsiburada)\n🎧 Xiaomi Redmi Buds 4 - 599 TL (Trendyol)\n🎧 Samsung Galaxy Buds FE - 799 TL (Hepsiburada)\n🎧 Realme Buds Air 3 - 499 TL (Trendyol)\n\nBu kulaklıklar günlük kullanım için mükemmel. Hangi özellikler önemli sizin için?"
        
        # İlk kulaklık mesajı
        else:
            return "Kulaklık seçiminde size yardımcı olabilirim! Hangi tür tercih ediyorsunuz? (kablosuz, kablolu, gaming) Bütçeniz nedir?"
    
    def _extract_number(self, message: str) -> int:
        """Mesajdan sayı çıkar"""
        import re
        numbers = re.findall(r'\d+', message)
        if numbers:
            return int(numbers[0])
        return 0
    
    def _extract_size(self, message: str) -> str:
        """Mesajdan boyut çıkar"""
        import re
        size_match = re.search(r'(\d+)\s*(?:inç|inch)', message.lower())
        if size_match:
            return f"{size_match.group(1)} inç"
        return "24 inç"
    
    def _extract_features(self, message: str) -> list:
        """Mesajdan özellik çıkar"""
        features = []
        message_lower = message.lower()
        
        if "4k" in message_lower:
            features.append("4K")
        if "qhd" in message_lower:
            features.append("QHD")
        if "full hd" in message_lower or "1080p" in message_lower:
            features.append("Full HD")
        if "144hz" in message_lower:
            features.append("144Hz")
        if "gaming" in message_lower or "oyun" in message_lower:
            features.append("Gaming")
        
        return features if features else ["Standart"]
    
    def _extract_laptop_features(self, message: str) -> list:
        """Mesajdan laptop özelliklerini çıkar"""
        features = []
        message_lower = message.lower()
        
        if "ram" in message_lower:
            features.append("RAM")
        if "işlemci" in message_lower or "cpu" in message_lower:
            features.append("İşlemci")
        if "ssd" in message_lower:
            features.append("SSD")
        if "oyun" in message_lower or "gaming" in message_lower:
            features.append("Gaming")
        
        return features if features else ["Standart"]
    
    def _update_simple_context(self, context: Dict[str, Any], message: str, response: str) -> Dict[str, Any]:
        """Basit context güncelleme"""
        updated_context = context.copy()
        
        # Conversation history'yi güncelle
        conversation_history = updated_context.get("conversation_history", [])
        conversation_history.append({
            "message": message,
            "response": response,
            "timestamp": "2025-01-29T17:33:30Z"
        })
        
        # Son 5 mesajı tut
        if len(conversation_history) > 5:
            conversation_history = conversation_history[-5:]
            
        updated_context["conversation_history"] = conversation_history
        
        return updated_context 