import 'package:flutter/foundation.dart';

class MindMapProvider extends ChangeNotifier {
  Map<String, dynamic>? _mindMapData;
  bool _isLoading = false;
  String? _error;

  Map<String, dynamic>? get mindMapData => _mindMapData;
  bool get isLoading => _isLoading;
  String? get error => _error;

  Future<void> generateMindMap(String userInput) async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      // TODO: Connect to API service
      // For now, use mock data
      await Future.delayed(const Duration(seconds: 2));

      _mindMapData = {
        'central_topic': userInput,
        'user_summary': 'Kullanıcının durumu: $userInput',
        'main_categories': [
          {
            'name': 'Temel İhtiyaçlar',
            'emoji': '📦',
            'items': ['Genel alışveriş listesi'],
            'priority': 'high',
            'estimated_budget': '5000-10000 TL',
          },
          {
            'name': 'Teknoloji',
            'emoji': '💻',
            'items': ['Laptop', 'Telefon'],
            'priority': 'high',
            'estimated_budget': '15000-30000 TL',
          },
          {
            'name': 'Giyim',
            'emoji': '👕',
            'items': ['Mevsimlik kıyafetler'],
            'priority': 'medium',
            'estimated_budget': '3000-7000 TL',
          },
        ],
        'total_estimated_budget': '23000-47000 TL',
      };
    } catch (e) {
      _error = e.toString();
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  void clear() {
    _mindMapData = null;
    _error = null;
    notifyListeners();
  }
}
