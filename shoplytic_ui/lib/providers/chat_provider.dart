import 'package:flutter/foundation.dart';

import '../services/api_service.dart';

class ChatMessage {
  final String id;
  final String message;
  final String response;
  final bool isUser;
  final DateTime timestamp;
  final Map<String, dynamic>? context;

  ChatMessage({
    required this.id,
    required this.message,
    required this.response,
    required this.isUser,
    required this.timestamp,
    this.context,
  });

  factory ChatMessage.fromJson(Map<String, dynamic> json) {
    return ChatMessage(
      id: json['id'] ?? '',
      message: json['message'] ?? '',
      response: json['response'] ?? '',
      isUser: json['is_user'] ?? false,
      timestamp: DateTime.parse(
        json['timestamp'] ?? DateTime.now().toIso8601String(),
      ),
      context: json['context'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'message': message,
      'response': response,
      'is_user': isUser,
      'timestamp': timestamp.toIso8601String(),
      'context': context,
    };
  }
}

class ChatProvider with ChangeNotifier {
  final ApiService _apiService = ApiService();

  List<ChatMessage> _messages = [];
  bool _isLoading = false;
  String? _error;
  String? _conversationId;
  Map<String, dynamic> _context = {};

  // Getters
  List<ChatMessage> get messages => _messages;
  bool get isLoading => _isLoading;
  String? get error => _error;
  String? get conversationId => _conversationId;

  // Chat mesajı gönder
  Future<void> sendMessage(String message) async {
    if (message.trim().isEmpty) return;

    // Kullanıcı mesajını ekle
    final userMessage = ChatMessage(
      id: DateTime.now().millisecondsSinceEpoch.toString(),
      message: message,
      response: '',
      isUser: true,
      timestamp: DateTime.now(),
    );

    _messages.add(userMessage);
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      // API'ye mesaj gönder
      final response = await _apiService.sendChatMessage(
        message: message,
        conversationId: _conversationId,
        context: _context,
      );

      if (response['success'] == true) {
        // AI yanıtını ekle
        final aiMessage = ChatMessage(
          id: DateTime.now().millisecondsSinceEpoch.toString(),
          message: '',
          response: response['response'] ?? 'Üzgünüm, yanıt veremiyorum.',
          isUser: false,
          timestamp: DateTime.now(),
          context: response['context'],
        );

        _messages.add(aiMessage);

        // Context'i güncelle
        if (response['context'] != null) {
          _context = response['context'];
        }

        // Conversation ID'yi güncelle
        if (response['conversation_id'] != null) {
          _conversationId = response['conversation_id'];
        }
      } else {
        _error = response['error'] ?? 'Mesaj gönderilemedi';
      }
    } catch (e) {
      _error = 'Bağlantı hatası: $e';
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  // Sohbeti temizle
  void clearChat() {
    _messages.clear();
    _conversationId = null;
    _context = {};
    _error = null;
    notifyListeners();
  }

  // Hata mesajını temizle
  void clearError() {
    _error = null;
    notifyListeners();
  }

  // Mock mesajlar ekle (test için)
  void addMockMessages() {
    _messages = [
      ChatMessage(
        id: '1',
        message: '',
        response:
            'Merhaba! Alışveriş konusunda size nasıl yardımcı olabilirim?',
        isUser: false,
        timestamp: DateTime.now().subtract(Duration(minutes: 5)),
      ),
      ChatMessage(
        id: '2',
        message: 'Laptop almak istiyorum',
        response: '',
        isUser: true,
        timestamp: DateTime.now().subtract(Duration(minutes: 4)),
      ),
      ChatMessage(
        id: '3',
        message: '',
        response:
            'Harika! Laptop seçiminde size yardımcı olabilirim. Hangi özellikler önemli sizin için? Bütçeniz nedir?',
        isUser: false,
        timestamp: DateTime.now().subtract(Duration(minutes: 3)),
      ),
    ];
    notifyListeners();
  }
}
