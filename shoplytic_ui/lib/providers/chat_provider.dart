import 'package:flutter/foundation.dart';

class ChatMessage {
  final String role; // 'user' or 'ai'
  final String content;
  final DateTime timestamp;

  ChatMessage({
    required this.role,
    required this.content,
    DateTime? timestamp,
  }) : timestamp = timestamp ?? DateTime.now();
}

class ChatProvider extends ChangeNotifier {
  final List<ChatMessage> _messages = [];
  bool _isLoading = false;

  List<ChatMessage> get messages => List.unmodifiable(_messages);
  bool get isLoading => _isLoading;

  void addMessage(String role, String content) {
    _messages.add(ChatMessage(role: role, content: content));
    notifyListeners();
  }

  Future<void> sendMessage(String text) async {
    _isLoading = true;
    addMessage('user', text);
    notifyListeners();

    try {
      // TODO: Connect to API service
      await Future.delayed(const Duration(seconds: 1));

      addMessage(
        'ai',
        'Analiz ediliyor... İsteğinizi işleme aldım. Şu an mock yanıt modundayım. Backend bağlandığında gerçek AI ile konuşabileceksiniz.',
      );
    } catch (e) {
      addMessage('ai', 'Bir hata oluştu. Lütfen tekrar deneyin.');
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  void clear() {
    _messages.clear();
    notifyListeners();
  }
}
