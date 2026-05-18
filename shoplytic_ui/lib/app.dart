import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import 'theme/app_theme.dart';
import 'views/splash/splash_screen.dart';
import 'views/onboard/onboard_screen.dart';
import 'views/home/home_screen.dart';
import 'providers/mind_map_provider.dart';
import 'providers/chat_provider.dart';
import 'providers/product_provider.dart';
import 'providers/legal_provider.dart';

class ShoplyticApp extends StatelessWidget {
  const ShoplyticApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => MindMapProvider()),
        ChangeNotifierProvider(create: (_) => ChatProvider()),
        ChangeNotifierProvider(create: (_) => ProductProvider()),
        ChangeNotifierProvider(create: (_) => LegalProvider()),
      ],
      child: MaterialApp(
        title: 'Shoplytic',
        debugShowCheckedModeBanner: false,
        theme: AppTheme.dark,
        initialRoute: '/',
        routes: {
          '/': (context) => const SplashScreen(),
          '/onboard': (context) => const OnboardScreen(),
          '/home': (context) => const HomeScreen(),
        },
      ),
    );
  }
}
