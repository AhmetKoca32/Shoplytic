import 'package:flutter/material.dart';

class HomeProvider with ChangeNotifier {
  // Example state
  int _selectedTab = 0;

  int get selectedTab => _selectedTab;

  void setTab(int index) {
    _selectedTab = index;
    notifyListeners();
  }
}
