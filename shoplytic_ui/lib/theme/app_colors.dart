import 'package:flutter/material.dart';

/// Shoplytic Design System — Color Palette
///
/// Defined from shoplytic_color_system.html
class AppColors {
  AppColors._();

  // ────────────────────────────────────────────────────────────────────────────
  // Ana Renkler (Primary)
  // ────────────────────────────────────────────────────────────────────────────

  /// Butonlar, AppBar, aktif tab, progress indicator
  static const Color deepTeal = Color(0xFF0D7A5F);

  /// Buton gradient, aktif durumlar
  static const Color emerald = Color(0xFF1BB68A);

  /// Aktif input, toggle active
  static const Color mintActive = Color(0xFF3ECFA3);

  /// Light tema kart yüzeyi, soft background
  static const Color mintSurface = Color(0xFFD4F5EC);

  // ────────────────────────────────────────────────────────────────────────────
  // Vurgu Rengi (Accent)
  // ────────────────────────────────────────────────────────────────────────────

  /// Fiyat etiketi, rating yıldızı, CTA vurgusu
  static const Color amberGold = Color(0xFFE8A020);

  /// Hover, soft accent
  static const Color amberLight = Color(0xFFF5C35A);

  /// Light tema soft vurgu zemini
  static const Color amberSurface = Color(0xFFFFF3D4);

  // ────────────────────────────────────────────────────────────────────────────
  // Nötr / Zemin
  // ────────────────────────────────────────────────────────────────────────────

  /// Scaffold arka plan (dark)
  static const Color darkNavy = Color(0xFF0A0F1E);

  /// Kartlar, surface (dark)
  static const Color surfaceDark = Color(0xFF141B2D);

  /// Scaffold arka plan (light)
  static const Color offWhite = Color(0xFFF8FAF9);

  /// Kart arka planı (dark mode card)
  static const Color cardDark = Color(0xFF1C2B27);

  // ────────────────────────────────────────────────────────────────────────────
  // Agent Renkleri
  // ────────────────────────────────────────────────────────────────────────────

  /// Context analiz agent'ı
  static const Color contextAgent = Color(0xFF1BB68A);

  /// Zihin haritası agent'ı — mind map node'ları, dallar
  static const Color mindMapAgent = Color(0xFF5C7CFA);

  /// Ürün agent'ı — ürün kartları, fiyat
  static const Color productAgent = Color(0xFFE8A020);

  /// Hukuk agent'ı — hukuki uyarı, tüketici hakları
  static const Color legalAgent = Color(0xFFE5533D);

  // ────────────────────────────────────────────────────────────────────────────
  // Text
  // ────────────────────────────────────────────────────────────────────────────

  static const Color textPrimary = Color(0xFFFFFFFF);
  static const Color textSecondary = Color(0xB3FFFFFF);
  static const Color textTertiary = Color(0x77FFFFFF);

  // ────────────────────────────────────────────────────────────────────────────
  // Semantic
  // ────────────────────────────────────────────────────────────────────────────

  static const Color error = Color(0xFFE5533D);
  static const Color success = Color(0xFF1BB68A);
  static const Color warning = Color(0xFFE8A020);

  // ────────────────────────────────────────────────────────────────────────────
  // Glass / Overlay
  // ────────────────────────────────────────────────────────────────────────────

  static Color get glassLight => Colors.white.withValues(alpha: 0.06);
  static Color get glassMedium => Colors.white.withValues(alpha: 0.10);
  static Color get glassHeavy => Colors.white.withValues(alpha: 0.16);
  static Color get glassBorder => Colors.white.withValues(alpha: 0.12);
  static Color get glassBorderActive => Colors.white.withValues(alpha: 0.25);

  // ────────────────────────────────────────────────────────────────────────────
  // Gradients
  // ────────────────────────────────────────────────────────────────────────────

  /// Ana buton gradienti: Deep Teal → Emerald
  static const Gradient primaryGradient = LinearGradient(
    colors: [deepTeal, emerald],
    begin: Alignment.centerLeft,
    end: Alignment.centerRight,
  );

  /// Dark tema arka plan gradienti
  static const Gradient backgroundDark = LinearGradient(
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
    colors: [darkNavy, surfaceDark, Color(0xFF1A2540)],
    stops: [0.0, 0.5, 1.0],
  );

  /// Glass kart gradienti
  static Gradient get glassGradient => LinearGradient(
        colors: [
          Colors.white.withValues(alpha: 0.08),
          Colors.white.withValues(alpha: 0.03),
        ],
        begin: Alignment.topLeft,
        end: Alignment.bottomRight,
      );

  // ────────────────────────────────────────────────────────────────────────────
  // Shadows
  // ────────────────────────────────────────────────────────────────────────────

  static List<BoxShadow> get glassShadow => [
        BoxShadow(
          color: Colors.black.withValues(alpha: 0.25),
          blurRadius: 24,
          offset: const Offset(0, 8),
        ),
      ];

  static List<BoxShadow> get primaryGlow => [
        BoxShadow(
          color: deepTeal.withValues(alpha: 0.35),
          blurRadius: 20,
          offset: const Offset(0, 8),
        ),
      ];

  static List<BoxShadow> get navbarShadow => [
        BoxShadow(
          color: Colors.black.withValues(alpha: 0.35),
          blurRadius: 32,
          offset: const Offset(0, 12),
        ),
        BoxShadow(
          color: deepTeal.withValues(alpha: 0.10),
          blurRadius: 60,
          offset: Offset.zero,
        ),
      ];
}
