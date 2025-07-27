import 'package:flutter/material.dart';

import 'views/auth/splash_screen.dart';
import 'views/onboard/onboard_screen.dart';

class ShoplyticApp extends StatelessWidget {
  const ShoplyticApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Shoplytic',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
        useMaterial3: true,
      ),
      initialRoute: '/',
      routes: {
        '/': (context) => const SplashScreen(),
        '/onboard': (context) => const OnboardScreen(),
        '/login': (context) =>
            const Placeholder(), // Giriş ekranı burada olacak
      },
    );
  }
}
