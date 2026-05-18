import 'package:flutter/foundation.dart';

class LegalProvider extends ChangeNotifier {
  Map<String, dynamic>? _analysisResult;
  bool _isLoading = false;

  Map<String, dynamic>? get analysisResult => _analysisResult;
  bool get isLoading => _isLoading;

  Future<void> analyzeComplaint(String complaint) async {
    _isLoading = true;
    _analysisResult = null;
    notifyListeners();

    try {
      // TODO: Connect to API service
      await Future.delayed(const Duration(seconds: 2));

      _analysisResult = {
        'complaint_summary': complaint,
        'violated_articles': [
          {
            'article': 'Madde 4',
            'title': 'Ayıplı Mal',
            'content': 'Satıcı, ayıplı maldan sorumludur.',
            'relevance': 0.85,
          },
        ],
        'consumer_rights': [
          'Malın iadesini talep etme',
          'Bedelin iadesini isteme',
        ],
        'authorities_to_apply': [
          'Tüketici Hakem Heyeti',
          'Ticaret Bakanlığı',
        ],
        'recommended_actions': [
          'Satıcıya yazılı başvuru yapın',
          'Tüketici Hakem Heyeti\'ne başvurun',
        ],
      };
    } catch (e) {
      debugPrint('Legal analysis error: $e');
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  void clear() {
    _analysisResult = null;
    notifyListeners();
  }
}
