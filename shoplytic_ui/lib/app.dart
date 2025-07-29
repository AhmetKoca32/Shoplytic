import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import 'providers/mind_map_provider.dart';
import 'views/auth/login_screen.dart';
import 'views/auth/splash_screen.dart';
import 'views/home/home_screen.dart';
import 'views/mind_map/mind_map_screen.dart';
import 'views/onboard/onboard_screen.dart';

class ShoplyticApp extends StatelessWidget {
  const ShoplyticApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [ChangeNotifierProvider(create: (_) => MindMapProvider())],
      child: MaterialApp(
        title: 'Shoplytic',
        debugShowCheckedModeBanner: false,
        theme: ThemeData(
          colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
          useMaterial3: true,
        ),
        initialRoute: '/',
        routes: {
          '/': (context) => const SplashScreen(),
          '/home': (context) => const HomeScreen(),
          '/onboard': (context) => const OnboardScreen(),
          '/login': (context) => const LoginScreen(),
          '/mindmap': (context) => const MindMapScreen(),
        },
      ),
    );
  }
}
