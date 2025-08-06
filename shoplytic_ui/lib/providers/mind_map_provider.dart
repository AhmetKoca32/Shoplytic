import 'package:flutter/material.dart';

import '../services/api_service.dart';

class MindMapNode {
  final String title;
  final List<MindMapNode> children;
  final String? category;
  final String? priority;
  final List<String>? items;
  final List<Map<String, dynamic>>? products;

  MindMapNode(
    this.title, {
    this.children = const [],
    this.category,
    this.priority,
    this.items,
    this.products,
  });
}

class MindMapProvider with ChangeNotifier {
  late MindMapNode _root;
  bool _isLoading = false;
  String? _error;
  String? _workflowId;
  final ApiService _apiService = ApiService();

  MindMapNode get root => _root;
  bool get isLoading => _isLoading;
  String? get error => _error;
  String? get workflowId => _workflowId;

  MindMapProvider() {
    // Başlangıçta boş harita
    _root = MindMapNode('Ana Fikir', children: []);
  }

  void setMap(MindMapNode root) {
    _root = root;
    _error = null;
    notifyListeners();
  }

  void addNode(MindMapNode parent, String title) {
    parent.children.add(MindMapNode(title));
    notifyListeners();
  }

  // API ile zihin haritası oluştur
  Future<void> generateMindMap(
    String userInput, {
    Map<String, dynamic>? userPreferences,
  }) async {
    _isLoading = true;
    _error = null;
    _workflowId = null;
    notifyListeners();

    try {
      final response = await _apiService.generateMindMap(
        userInput: userInput,
        userPreferences: userPreferences,
      );

      print('🔍 MindMapProvider: Response analiz ediliyor...');
      print('📊 Response: $response');

      if (response['success'] == true && response['mind_map'] != null) {
        final mindMapData = response['mind_map'];
        _workflowId = response['workflow_id'];

        print('✅ Mind Map verisi bulundu!');
        print('📋 Mind Map Data: $mindMapData');

        // Backend'den gelen veri formatını kontrol et
        Map<String, dynamic> actualMindMapData;

        // İç içe mind_map kontrolü
        if (mindMapData['mind_map'] != null) {
          actualMindMapData = mindMapData['mind_map'];
          print('🔄 İç içe mind_map bulundu, düzeltiliyor...');
        } else {
          actualMindMapData = mindMapData;
        }

        print('📋 Actual Mind Map Data: $actualMindMapData');

        // Backend'den gelen genel workflow yanıtını mind map formatına çevir
        if (actualMindMapData['agent_type'] == 'general' &&
            actualMindMapData['result'] != null) {
          print('🔄 Genel workflow yanıtı mind map formatına çevriliyor...');

          // Kullanıcı input'una göre kategoriler oluştur
          final categories = _createCategoriesFromUserInput(userInput);

          final nodes = categories.map((category) {
            return MindMapNode(
              category['name'] ?? 'Kategori',
              category: category['name'],
              priority: category['priority']?.toString(),
              items: category['items'] != null
                  ? List<String>.from(category['items'])
                  : null,
              products: category['products'] != null
                  ? List<Map<String, dynamic>>.from(category['products'])
                  : null,
            );
          }).toList();

          _root = MindMapNode('Üniversite Hazırlığı', children: nodes);
        } else if (actualMindMapData['result'] != null &&
            actualMindMapData['result']['categories'] != null) {
          // Yeni format: result.categories
          final categories = actualMindMapData['result']['categories'] as List;
          final nodes = categories.map((category) {
            // Debug: E-ticaret ürünlerini kontrol et
            print('🔍 Kategori: ${category['name']}');
            print('📦 E-ticaret ürünleri: ${category['ecommerce_products']}');

            return MindMapNode(
              category['name'] ?? 'Kategori',
              category: category['name'],
              priority: category['priority']?.toString(),
              items: category['products'] != null
                  ? List<String>.from(category['products'])
                  : null,
              products: category['ecommerce_products'] != null
                  ? List<Map<String, dynamic>>.from(
                      category['ecommerce_products'],
                    )
                  : null,
            );
          }).toList();

          _root = MindMapNode('Ana Fikir', children: nodes);
        } else if (actualMindMapData['main_categories'] != null) {
          final categories = actualMindMapData['main_categories'] as List;
          final nodes = categories.map((category) {
            return MindMapNode(
              category['name'] ?? 'Kategori',
              category: category['name'],
              priority: category['priority'],
              items: category['items'] != null
                  ? List<String>.from(category['items'])
                  : null,
              products: category['products'] != null
                  ? List<Map<String, dynamic>>.from(category['products'])
                  : null,
            );
          }).toList();

          _root = MindMapNode(
            actualMindMapData['central_topic'] ?? 'Ana Fikir',
            children: nodes,
          );
        } else if (actualMindMapData['categories'] != null) {
          // Eski API yapısı için geriye uyumluluk
          final categories = actualMindMapData['categories'] as List;
          final nodes = categories.map((category) {
            return MindMapNode(
              category['name'] ?? 'Kategori',
              category: category['name'],
              priority: category['priority']?.toString(),
              items: category['products'] != null
                  ? List<String>.from(category['products'])
                  : null,
            );
          }).toList();

          _root = MindMapNode('Ana Fikir', children: nodes);
        } else {
          // Hiçbir format uymuyorsa, kullanıcı input'una göre varsayılan kategoriler oluştur
          print(
            '⚠️ Backend formatı tanınmadı, varsayılan kategoriler oluşturuluyor...',
          );
          final categories = _createCategoriesFromUserInput(userInput);

          final nodes = categories.map((category) {
            return MindMapNode(
              category['name'] ?? 'Kategori',
              category: category['name'],
              priority: category['priority']?.toString(),
              items: category['items'] != null
                  ? List<String>.from(category['items'])
                  : null,
              products: category['products'] != null
                  ? List<Map<String, dynamic>>.from(category['products'])
                  : null,
            );
          }).toList();

          _root = MindMapNode('Üniversite Hazırlığı', children: nodes);
        }
      } else {
        _error = 'Zihin haritası oluşturulamadı';
      }
    } catch (e) {
      _error = 'Zihin haritası oluşturulurken hata oluştu: $e';
      print('Mind map generation error: $e');
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  // Kullanıcı input'una göre kategoriler oluştur
  List<Map<String, dynamic>> _createCategoriesFromUserInput(String userInput) {
    final inputLower = userInput.toLowerCase();

    if (inputLower.contains('üniversite') ||
        inputLower.contains('okul') ||
        inputLower.contains('eğitim')) {
      return [
        {
          "name": "Akademik Malzemeler",
          "items": [
            "laptop",
            "çanta",
            "defter",
            "kalem",
            "hesap makinesi",
            "yazıcı",
          ],
          "priority": "high",
          "products": [
            {
              "name": "Lenovo ThinkPad E15",
              "price": 15999.99,
              "platform": "Trendyol",
              "rating": 4.5,
              "url": "https://trendyol.com/laptop-1",
              "image": "https://via.placeholder.com/150",
              "description": "Üniversite öğrencileri için ideal laptop",
            },
            {
              "name": "Samsonite Çanta",
              "price": 899.99,
              "platform": "Hepsiburada",
              "rating": 4.3,
              "url": "https://hepsiburada.com/canta-1",
              "image": "https://via.placeholder.com/150",
              "description": "Dayanıklı ve geniş okul çantası",
            },
            {
              "name": "HP Pavilion Laptop",
              "price": 12999.99,
              "platform": "Trendyol",
              "rating": 4.6,
              "url": "https://trendyol.com/laptop-2",
              "image": "https://via.placeholder.com/150",
              "description": "Güçlü performanslı öğrenci laptopu",
            },
            {
              "name": "Nike Spor Çanta",
              "price": 299.99,
              "platform": "Hepsiburada",
              "rating": 4.2,
              "url": "https://hepsiburada.com/canta-2",
              "image": "https://via.placeholder.com/150",
              "description": "Spor ve okul için çok amaçlı çanta",
            },
            {
              "name": "Casio Hesap Makinesi",
              "price": 199.99,
              "platform": "Trendyol",
              "rating": 4.8,
              "url": "https://trendyol.com/hesap-makinesi",
              "image": "https://via.placeholder.com/150",
              "description": "Bilimsel hesap makinesi",
            },
          ],
        },
        {
          "name": "Kırtasiye",
          "items": ["defter", "kalem", "silgi", "kalemlik", "dosya", "post-it"],
          "priority": "medium",
          "products": [
            {
              "name": "Moleskine Defter",
              "price": 89.99,
              "platform": "Trendyol",
              "rating": 4.7,
              "url": "https://trendyol.com/defter-1",
              "image": "https://via.placeholder.com/150",
              "description": "Kaliteli not defteri",
            },
            {
              "name": "Pilot Kalem Seti",
              "price": 45.99,
              "platform": "Hepsiburada",
              "rating": 4.4,
              "url": "https://hepsiburada.com/kalem-seti",
              "image": "https://via.placeholder.com/150",
              "description": "12'li renkli kalem seti",
            },
            {
              "name": "Staedtler Silgi",
              "price": 12.99,
              "platform": "Trendyol",
              "rating": 4.6,
              "url": "https://trendyol.com/silgi",
              "image": "https://via.placeholder.com/150",
              "description": "Profesyonel silgi",
            },
            {
              "name": "3M Post-it",
              "price": 25.99,
              "platform": "Hepsiburada",
              "rating": 4.5,
              "url": "https://hepsiburada.com/post-it",
              "image": "https://via.placeholder.com/150",
              "description": "Renkli yapışkan notlar",
            },
            {
              "name": "Dosya Organizörü",
              "price": 35.99,
              "platform": "Trendyol",
              "rating": 4.3,
              "url": "https://trendyol.com/dosya-organizor",
              "image": "https://via.placeholder.com/150",
              "description": "Ders notları için dosya organizörü",
            },
          ],
        },
        {
          "name": "Teknoloji",
          "items": [
            "tablet",
            "kulaklık",
            "powerbank",
            "klavye",
            "mouse",
            "webcam",
          ],
          "priority": "medium",
          "products": [
            {
              "name": "Samsung Galaxy Tab",
              "price": 3999.99,
              "platform": "Hepsiburada",
              "rating": 4.4,
              "url": "https://hepsiburada.com/tablet-1",
              "image": "https://via.placeholder.com/150",
              "description": "Eğitim için ideal tablet",
            },
            {
              "name": "Sony WH-1000XM4",
              "price": 2999.99,
              "platform": "Trendyol",
              "rating": 4.9,
              "url": "https://trendyol.com/kulaklik",
              "image": "https://via.placeholder.com/150",
              "description": "Gürültü önleyici kulaklık",
            },
            {
              "name": "Anker PowerBank",
              "price": 199.99,
              "platform": "Hepsiburada",
              "rating": 4.7,
              "url": "https://hepsiburada.com/powerbank",
              "image": "https://via.placeholder.com/150",
              "description": "20000mAh taşınabilir şarj",
            },
            {
              "name": "Logitech K380 Klavye",
              "price": 299.99,
              "platform": "Trendyol",
              "rating": 4.6,
              "url": "https://trendyol.com/klavye",
              "image": "https://via.placeholder.com/150",
              "description": "Bluetooth kablosuz klavye",
            },
            {
              "name": "Logitech C920 Webcam",
              "price": 599.99,
              "platform": "Hepsiburada",
              "rating": 4.5,
              "url": "https://hepsiburada.com/webcam",
              "image": "https://via.placeholder.com/150",
              "description": "HD webcam online dersler için",
            },
          ],
        },
      ];
    } else if (inputLower.contains('ev') || inputLower.contains('yeni ev')) {
      return [
        {
          "name": "Mobilya",
          "items": ["yatak", "masa", "dolap", "koltuk", "sandık", "gardrop"],
          "priority": "high",
          "products": [
            {
              "name": "IKEA Yatak",
              "price": 1299.99,
              "platform": "IKEA",
              "rating": 4.2,
              "url": "https://ikea.com/yatak-1",
              "image": "https://via.placeholder.com/150",
              "description": "Rahat ve dayanıklı yatak",
            },
            {
              "name": "Çalışma Masası",
              "price": 599.99,
              "platform": "Trendyol",
              "rating": 4.5,
              "url": "https://trendyol.com/masa",
              "image": "https://via.placeholder.com/150",
              "description": "Modern çalışma masası",
            },
            {
              "name": "Koltuk Takımı",
              "price": 2499.99,
              "platform": "Hepsiburada",
              "rating": 4.3,
              "url": "https://hepsiburada.com/koltuk",
              "image": "https://via.placeholder.com/150",
              "description": "3+3+1 koltuk takımı",
            },
            {
              "name": "Gardrop",
              "price": 899.99,
              "platform": "IKEA",
              "rating": 4.4,
              "url": "https://ikea.com/gardrop",
              "image": "https://via.placeholder.com/150",
              "description": "Geniş gardrop",
            },
          ],
        },
        {
          "name": "Ev Tekstili",
          "items": ["çarşaf", "yastık", "battaniye", "havlu", "perde"],
          "priority": "medium",
          "products": [
            {
              "name": "Pamuklu Çarşaf Takımı",
              "price": 199.99,
              "platform": "Trendyol",
              "rating": 4.6,
              "url": "https://trendyol.com/carsaf",
              "image": "https://via.placeholder.com/150",
              "description": "100% pamuk çarşaf takımı",
            },
            {
              "name": "Yastık Seti",
              "price": 89.99,
              "platform": "Hepsiburada",
              "rating": 4.4,
              "url": "https://hepsiburada.com/yastik",
              "image": "https://via.placeholder.com/150",
              "description": "2'li yastık seti",
            },
            {
              "name": "Battaniye",
              "price": 149.99,
              "platform": "Trendyol",
              "rating": 4.5,
              "url": "https://trendyol.com/battaniye",
              "image": "https://via.placeholder.com/150",
              "description": "Sıcak battaniye",
            },
          ],
        },
      ];
    } else {
      // Genel kategoriler
      return [
        {
          "name": "Temel İhtiyaçlar",
          "items": ["temel ürünler"],
          "priority": "high",
          "products": [],
        },
        {
          "name": "Öneriler",
          "items": ["önerilen ürünler"],
          "priority": "medium",
          "products": [],
        },
      ];
    }
  }

  // Workflow çalıştır
  Future<void> executeWorkflow(
    Map<String, dynamic> inputData,
    String workflowType, {
    String? userId,
  }) async {
    _isLoading = true;
    _error = null;
    _workflowId = null;
    notifyListeners();

    try {
      final response = await _apiService.executeWorkflow(
        inputData: inputData,
        workflowType: workflowType,
        userId: userId,
      );

      if (response['success'] == true && response['result'] != null) {
        final result = response['result'];
        _workflowId = response['workflow_id'];

        if (result['mind_map'] != null) {
          final mindMapData = result['mind_map'];

          if (mindMapData['main_categories'] != null) {
            final categories = mindMapData['main_categories'] as List;
            final nodes = categories.map((category) {
              return MindMapNode(
                category['name'] ?? 'Kategori',
                category: category['name'],
                priority: category['priority'],
                items: category['items'] != null
                    ? List<String>.from(category['items'])
                    : null,
                products: category['products'] != null
                    ? List<Map<String, dynamic>>.from(category['products'])
                    : null,
              );
            }).toList();

            _root = MindMapNode(
              mindMapData['central_topic'] ?? 'Ana Fikir',
              children: nodes,
            );
          }
        }
      } else {
        _error = 'Workflow çalıştırılamadı';
      }
    } catch (e) {
      _error = 'Workflow çalıştırılırken hata oluştu: $e';
      print('Workflow execution error: $e');
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  // Ürün arama
  Future<List<Map<String, dynamic>>> searchProducts(
    String query, {
    String? category,
    int limit = 10,
  }) async {
    try {
      final response = await _apiService.searchProducts(
        query: query,
        category: category,
        limit: limit,
      );

      if (response['success'] == true) {
        return List<Map<String, dynamic>>.from(response['products'] ?? []);
      } else {
        _error = 'Ürün arama başarısız';
        return [];
      }
    } catch (e) {
      _error = 'Ürün arama hatası: $e';
      return [];
    }
  }

  // Fiyat karşılaştırması
  Future<Map<String, dynamic>> comparePrices(String productName) async {
    try {
      final response = await _apiService.comparePrices(productName);

      if (response['success'] == true) {
        return response['comparison'] ?? {};
      } else {
        _error = 'Fiyat karşılaştırması başarısız';
        return {};
      }
    } catch (e) {
      _error = 'Fiyat karşılaştırması hatası: $e';
      return {};
    }
  }

  // Stok kontrolü
  Future<Map<String, dynamic>> checkStock(String productId) async {
    try {
      final response = await _apiService.checkStock(productId);

      if (response['success'] == true) {
        return response['stock_info'] ?? {};
      } else {
        _error = 'Stok kontrolü başarısız';
        return {};
      }
    } catch (e) {
      _error = 'Stok kontrolü hatası: $e';
      return {};
    }
  }

  // Ürün önerileri
  Future<List<Map<String, dynamic>>> getRecommendations(
    String category, {
    double? budget,
    double? rating,
  }) async {
    try {
      final response = await _apiService.getRecommendations(
        category: category,
        budget: budget,
        rating: rating,
      );

      if (response['success'] == true) {
        return List<Map<String, dynamic>>.from(
          response['recommendations'] ?? [],
        );
      } else {
        _error = 'Ürün önerileri alınamadı';
        return [];
      }
    } catch (e) {
      _error = 'Ürün önerileri hatası: $e';
      return [];
    }
  }

  // Sistem durumu kontrolü
  Future<Map<String, dynamic>> getSystemStatus() async {
    try {
      return await _apiService.getSystemStatus();
    } catch (e) {
      return {"api_status": "error", "error": e.toString()};
    }
  }

  void clearError() {
    _error = null;
    notifyListeners();
  }

  void reset() {
    _root = MindMapNode('Ana Fikir', children: []);
    _error = null;
    _workflowId = null;
    _isLoading = false;
    notifyListeners();
  }
}
