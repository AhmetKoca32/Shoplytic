import 'package:dio/dio.dart';

class ApiService {
  static const String baseUrl = 'http://localhost:8000/api/v1';
  static const String backendUrl =
      'http://10.0.2.2:8000/api/v1'; // Android emulator için

  final Dio _dio = Dio();

  ApiService() {
    _dio.options.baseUrl = baseUrl;
    _dio.options.connectTimeout = const Duration(seconds: 10);
    _dio.options.receiveTimeout = const Duration(seconds: 10);
  }

  // Mock data for testing when backend is not available
  Map<String, dynamic> _getMockMindMapData(String userInput) {
    return {
      "mind_map": {
        "categories": [
          {
            "name": "Ev Eşyaları",
            "priority": 1,
            "products": [
              "Yatak",
              "Çalışma Masası",
              "Mutfak Gereçleri",
              "Dolap",
            ],
          },
          {
            "name": "Teknoloji",
            "priority": 2,
            "products": ["Laptop", "Tablet", "Kulaklık", "Telefon"],
          },
          {
            "name": "Kıyafet",
            "priority": 3,
            "products": ["Günlük Kıyafetler", "Spor Kıyafetleri", "Ayakkabı"],
          },
          {
            "name": "Kitap & Kırtasiye",
            "priority": 4,
            "products": ["Ders Kitapları", "Defter", "Kalem", "Çanta"],
          },
        ],
        "user_input": userInput,
        "generated_at": DateTime.now().toIso8601String(),
      },
    };
  }

  // Health Check
  Future<bool> checkHealth() async {
    try {
      final response = await _dio.get('/system/health');
      return response.statusCode == 200;
    } catch (e) {
      print('Health check failed: $e');
      return false;
    }
  }

  // Mind Map Generation
  Future<Map<String, dynamic>> generateMindMap({
    required String userInput,
    required String userId,
  }) async {
    try {
      // Önce backend'e bağlanmayı dene
      final response = await _dio.post(
        '/ai/generate-mindmap',
        data: {'user_input': userInput, 'user_id': userId},
      );

      return response.data;
    } catch (e) {
      print('Backend connection failed, using mock data: $e');
      // Backend çalışmıyorsa mock veri döndür
      await Future.delayed(const Duration(seconds: 1)); // Gerçekçi gecikme
      return _getMockMindMapData(userInput);
    }
  }

  // Workflow Execution
  Future<Map<String, dynamic>> executeWorkflow({
    required String workflowType,
    required String userInput,
    required String userId,
  }) async {
    try {
      final response = await _dio.post(
        '/workflow/execute',
        data: {
          'workflow_type': workflowType,
          'user_input': userInput,
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
      rethrow;
    }
  }

  // Price Comparison
  Future<Map<String, dynamic>> comparePrices(String productName) async {
    try {
      final response = await _dio.get('/ecommerce/compare/$productName');
      return response.data;
    } catch (e) {
      print('Price comparison failed: $e');
      rethrow;
    }
  }

  // Stock Check
  Future<Map<String, dynamic>> checkStock(String productId) async {
    try {
      final response = await _dio.get('/ecommerce/stock/$productId');
      return response.data;
    } catch (e) {
      print('Stock check failed: $e');
      rethrow;
    }
  }

  // Product Recommendations
  Future<Map<String, dynamic>> getRecommendations({
    required String category,
    int? budget,
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
      rethrow;
    }
  }

  // System Status
  Future<Map<String, dynamic>> getSystemStatus() async {
    try {
      final response = await _dio.get('/system/status');
      return response.data;
    } catch (e) {
      print('System status failed: $e');
      rethrow;
    }
  }
}

// API Response Models
class MindMapResponse {
  final Map<String, dynamic> mindMap;
  final Map<String, dynamic>? contextAnalysis;

  MindMapResponse({required this.mindMap, this.contextAnalysis});

  factory MindMapResponse.fromJson(Map<String, dynamic> json) {
    return MindMapResponse(
      mindMap: json['mind_map'] ?? {},
      contextAnalysis: json['context_analysis'],
    );
  }
}

class ProductResponse {
  final List<Map<String, dynamic>> products;
  final int totalCount;

  ProductResponse({required this.products, required this.totalCount});

  factory ProductResponse.fromJson(Map<String, dynamic> json) {
    return ProductResponse(
      products: List<Map<String, dynamic>>.from(json['products'] ?? []),
      totalCount: json['total_count'] ?? 0,
    );
  }
}

class PriceComparisonResponse {
  final String productName;
  final Map<String, dynamic> comparison;

  PriceComparisonResponse({
    required this.productName,
    required this.comparison,
  });

  factory PriceComparisonResponse.fromJson(Map<String, dynamic> json) {
    return PriceComparisonResponse(
      productName: json['product_name'] ?? '',
      comparison: json['comparison'] ?? {},
    );
  }
}
