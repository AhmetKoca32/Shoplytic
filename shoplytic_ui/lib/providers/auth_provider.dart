import 'package:flutter/material.dart';

class AuthProvider with ChangeNotifier {
  // Example state
  String? _userEmail;
  bool _isLoggedIn = false;

  String? get userEmail => _userEmail;
  bool get isLoggedIn => _isLoggedIn;

  void login(String email) {
    _userEmail = email;
    _isLoggedIn = true;
    notifyListeners();
  }

  void logout() {
    _userEmail = null;
    _isLoggedIn = false;
    notifyListeners();
  }
}
