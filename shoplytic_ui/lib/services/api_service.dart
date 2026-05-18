import 'package:dio/dio.dart';

class ApiService {
  static const String _baseUrl = 'http://localhost:8000';
  late final Dio _dio;

  ApiService() {
    _dio = Dio(
      BaseOptions(
        baseUrl: _baseUrl,
        connectTimeout: const Duration(seconds: 10),
        receiveTimeout: const Duration(seconds: 30),
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
      ),
    );
  }

  // ── Health ──────────────────────────────────────────────────────────────────

  Future<Map<String, dynamic>> healthCheck() async {
    try {
      final response = await _dio.get('/health');
      return response.data;
    } catch (e) {
      return {'status': 'offline', 'service': 'Shoplytic'};
    }
  }

  Future<Map<String, dynamic>> systemStatus() async {
    try {
      final response = await _dio.get('/api/v1/system/status');
      return response.data;
    } catch (e) {
      return {'status': 'offline', 'version': '1.0.0'};
    }
  }

  // ── AI - Mind Map ───────────────────────────────────────────────────────────

  Future<Map<String, dynamic>> generateMindMap({
    required String userInput,
    String threadId = 'default',
  }) async {
    try {
      final response = await _dio.post(
        '/api/v1/ai/generate-mindmap',
        data: {
          'user_input': userInput,
          'thread_id': threadId,
        },
      );
      return response.data;
    } catch (e) {
      throw Exception('Failed to generate mind map: $e');
    }
  }

  // ── AI - Chat ──────────────────────────────────────────────────────────────

  Future<Map<String, dynamic>> sendChatMessage({
    required String message,
    String threadId = 'default',
    String? nodeContext,
  }) async {
    try {
      final data = <String, dynamic>{
        'message': message,
        'thread_id': threadId,
      };
      if (nodeContext != null) {
        data['node_context'] = nodeContext;
      }
      final response = await _dio.post(
        '/api/v1/ai/chat',
        data: data,
      );
      return response.data;
    } catch (e) {
      throw Exception('Failed to send message: $e');
    }
  }

  // ── E-Commerce ─────────────────────────────────────────────────────────────

  Future<Map<String, dynamic>> searchProducts({
    String query = '',
    String category = '',
    double budget = 0,
  }) async {
    try {
      final response = await _dio.get(
        '/api/v1/ecommerce/search',
        queryParameters: {
          'q': query,
          if (category.isNotEmpty) 'category': category,
          if (budget > 0) 'budget': budget.toString(),
        },
      );
      return response.data;
    } catch (e) {
      throw Exception('Failed to search products: $e');
    }
  }

  Future<Map<String, dynamic>> comparePrices(String productName) async {
    try {
      final response = await _dio.get('/api/v1/ecommerce/compare/$productName');
      return response.data;
    } catch (e) {
      throw Exception('Failed to compare prices: $e');
    }
  }

  Future<Map<String, dynamic>> getStock(String productId) async {
    try {
      final response = await _dio.get('/api/v1/ecommerce/stock/$productId');
      return response.data;
    } catch (e) {
      throw Exception('Failed to get stock: $e');
    }
  }

  // ── Legal ───────────────────────────────────────────────────────────────────

  Future<Map<String, dynamic>> analyzeComplaint(String complaint) async {
    try {
      final response = await _dio.post(
        '/api/v1/legal/analyze',
        data: {'complaint': complaint},
      );
      return response.data;
    } catch (e) {
      throw Exception('Failed to analyze complaint: $e');
    }
  }

  Future<Map<String, dynamic>> generatePetition({
    required String complaint,
    required String violatedLaw,
    required String demand,
  }) async {
    try {
      final response = await _dio.post(
        '/api/v1/legal/petition',
        data: {
          'complaint': complaint,
          'violated_law': violatedLaw,
          'demand': demand,
        },
      );
      return response.data;
    } catch (e) {
      throw Exception('Failed to generate petition: $e');
    }
  }
}
