import 'package:flutter/material.dart';

class MindMapNode {
  final String title;
  final List<MindMapNode> children;
  final String? category;
  MindMapNode(this.title, {this.children = const [], this.category});
}

class MindMapProvider with ChangeNotifier {
  late MindMapNode _root;

  MindMapNode get root => _root;

  MindMapProvider() {
    // Başlangıçta boş harita
    _root = MindMapNode('Ana Fikir', children: []);
  }

  void setMap(MindMapNode root) {
    _root = root;
    notifyListeners();
  }

  void addNode(MindMapNode parent, String title) {
    parent.children.add(MindMapNode(title));
    notifyListeners();
  }
}
