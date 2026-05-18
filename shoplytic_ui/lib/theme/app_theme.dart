import 'package:flutter/material.dart';
import 'app_colors.dart';

class AppTheme {
  AppTheme._();

  // ────────────────────────────────────────────────────────────────────────────
  // Font Ailesi Dağılımı (font.md)
  //   Montserrat    → Başlıklar, CTA butonları (vitrin)
  //   Inter         → Gövde metni, içerik, sohbet, kartlar (okunabilirlik)
  //   JetBrainsMono → Teknik veri, log, hukuki atıf (mühendislik)
  // ────────────────────────────────────────────────────────────────────────────

  static const String _headingFamily = 'Montserrat';
  static const String _bodyFamily = 'Inter';
  // JetBrainsMono — inline kullanım için (log, OCR, hukuk) — ekran bazında eklenecek

  // ────────────────────────────────────────────────────────────────────────────
  // Dark Theme
  // ────────────────────────────────────────────────────────────────────────────

  static ThemeData get dark => ThemeData(
        brightness: Brightness.dark,
        scaffoldBackgroundColor: AppColors.darkNavy,
        colorScheme: const ColorScheme.dark(
          primary: AppColors.deepTeal,
          secondary: AppColors.amberGold,
          surface: AppColors.surfaceDark,
          error: AppColors.error,
        ),
        useMaterial3: true,
        fontFamily: _bodyFamily,
        textTheme: _darkTextTheme,
        appBarTheme: const AppBarTheme(
          backgroundColor: Colors.transparent,
          elevation: 0,
          centerTitle: false,
          titleTextStyle: TextStyle(
            fontFamily: _headingFamily,
            fontSize: 20,
            fontWeight: FontWeight.w700,
            color: AppColors.textPrimary,
          ),
        ),
        elevatedButtonTheme: ElevatedButtonThemeData(
          style: ElevatedButton.styleFrom(
            backgroundColor: AppColors.deepTeal,
            foregroundColor: Colors.white,
            elevation: 0,
            padding: const EdgeInsets.symmetric(vertical: 18, horizontal: 32),
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(16),
            ),
            textStyle: const TextStyle(
              fontFamily: _headingFamily,
              fontSize: 16,
              fontWeight: FontWeight.w600,
            ),
          ).copyWith(
            overlayColor: WidgetStateProperty.resolveWith((states) {
              if (states.contains(WidgetState.pressed)) {
                return Colors.white.withValues(alpha: 0.15);
              }
              return null;
            }),
          ),
        ),
        inputDecorationTheme: InputDecorationTheme(
          filled: true,
          fillColor: AppColors.glassMedium,
          hintStyle: TextStyle(
            fontFamily: _bodyFamily,
            color: AppColors.textSecondary.withValues(alpha: 0.5),
            fontSize: 16,
            fontWeight: FontWeight.w400,
          ),
          border: OutlineInputBorder(
            borderRadius: BorderRadius.circular(16),
            borderSide: BorderSide.none,
          ),
          enabledBorder: OutlineInputBorder(
            borderRadius: BorderRadius.circular(16),
            borderSide: BorderSide(
              color: AppColors.glassBorder,
              width: 1,
            ),
          ),
          focusedBorder: OutlineInputBorder(
            borderRadius: BorderRadius.circular(16),
            borderSide: BorderSide(
              color: AppColors.deepTeal.withValues(alpha: 0.6),
              width: 1.5,
            ),
          ),
          contentPadding: const EdgeInsets.symmetric(
            horizontal: 20,
            vertical: 16,
          ),
        ),
        snackBarTheme: SnackBarThemeData(
          behavior: SnackBarBehavior.floating,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(14),
          ),
        ),
        dialogTheme: DialogThemeData(
          backgroundColor: AppColors.surfaceDark,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(24),
          ),
          titleTextStyle: const TextStyle(
            fontFamily: _headingFamily,
            fontSize: 20,
            fontWeight: FontWeight.w700,
            color: AppColors.textPrimary,
          ),
        ),
        chipTheme: ChipThemeData(
          backgroundColor: AppColors.glassMedium,
          labelStyle: const TextStyle(
            fontFamily: _bodyFamily,
            color: AppColors.textPrimary,
          ),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(10),
          ),
          side: BorderSide.none,
        ),
        dividerTheme: DividerThemeData(
          color: AppColors.glassBorder,
          thickness: 0.5,
        ),
      );

  // ────────────────────────────────────────────────────────────────────────────
  // Light Theme
  // ────────────────────────────────────────────────────────────────────────────

  static ThemeData get light => ThemeData(
        brightness: Brightness.light,
        scaffoldBackgroundColor: AppColors.offWhite,
        colorScheme: const ColorScheme.light(
          primary: AppColors.deepTeal,
          secondary: AppColors.amberGold,
          surface: Colors.white,
          error: AppColors.error,
        ),
        useMaterial3: true,
        fontFamily: _bodyFamily,
        textTheme: _lightTextTheme,
        appBarTheme: const AppBarTheme(
          backgroundColor: Colors.transparent,
          elevation: 0,
          centerTitle: false,
          titleTextStyle: TextStyle(
            fontFamily: _headingFamily,
            fontSize: 20,
            fontWeight: FontWeight.w700,
            color: AppColors.darkNavy,
          ),
        ),
        elevatedButtonTheme: ElevatedButtonThemeData(
          style: ElevatedButton.styleFrom(
            backgroundColor: AppColors.deepTeal,
            foregroundColor: Colors.white,
            elevation: 0,
            padding: const EdgeInsets.symmetric(vertical: 18, horizontal: 32),
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(16),
            ),
            textStyle: const TextStyle(
              fontFamily: _headingFamily,
              fontSize: 16,
              fontWeight: FontWeight.w600,
            ),
          ),
        ),
        inputDecorationTheme: InputDecorationTheme(
          filled: true,
          fillColor: AppColors.mintSurface.withValues(alpha: 0.5),
          hintStyle: TextStyle(
            fontFamily: _bodyFamily,
            color: AppColors.darkNavy.withValues(alpha: 0.4),
            fontSize: 16,
            fontWeight: FontWeight.w400,
          ),
          border: OutlineInputBorder(
            borderRadius: BorderRadius.circular(16),
            borderSide: BorderSide.none,
          ),
          enabledBorder: OutlineInputBorder(
            borderRadius: BorderRadius.circular(16),
            borderSide: BorderSide(
              color: AppColors.darkNavy.withValues(alpha: 0.1),
              width: 1,
            ),
          ),
          focusedBorder: OutlineInputBorder(
            borderRadius: BorderRadius.circular(16),
            borderSide: BorderSide(
              color: AppColors.deepTeal.withValues(alpha: 0.5),
              width: 1.5,
            ),
          ),
          contentPadding: const EdgeInsets.symmetric(
            horizontal: 20,
            vertical: 16,
          ),
        ),
        snackBarTheme: SnackBarThemeData(
          behavior: SnackBarBehavior.floating,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(14),
          ),
        ),
        dialogTheme: DialogThemeData(
          backgroundColor: Colors.white,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(24),
          ),
          titleTextStyle: const TextStyle(
            fontFamily: _headingFamily,
            fontSize: 20,
            fontWeight: FontWeight.w700,
            color: AppColors.darkNavy,
          ),
        ),
      );

  // ────────────────────────────────────────────────────────────────────────────
  // Text Themes — Dark
  //
  // Montserrat kullanımı: display (32sp w700 splash), headline (20sp w700 appbar),
  //   labelLarge (16sp w600 CTA)
  // Inter kullanımı: title (14sp w500 mindmap nodes, product name),
  //   titleLarge (16sp w600 product price), body (15sp w400 chat)
  // JetBrainsMono: inline olarak kullanılacak (log, OCR, hukuki atıf)
  // ────────────────────────────────────────────────────────────────────────────

  static const TextTheme _darkTextTheme = TextTheme(
    // Montserrat — Görsel Vitrin & Başlık
    displayLarge: TextStyle(
      fontFamily: _headingFamily,
      fontSize: 32,
      fontWeight: FontWeight.w700,
      color: AppColors.textPrimary,
    ),
    displayMedium: TextStyle(
      fontFamily: _headingFamily,
      fontSize: 28,
      fontWeight: FontWeight.w700,
      color: AppColors.textPrimary,
    ),
    displaySmall: TextStyle(
      fontFamily: _headingFamily,
      fontSize: 24,
      fontWeight: FontWeight.w700,
      color: AppColors.textPrimary,
    ),
    headlineLarge: TextStyle(
      fontFamily: _headingFamily,
      fontSize: 20,
      fontWeight: FontWeight.w700,
      color: AppColors.textPrimary,
    ),
    headlineMedium: TextStyle(
      fontFamily: _headingFamily,
      fontSize: 18,
      fontWeight: FontWeight.w600,
      color: AppColors.textPrimary,
    ),
    headlineSmall: TextStyle(
      fontFamily: _headingFamily,
      fontSize: 16,
      fontWeight: FontWeight.w600,
      color: AppColors.textPrimary,
    ),

    // Inter — Gövde Metni & İçerik
    titleLarge: TextStyle(
      fontFamily: _bodyFamily,
      fontSize: 16,
      fontWeight: FontWeight.w600,
      color: AppColors.textPrimary,
    ),
    titleMedium: TextStyle(
      fontFamily: _bodyFamily,
      fontSize: 14,
      fontWeight: FontWeight.w500,
      color: AppColors.textPrimary,
    ),
    titleSmall: TextStyle(
      fontFamily: _bodyFamily,
      fontSize: 13,
      fontWeight: FontWeight.w500,
      color: AppColors.textSecondary,
    ),
    bodyLarge: TextStyle(
      fontFamily: _bodyFamily,
      fontSize: 15,
      fontWeight: FontWeight.w400,
      color: AppColors.textSecondary,
    ),
    bodyMedium: TextStyle(
      fontFamily: _bodyFamily,
      fontSize: 14,
      fontWeight: FontWeight.w400,
      color: AppColors.textSecondary,
    ),
    bodySmall: TextStyle(
      fontFamily: _bodyFamily,
      fontSize: 12,
      fontWeight: FontWeight.w400,
      color: AppColors.textTertiary,
    ),

    // Montserrat — CTA Butonları
    labelLarge: TextStyle(
      fontFamily: _headingFamily,
      fontSize: 16,
      fontWeight: FontWeight.w600,
      color: AppColors.textPrimary,
    ),
    labelMedium: TextStyle(
      fontFamily: _bodyFamily,
      fontSize: 13,
      fontWeight: FontWeight.w500,
      color: AppColors.textSecondary,
    ),
    labelSmall: TextStyle(
      fontFamily: _bodyFamily,
      fontSize: 11,
      fontWeight: FontWeight.w500,
      color: AppColors.textTertiary,
    ),
  );

  // ────────────────────────────────────────────────────────────────────────────
  // Text Themes — Light
  // ────────────────────────────────────────────────────────────────────────────

  static final TextTheme _lightTextTheme = TextTheme(
    // Montserrat
    displayLarge: TextStyle(
      fontFamily: _headingFamily,
      fontSize: 32,
      fontWeight: FontWeight.w700,
      color: AppColors.darkNavy,
    ),
    displayMedium: TextStyle(
      fontFamily: _headingFamily,
      fontSize: 28,
      fontWeight: FontWeight.w700,
      color: AppColors.darkNavy,
    ),
    displaySmall: TextStyle(
      fontFamily: _headingFamily,
      fontSize: 24,
      fontWeight: FontWeight.w700,
      color: AppColors.darkNavy,
    ),
    headlineLarge: TextStyle(
      fontFamily: _headingFamily,
      fontSize: 20,
      fontWeight: FontWeight.w700,
      color: AppColors.darkNavy,
    ),
    headlineMedium: TextStyle(
      fontFamily: _headingFamily,
      fontSize: 18,
      fontWeight: FontWeight.w600,
      color: AppColors.darkNavy,
    ),
    headlineSmall: TextStyle(
      fontFamily: _headingFamily,
      fontSize: 16,
      fontWeight: FontWeight.w600,
      color: AppColors.darkNavy,
    ),

    // Inter
    titleLarge: TextStyle(
      fontFamily: _bodyFamily,
      fontSize: 16,
      fontWeight: FontWeight.w600,
      color: AppColors.darkNavy,
    ),
    titleMedium: TextStyle(
      fontFamily: _bodyFamily,
      fontSize: 14,
      fontWeight: FontWeight.w500,
      color: AppColors.darkNavy,
    ),
    titleSmall: TextStyle(
      fontFamily: _bodyFamily,
      fontSize: 13,
      fontWeight: FontWeight.w500,
      color: AppColors.darkNavy,
    ),
    bodyLarge: TextStyle(
      fontFamily: _bodyFamily,
      fontSize: 15,
      fontWeight: FontWeight.w400,
      color: AppColors.darkNavy,
    ),
    bodyMedium: TextStyle(
      fontFamily: _bodyFamily,
      fontSize: 14,
      fontWeight: FontWeight.w400,
      color: AppColors.darkNavy,
    ),
    bodySmall: TextStyle(
      fontFamily: _bodyFamily,
      fontSize: 12,
      fontWeight: FontWeight.w400,
      color: AppColors.darkNavy,
    ),
    labelLarge: TextStyle(
      fontFamily: _headingFamily,
      fontSize: 16,
      fontWeight: FontWeight.w600,
      color: AppColors.darkNavy,
    ),
    labelMedium: TextStyle(
      fontFamily: _bodyFamily,
      fontSize: 13,
      fontWeight: FontWeight.w500,
      color: AppColors.darkNavy,
    ),
    labelSmall: TextStyle(
      fontFamily: _bodyFamily,
      fontSize: 11,
      fontWeight: FontWeight.w500,
      color: AppColors.darkNavy,
    ),
  );
}
