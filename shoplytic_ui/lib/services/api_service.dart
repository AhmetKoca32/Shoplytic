import 'package:dio/dio.dart';

class ApiService {
  // Backend URL'leri - geliştirme ortamı için
  static const String baseUrl = 'http://localhost:8000/api/v1';
  static const String androidEmulatorUrl = 'http://10.0.2.2:8000/api/v1';
  static const String iosSimulatorUrl = 'http://localhost:8000/api/v1';

  // Platform'a göre URL seçimi
  static String get backendUrl {
    // TODO: Platform detection eklenebilir
    return androidEmulatorUrl; // Şimdilik Android emulator için
  }

  final Dio _dio = Dio();

  ApiService() {
    _dio.options.baseUrl = backendUrl;
    _dio.options.connectTimeout = const Duration(seconds: 15);
    _dio.options.receiveTimeout = const Duration(seconds: 30);

    // Interceptor ekle - hata yönetimi için
    _dio.interceptors.add(
      InterceptorsWrapper(
        onError: (error, handler) {
          print('API Error: ${error.message}');
          print('Status Code: ${error.response?.statusCode}');
          print('Response Data: ${error.response?.data}');
          handler.next(error);
        },
        onRequest: (options, handler) {
          print('API Request: ${options.method} ${options.path}');
          print('Request Data: ${options.data}');
          handler.next(options);
        },
        onResponse: (response, handler) {
          print('API Response: ${response.statusCode}');
          print('Response Data: ${response.data}');
          handler.next(response);
        },
      ),
    );
  }

  // Mock data for testing when backend is not available
  Map<String, dynamic> _getMockMindMapData(String userInput) {
    return {
      "success": true,
      "mind_map": {
        "central_topic": "Adana Üniversite Hazırlığı",
        "main_categories": [
          {
            "name": "Akademik Malzemeler",
            "items": ["laptop", "çanta", "defter", "kalem"],
            "priority": "high",
            "products": [
              {
                "name": "Lenovo ThinkPad E15",
                "price": 15999.99,
                "platform": "Trendyol",
                "rating": 4.5,
                "url": "https://trendyol.com/laptop-1",
              },
            ]
          },
          {
            "name": "Kış Hazırlığı",
            "items": ["mont", "bot", "atkı", "eldiven"],
            "priority": "high",
            "products": [
              {
                "name": "Columbia Mont",
                "price": 899.99,
                "platform": "Hepsiburada",
                "rating": 4.3,
                "url": "https://hepsiburada.com/mont-1",
              },
            ]
          },
          {
            "name": "Ev Eşyaları",
            "items": ["yatak", "masa", "dolap", "lamba"],
            "priority": "medium",
            "products": [],
          }
        ],
        "user_input": userInput,
        "generated_at": DateTime.now().toIso8601String(),
      },
      "workflow_id": "mock_workflow_${DateTime.now().millisecondsSinceEpoch}",
    };
  }

  // Health Check
  Future<bool> checkHealth() async {
    try {
      final response = await _dio.get('/health');
      return response.statusCode == 200;
    } catch (e) {
      print('Health check failed: $e');
      return false;
    }
  }

  // Test Connection
  Future<Map<String, dynamic>> testConnection() async {
    try {
      final response = await _dio.get('/test');
      return response.data;
    } catch (e) {
      print('Test connection failed: $e');
      return {
        "message": "Backend bağlantısı başarısız!",
        "status": "disconnected",
        "error": e.toString(),
        "timestamp": DateTime.now().toIso8601String(),
      };
    }
  }

  // System Status
  Future<Map<String, dynamic>> getSystemStatus() async {
    try {
      final response = await _dio.get('/system/status');
      return response.data;
    } catch (e) {
      print('System status failed: $e');
      return {
        "api_status": "unavailable",
        "ai_service": "unavailable",
        "langgraph": "unavailable",
        "timestamp": DateTime.now().toIso8601String(),
        "error": e.toString(),
      };
    }
  }

  // Mind Map Generation
  Future<Map<String, dynamic>> generateMindMap({
    required String userInput,
    Map<String, dynamic>? userPreferences,
  }) async {
    try {
      print('🔄 AI Mind Map isteği gönderiliyor...');
      print('📝 User Input: $userInput');
      
      final response = await _dio.post(
        '/ai/generate-mindmap',
        data: {
          'user_input': userInput,
          'user_preferences': userPreferences ?? {},
        },
      );

      print('✅ AI Mind Map yanıtı alındı!');
      print('📊 Response Data: ${response.data}');
      
      return response.data;
    } catch (e) {
      print('❌ Backend connection failed, using mock data: $e');
      // Backend çalışmıyorsa mock veri döndür
      await Future.delayed(const Duration(seconds: 2)); // Gerçekçi gecikme
      return _getMockMindMapData(userInput);
    }
  }

  // Workflow Execution
  Future<Map<String, dynamic>> executeWorkflow({
    required Map<String, dynamic> inputData,
    required String workflowType,
    String? userId,
  }) async {
    try {
      final response = await _dio.post(
        '/workflow/execute',
        data: {
          'input_data': inputData,
          'workflow_type': workflowType,
          'user_id': userId,
        },
      );

      return response.data;
    } catch (e) {
      print('Workflow execution failed: $e');
      rethrow;
    }
  }

  // Product Search
  Future<Map<String, dynamic>> searchProducts({
    required String query,
    String? category,
    int limit = 10,
  }) async {
    try {
      final response = await _dio.get(
        '/ecommerce/search',
        queryParameters: {
          'query': query,
          if (category != null) 'category': category,
          'limit': limit,
        },
      );

      return response.data;
    } catch (e) {
      print('Product search failed: $e');
      return {
        "success": false,
        "products": [],
        "query": query,
        "category": category,
        "error": e.toString(),
      };
    }
  }

  // Price Comparison
  Future<Map<String, dynamic>> comparePrices(String productName) async {
    try {
      final response = await _dio.get('/ecommerce/compare/$productName');
      return response.data;
    } catch (e) {
      print('Price comparison failed: $e');
      return {
        "success": false,
        "comparison": {},
        "product_name": productName,
        "error": e.toString(),
      };
    }
  }

  // Stock Check
  Future<Map<String, dynamic>> checkStock(String productId) async {
    try {
      final response = await _dio.get('/ecommerce/stock/$productId');
      return response.data;
    } catch (e) {
      print('Stock check failed: $e');
      return {
        "success": false,
        "stock_info": {
          "in_stock": false,
          "quantity": 0,
          "last_updated": DateTime.now().toIso8601String(),
        },
        "error": e.toString(),
      };
    }
  }

  // Product Recommendations
  Future<Map<String, dynamic>> getRecommendations({
    required String category,
    double? budget,
    double? rating,
  }) async {
    try {
      final response = await _dio.get(
        '/ecommerce/recommendations/$category',
        queryParameters: {
          if (budget != null) 'budget': budget,
          if (rating != null) 'rating': rating,
        },
      );

      return response.data;
    } catch (e) {
      print('Recommendations failed: $e');
      return {
        "success": false,
        "recommendations": [],
        "category": category,
        "budget": budget,
        "error": e.toString(),
      };
    }
  }

  // Chat Message
  Future<Map<String, dynamic>> sendChatMessage({
    required String message,
    String? conversationId,
    Map<String, dynamic>? context,
  }) async {
    try {
      print('💬 Chat mesajı gönderiliyor...');
      print('📝 Message: $message');

      final response = await _dio.post(
        '/ai/chat',
        data: {
          'message': message,
          'conversation_id': conversationId,
          'context': context ?? {},
        },
      );

      print('✅ Chat yanıtı alındı!');
      print('📊 Response Data: ${response.data}');
      
      return response.data;
    } catch (e) {
      print('❌ Chat failed, using mock response: $e');
      // Backend çalışmıyorsa mock yanıt döndür
      await Future.delayed(const Duration(seconds: 1)); // Gerçekçi gecikme
      return _getMockChatResponse(message);
    }
  }

  // Mock chat response
  Map<String, dynamic> _getMockChatResponse(String message) {
    final messageLower = message.toLowerCase();

    // Basit keyword-based yanıtlar
    if (messageLower.contains('laptop') ||
        messageLower.contains('bilgisayar')) {
      return {
        "success": true,
        "response":
            "Laptop seçiminde size yardımcı olabilirim! Hangi özellikler önemli sizin için? Bütçeniz nedir?",
        "conversation_id": "mock_conv_${DateTime.now().millisecondsSinceEpoch}",
        "timestamp": DateTime.now().toIso8601String(),
        "context": {"last_topic": "laptop"},
      };
    } else if (messageLower.contains('fiyat') ||
        messageLower.contains('pahalı')) {
      return {
        "success": true,
        "response":
            "Fiyat konusunda size en iyi seçenekleri sunabilirim. Hangi kategoride arama yapmak istiyorsunuz?",
        "conversation_id": "mock_conv_${DateTime.now().millisecondsSinceEpoch}",
        "timestamp": DateTime.now().toIso8601String(),
        "context": {"last_topic": "price"},
      };
    } else if (messageLower.contains('öneri') ||
        messageLower.contains('tavsiye')) {
      return {
        "success": true,
        "response":
            "Size kişiselleştirilmiş öneriler sunabilirim! Hangi kategoride ürün arıyorsunuz?",
        "conversation_id": "mock_conv_${DateTime.now().millisecondsSinceEpoch}",
        "timestamp": DateTime.now().toIso8601String(),
        "context": {"last_topic": "recommendations"},
      };
    } else {
      return {
        "success": true,
        "response":
            "Alışveriş konusunda size nasıl yardımcı olabilirim? Hangi ürün veya kategori hakkında bilgi almak istiyorsunuz?",
        "conversation_id": "mock_conv_${DateTime.now().millisecondsSinceEpoch}",
        "timestamp": DateTime.now().toIso8601String(),
        "context": {"last_topic": "general"},
      };
    }
  }
}

// API Response Models
class MindMapResponse {
  final Map<String, dynamic> mindMap;
  final Map<String, dynamic>? contextAnalysis;
  final String? workflowId;

  MindMapResponse({
    required this.mindMap,
    this.contextAnalysis,
    this.workflowId,
  });

  factory MindMapResponse.fromJson(Map<String, dynamic> json) {
    return MindMapResponse(
      mindMap: json['mind_map'] ?? {},
      contextAnalysis: json['context_analysis'],
      workflowId: json['workflow_id'],
    );
  }
}

class ProductResponse {
  final List<Map<String, dynamic>> products;
  final int totalCount;
  final bool success;

  ProductResponse({
    required this.products,
    required this.totalCount,
    required this.success,
  });

  factory ProductResponse.fromJson(Map<String, dynamic> json) {
    return ProductResponse(
      products: List<Map<String, dynamic>>.from(json['products'] ?? []),
      totalCount: json['total_count'] ?? 0,
      success: json['success'] ?? false,
    );
  }
}

class PriceComparisonResponse {
  final String productName;
  final Map<String, dynamic> comparison;
  final bool success;

  PriceComparisonResponse({
    required this.productName,
    required this.comparison,
    required this.success,
  });

  factory PriceComparisonResponse.fromJson(Map<String, dynamic> json) {
    return PriceComparisonResponse(
      productName: json['product_name'] ?? '',
      comparison: json['comparison'] ?? {},
      success: json['success'] ?? false,
    );
  }
}
