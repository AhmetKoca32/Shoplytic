"""
Gerçek e-ticaret platformlarından ürün çekme servisi
"""
import aiohttp
import asyncio
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
import json

logger = logging.getLogger(__name__)

class EcommerceService:
    """Gerçek e-ticaret platformlarından ürün çekme servisi"""
    
    def __init__(self):
        self.session = None
        self.platforms = {
            "trendyol": {
                "base_url": "https://api.trendyol.com/sapigw",
                "headers": {
                    "User-Agent": "Shoplytic/1.0",
                    "Content-Type": "application/json"
                }
            },
            "hepsiburada": {
                "base_url": "https://marketplace.hepsiburada.com/api",
                "headers": {
                    "User-Agent": "Shoplytic/1.0",
                    "Content-Type": "application/json"
                }
            },
            "amazon": {
                "base_url": "https://amazon.com.tr",
                "headers": {
                    "User-Agent": "Shoplytic/1.0",
                    "Content-Type": "application/json"
                }
            }
        }
    
    async def _get_session(self):
        """HTTP session oluştur"""
        if self.session is None:
            self.session = aiohttp.ClientSession()
        return self.session
    
    async def search_products_by_category(self, category: str, products: List[str], limit: int = 5) -> List[Dict[str, Any]]:
        """Kategori ve ürün listesine göre arama yap"""
        try:
            session = await self._get_session()
            all_products = []
            
            # Sadece ilk ürünü ara (performans için)
            if products:
                product_name = products[0]
                
                # Alternatif kaynaklardan arama
                search_methods = [
                    ('Trendyol', self._search_trendyol),
                    ('Hepsiburada', self._search_hepsiburada),
                    ('Amazon', self._search_amazon),
                    ('N11', self._search_n11),
                ]
                
                for platform_name, search_method in search_methods:
                    try:
                        products_found = await asyncio.wait_for(
                            search_method(session, product_name, category),
                            timeout=5.0
                        )
                        if products_found:
                            all_products.extend(products_found)
                            logger.info(f"{platform_name}'dan {len(products_found)} ürün bulundu")
                            break  # İlk başarılı kaynaktan sonra dur
                    except asyncio.TimeoutError:
                        logger.warning(f"{platform_name} timeout: {product_name}")
                    except Exception as e:
                        logger.warning(f"{platform_name} hatası: {e}")
            
            # En iyi ürünleri seç
            if all_products:
                sorted_products = sorted(all_products, key=lambda x: (
                    x.get('rating', 0), 
                    -x.get('price', float('inf')),
                    x.get('stock', False)
                ), reverse=True)
                return sorted_products[:limit]
            else:
                # Hiç ürün bulunamazsa fallback
                return await self._get_fallback_products(category, products, limit)
            
        except Exception as e:
            logger.error(f"Ürün arama hatası: {e}")
            return await self._get_fallback_products(category, products, limit)
    
    async def _search_trendyol(self, session: aiohttp.ClientSession, product_name: str, category: str) -> List[Dict[str, Any]]:
        """Trendyol'dan ürün ara"""
        try:
            # Trendyol web sayfasından arama (daha güvenilir)
            search_url = f"https://www.trendyol.com/sr?q={product_name}"
            
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
                "Accept-Encoding": "gzip, deflate, br",
                "DNT": "1",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "none",
                "Sec-Fetch-User": "?1",
                "Cache-Control": "max-age=0"
            }
            
            async with session.get(search_url, headers=headers, timeout=15) as response:
                if response.status == 200:
                    html_content = await response.text()
                    return self._parse_trendyol_html(html_content, product_name)
                else:
                    logger.warning(f"Trendyol web arama hatası: {response.status}")
                    return []
                    
        except Exception as e:
            logger.error(f"Trendyol arama hatası: {e}")
            return []
    
    async def _search_hepsiburada(self, session: aiohttp.ClientSession, product_name: str, category: str) -> List[Dict[str, Any]]:
        """Hepsiburada'dan ürün ara"""
        try:
            # Hepsiburada web scraping (daha güvenilir)
            search_url = f"https://www.hepsiburada.com/ara?q={product_name}"
            
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "tr-TR,tr;q=0.9,en;q=0.8",
                "Referer": "https://www.hepsiburada.com/"
            }
            
            async with session.get(search_url, headers=headers, timeout=10) as response:
                if response.status == 200:
                    html_content = await response.text()
                    return self._parse_hepsiburada_html(html_content, product_name)
                else:
                    logger.warning(f"Hepsiburada web arama hatası: {response.status}")
                    return []
            url = f"https://marketplace.hepsiburada.com/api/search?q={product_name}&category={category}"
            
            async with session.get(url, headers=self.platforms["hepsiburada"]["headers"]) as response:
                if response.status == 200:
                    data = await response.json()
                    return self._parse_hepsiburada_response(data, product_name)
                else:
                    logger.warning(f"Hepsiburada API hatası: {response.status}")
                    return []
                    
        except Exception as e:
            logger.error(f"Hepsiburada arama hatası: {e}")
            return []
    
    async def _search_amazon(self, session: aiohttp.ClientSession, product_name: str, category: str) -> List[Dict[str, Any]]:
        """Amazon'dan ürün ara"""
        try:
            search_url = f"https://www.amazon.com.tr/s?k={product_name}"
            
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "tr-TR,tr;q=0.9,en;q=0.8",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive"
            }
            
            async with session.get(search_url, headers=headers, timeout=10) as response:
                if response.status == 200:
                    html_content = await response.text()
                    return self._parse_amazon_html(html_content, product_name)
                else:
                    logger.warning(f"Amazon arama hatası: {response.status}")
                    return []
                    
        except Exception as e:
            logger.error(f"Amazon arama hatası: {e}")
            return []
    
    async def _search_n11(self, session: aiohttp.ClientSession, product_name: str, category: str) -> List[Dict[str, Any]]:
        """N11'den ürün ara"""
        try:
            search_url = f"https://www.n11.com/arama?q={product_name}"
            
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "tr-TR,tr;q=0.9,en;q=0.8",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive"
            }
            
            async with session.get(search_url, headers=headers, timeout=10) as response:
                if response.status == 200:
                    html_content = await response.text()
                    return self._parse_n11_html(html_content, product_name)
                else:
                    logger.warning(f"N11 arama hatası: {response.status}")
                    return []
                    
        except Exception as e:
            logger.error(f"N11 arama hatası: {e}")
            return []
    
    def _get_category_id(self, category: str) -> str:
        """Kategori adından ID döndür"""
        category_mapping = {
            "Giyim": "411",
            "Elektronik": "1249", 
            "Ev ve Yaşam": "1249",
            "Kişisel Bakım": "1249",
            "Kitap ve Kırtasiye": "1249",
            "Spor ve Outdoor": "1249"
        }
        return category_mapping.get(category, "1249")
    
    def _parse_trendyol_html(self, html_content: str, product_name: str) -> List[Dict[str, Any]]:
        """Trendyol HTML içeriğini parse et"""
        products = []
        try:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Ürün kartlarını bul (güncel CSS class'ları)
            product_cards = soup.find_all('div', class_='p-card-wrppr') or \
                           soup.find_all('div', class_='product-card') or \
                           soup.find_all('div', {'data-testid': 'product-card'})
            
            for card in product_cards[:5]:
                try:
                    # Ürün adı
                    name_elem = card.find('span', class_='prdct-desc-cntnr-name') or \
                               card.find('h3') or \
                               card.find('div', class_='product-name')
                    name = name_elem.get_text(strip=True) if name_elem else product_name
                    
                    # Fiyat
                    price_elem = card.find('div', class_='prc-box-dscntd') or \
                                card.find('span', class_='price') or \
                                card.find('div', class_='product-price')
                    price = 0
                    if price_elem:
                        price_text = price_elem.get_text(strip=True)
                        # Sadece sayıları al
                        price_digits = ''.join(filter(str.isdigit, price_text))
                        price = float(price_digits) if price_digits else 0
                    
                    # Resim
                    img_elem = card.find('img')
                    image = img_elem.get('src', '') if img_elem else ''
                    if not image and img_elem:
                        image = img_elem.get('data-src', '')  # Lazy loading
                    
                    # Link
                    link_elem = card.find('a')
                    url = 'https://www.trendyol.com' + link_elem.get('href', '') if link_elem else ''
                    
                    products.append({
                        'id': f"ty_{len(products)}",
                        'name': name,
                        'price': price,
                        'platform': 'Trendyol',
                        'rating': 4.0,
                        'stock': True,
                        'url': url,
                        'image': image,
                        'category': product_name,
                        'description': f'{product_name} ürünü - Trendyol'
                    })
                except Exception as e:
                    logger.error(f"Trendyol ürün kartı parse hatası: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"Trendyol HTML parse hatası: {e}")
        return products
    
    def _parse_hepsiburada_html(self, html_content: str, product_name: str) -> List[Dict[str, Any]]:
        """Hepsiburada HTML içeriğini parse et"""
        products = []
        try:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Ürün kartlarını bul
            product_cards = soup.find_all('li', class_='productListContent-zAP0Y5msy8OHn5z7T_K_')
            
            for card in product_cards[:5]:
                try:
                    # Ürün adı
                    name_elem = card.find('h3', class_='productListContent-title')
                    name = name_elem.get_text(strip=True) if name_elem else product_name
                    
                    # Fiyat
                    price_elem = card.find('div', class_='price-value')
                    price = 0
                    if price_elem:
                        price_text = price_elem.get_text(strip=True)
                        price = float(''.join(filter(str.isdigit, price_text))) if price_text else 0
                    
                    # Resim
                    img_elem = card.find('img')
                    image = img_elem.get('src', '') if img_elem else ''
                    
                    # Link
                    link_elem = card.find('a')
                    url = 'https://www.hepsiburada.com' + link_elem.get('href', '') if link_elem else ''
                    
                    products.append({
                        'id': f"hb_{len(products)}",
                        'name': name,
                        'price': price,
                        'platform': 'Hepsiburada',
                        'rating': 4.0,
                        'stock': True,
                        'url': url,
                        'image': image,
                        'category': product_name,
                        'description': f'{product_name} ürünü - Hepsiburada'
                    })
                except Exception as e:
                    logger.error(f"Hepsiburada ürün kartı parse hatası: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"Hepsiburada HTML parse hatası: {e}")
        return products
    
    def _parse_amazon_html(self, html_content: str, product_name: str) -> List[Dict[str, Any]]:
        """Amazon HTML içeriğini parse et"""
        products = []
        try:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Amazon ürün kartlarını bul
            product_cards = soup.find_all('div', {'data-component-type': 's-search-result'})
            
            for card in product_cards[:5]:
                try:
                    # Ürün adı
                    name_elem = card.find('span', class_='a-text-normal') or \
                               card.find('h2', class_='a-size-mini')
                    name = name_elem.get_text(strip=True) if name_elem else product_name
                    
                    # Fiyat
                    price_elem = card.find('span', class_='a-price-whole') or \
                                card.find('span', class_='a-price')
                    price = 0
                    if price_elem:
                        price_text = price_elem.get_text(strip=True)
                        price_digits = ''.join(filter(str.isdigit, price_text))
                        price = float(price_digits) if price_digits else 0
                    
                    # Resim
                    img_elem = card.find('img', class_='s-image')
                    image = img_elem.get('src', '') if img_elem else ''
                    
                    # Link
                    link_elem = card.find('a', class_='a-link-normal')
                    url = 'https://www.amazon.com.tr' + link_elem.get('href', '') if link_elem else ''
                    
                    products.append({
                        'id': f"amz_{len(products)}",
                        'name': name,
                        'price': price,
                        'platform': 'Amazon',
                        'rating': 4.0,
                        'stock': True,
                        'url': url,
                        'image': image,
                        'category': product_name,
                        'description': f'{product_name} ürünü - Amazon'
                    })
                except Exception as e:
                    logger.error(f"Amazon ürün kartı parse hatası: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"Amazon HTML parse hatası: {e}")
        return products
    
    def _parse_n11_html(self, html_content: str, product_name: str) -> List[Dict[str, Any]]:
        """N11 HTML içeriğini parse et"""
        products = []
        try:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # N11 ürün kartlarını bul
            product_cards = soup.find_all('li', class_='column') or \
                           soup.find_all('div', class_='productItem')
            
            for card in product_cards[:5]:
                try:
                    # Ürün adı
                    name_elem = card.find('h3', class_='productName') or \
                               card.find('a', class_='plink')
                    name = name_elem.get_text(strip=True) if name_elem else product_name
                    
                    # Fiyat
                    price_elem = card.find('div', class_='priceContainer') or \
                                card.find('span', class_='price')
                    price = 0
                    if price_elem:
                        price_text = price_elem.get_text(strip=True)
                        price_digits = ''.join(filter(str.isdigit, price_text))
                        price = float(price_digits) if price_digits else 0
                    
                    # Resim
                    img_elem = card.find('img')
                    image = img_elem.get('src', '') if img_elem else ''
                    
                    # Link
                    link_elem = card.find('a', class_='plink')
                    url = 'https://www.n11.com' + link_elem.get('href', '') if link_elem else ''
                    
                    products.append({
                        'id': f"n11_{len(products)}",
                        'name': name,
                        'price': price,
                        'platform': 'N11',
                        'rating': 4.0,
                        'stock': True,
                        'url': url,
                        'image': image,
                        'category': product_name,
                        'description': f'{product_name} ürünü - N11'
                    })
                except Exception as e:
                    logger.error(f"N11 ürün kartı parse hatası: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"N11 HTML parse hatası: {e}")
        return products
    
    async def _get_fallback_products(self, category: str, products: List[str], limit: int) -> List[Dict[str, Any]]:
        """API hatası durumunda fallback ürünler döndür"""
        fallback_products = []
        
        # Kategori bazlı resim anahtar kelimeleri
        category_image_keywords = {
            "Elektronik": ["electronics", "gadget", "tech", "smartphone", "laptop"],
            "Giyim": ["clothing", "fashion", "shirt", "dress", "shoes"],
            "Ev ve Yaşam": ["furniture", "home", "kitchen", "bedroom", "living"],
            "Kişisel Bakım": ["cosmetics", "beauty", "skincare", "makeup", "perfume"],
            "Kitap ve Kırtasiye": ["book", "stationery", "pen", "notebook", "office"],
            "Spor ve Outdoor": ["sports", "fitness", "outdoor", "exercise", "gym"]
        }
        
        image_keywords = category_image_keywords.get(category, ["product", "item", "shopping"])
        
        for i, product_name in enumerate(products[:limit]):
            import random
            
            # Gerçekçi resim URL'leri oluştur
            keyword = random.choice(image_keywords)
            image_urls = [
                f"https://source.unsplash.com/300x300/?{product_name.lower().replace(' ', '+')}",
                f"https://source.unsplash.com/300x300/?{keyword}",
                f"https://source.unsplash.com/300x300/?{category.lower().replace(' ', '+')}",
                f"https://source.unsplash.com/300x300/?{keyword}+product",
                f"https://source.unsplash.com/300x300/?{keyword}+item"
            ]
            
            fallback_products.append({
                "id": f"fallback_{i}",
                "name": f"{product_name} - {category}",
                "price": 100 + (i * 50),
                "platform": "Demo",
                "rating": 4.0 + (i * 0.1),
                "stock": True,
                "url": f"https://demo.com/{product_name.lower().replace(' ', '-')}",
                "image": random.choice(image_urls),
                "category": category,
                "description": f"{product_name} ürünü - {category} kategorisinde kaliteli seçenek"
            })
        
        return fallback_products
    
    async def close(self):
        """Session'ı kapat"""
        if self.session:
            await self.session.close()
            self.session = None 