import 'dart:async';

import 'package:flutter/material.dart';

class SplashScreen extends StatefulWidget {
  const SplashScreen({Key? key}) : super(key: key);

  @override
  State<SplashScreen> createState() => _SplashScreenState();
}

class _SplashScreenState extends State<SplashScreen>
    with TickerProviderStateMixin {
  double _logoOpacity = 0.0;
  double _logoScale = 0.8;

  @override
  void initState() {
    super.initState();
    // Logo animasyonu
    Timer(const Duration(milliseconds: 2000), () {
      setState(() {
        _logoOpacity = 1.0;
        _logoScale = 1.0;
      });
      // 2 saniye sonra login ekranına geç
      Timer(const Duration(seconds: 3), () {
        if (mounted) {
          Navigator.of(context).pushReplacementNamed('/onboard');
        }
      });
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        width: double.infinity,
        height: double.infinity,
        decoration: const BoxDecoration(
          image: DecorationImage(
            image: AssetImage(
              'assets/images/splash_screen_background_image.jpg',
            ), // Arka plan görseli
            fit: BoxFit.cover,
          ),
        ),
        child: Stack(
          children: [
            // Logo tam ortada
            Center(
              child: AnimatedOpacity(
                opacity: _logoOpacity,
                duration: const Duration(milliseconds: 900),
                child: AnimatedScale(
                  scale: _logoScale,
                  duration: const Duration(milliseconds: 900),
                  curve: Curves.easeOutBack,
                  child: Image.asset(
                    'assets/logos/shoplytics-high-resolution-logo-transparent.png', // Logo dosyan
                    width: 220,
                    fit: BoxFit.contain,
                  ),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
