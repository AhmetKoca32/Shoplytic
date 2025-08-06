import 'package:flutter/material.dart';

import '../services/api_service.dart';

class MindMapNode {
  final String title;
  final List<MindMapNode> children;
  final String? category;
  final int? priority;
  final List<String>? products;

  MindMapNode(
    this.title, {
    this.children = const [],
    this.category,
    this.priority,
    this.products,
  });
}

class MindMapProvider with ChangeNotifier {
  late MindMapNode _root;
  bool _isLoading = false;
  String? _error;
  final ApiService _apiService = ApiService();

  MindMapNode get root => _root;
  bool get isLoading => _isLoading;
  String? get error => _error;

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
  Future<void> generateMindMap(String userInput, String userId) async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      final response = await _apiService.generateMindMap(
        userInput: userInput,
        userId: userId,
      );

      final mindMapData = response['mind_map'];
      if (mindMapData != null && mindMapData['categories'] != null) {
        final categories = mindMapData['categories'] as List;
        final nodes = categories.map((category) {
          return MindMapNode(
            category['name'] ?? 'Kategori',
            category: category['name'],
            priority: category['priority'],
            products: category['products'] != null
                ? List<String>.from(category['products'])
                : null,
          );
        }).toList();

        _root = MindMapNode('Ana Fikir', children: nodes);
      }
    } catch (e) {
      _error = 'Zihin haritası oluşturulurken hata oluştu: $e';
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  // Workflow çalıştır
  Future<void> executeWorkflow(String userInput, String userId) async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      final response = await _apiService.executeWorkflow(
        workflowType: 'mind_map_generation',
        userInput: userInput,
        userId: userId,
      );

      if (response['result'] != null &&
          response['result']['mind_map'] != null) {
        final mindMapData = response['result']['mind_map'];
        if (mindMapData['categories'] != null) {
          final categories = mindMapData['categories'] as List;
          final nodes = categories.map((category) {
            return MindMapNode(
              category['name'] ?? 'Kategori',
              category: category['name'],
              priority: category['priority'],
              products: category['products'] != null
                  ? List<String>.from(category['products'])
                  : null,
            );
          }).toList();

          _root = MindMapNode('Ana Fikir', children: nodes);
        }
      }
    } catch (e) {
      _error = 'Workflow çalıştırılırken hata oluştu: $e';
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  void clearError() {
    _error = null;
    notifyListeners();
  }
}
