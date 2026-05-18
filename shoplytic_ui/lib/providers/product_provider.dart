import 'package:flutter/foundation.dart';

class ProductItem {
  final String id;
  final String name;
  final double price;
  final String platform;
  final double rating;
  final int reviewCount;
  final bool isFavorite;

  ProductItem({
    required this.id,
    required this.name,
    required this.price,
    required this.platform,
    this.rating = 4.0,
    this.reviewCount = 0,
    this.isFavorite = false,
  });
}

class ProductProvider extends ChangeNotifier {
  final List<ProductItem> _products = [];
  final List<ProductItem> _favorites = [];
  bool _isLoading = false;

  List<ProductItem> get products => List.unmodifiable(_products);
  List<ProductItem> get favorites => List.unmodifiable(_favorites);
  bool get isLoading => _isLoading;

  Future<void> searchProducts({
    required String query,
    String category = '',
    double budget = 0,
  }) async {
    _isLoading = true;
    notifyListeners();

    try {
      // TODO: Connect to API service
      await Future.delayed(const Duration(seconds: 1));

      // Mock products will be added when API is connected
    } catch (e) {
      debugPrint('Product search error: $e');
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  void toggleFavorite(ProductItem product) {
    if (_favorites.any((p) => p.id == product.id)) {
      _favorites.removeWhere((p) => p.id == product.id);
    } else {
      _favorites.add(product);
    }
    notifyListeners();
  }

  void clear() {
    _products.clear();
    notifyListeners();
  }
}
