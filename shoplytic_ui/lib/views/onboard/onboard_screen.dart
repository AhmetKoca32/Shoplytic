import 'package:flutter/material.dart';

class OnboardScreen extends StatefulWidget {
  const OnboardScreen({Key? key}) : super(key: key);

  @override
  State<OnboardScreen> createState() => _OnboardScreenState();
}

class _OnboardScreenState extends State<OnboardScreen> {
  final PageController _pageController = PageController();
  int _currentPage = 0;

  final List<_OnboardPageData> _pages = [
    _OnboardPageData(
      title: 'Hayatından Bir Cümle',
      description:
          '“Üniversiteye başlayacağım” gibi bir cümleyle ihtiyaçlarını anlayan akıllı asistan.',
      image: 'assets/images/HayatındanBirCümle.jpg',
      gradient: LinearGradient(
        colors: [Color(0xFF7F7FD5), Color(0xFF86A8E7), Color(0xFF91EAE4)],
        begin: Alignment.topLeft,
        end: Alignment.bottomRight,
      ),
    ),
    _OnboardPageData(
      title: 'Zihinsel Harita',
      description:
          'Senin için alışveriş yolculuğunu planlar, adım adım rehberlik eder.',
      image: 'assets/images/ZihinselHarita.jpg',
      gradient: LinearGradient(
        colors: [Color(0xFFFC5C7D), Color(0xFF6A82FB)],
        begin: Alignment.topRight,
        end: Alignment.bottomLeft,
      ),
    ),
    _OnboardPageData(
      title: 'Ürün Önerileri',
      description: 'İhtiyaçlarına uygun ürünleri akıllıca önerir.',
      image: 'assets/images/ÜrünÖnerileri.jpg',
      gradient: LinearGradient(
        colors: [Color(0xFFF7971E), Color(0xFFFFD200)],
        begin: Alignment.topLeft,
        end: Alignment.bottomRight,
      ),
    ),
    _OnboardPageData(
      title: 'Tercihlerini Hatırlar',
      description:
          'Daha önceki seçimlerini hafızada tutar, alışverişini kolaylaştırır.',
      image: 'assets/images/TercihleriniHatırlar.jpg',
      gradient: LinearGradient(
        colors: [Color(0xFF43CEA2), Color(0xFF185A9D)],
        begin: Alignment.topRight,
        end: Alignment.bottomLeft,
      ),
    ),
    _OnboardPageData(
      title: 'Tüketici Hakları',
      description: 'Alışverişte haklarını korur, sana yol gösterir.',
      image: 'assets/images/TüketiciHakları.jpg',
      gradient: LinearGradient(
        colors: [Color(0xFFB06AB3), Color(0xFF4568DC)],
        begin: Alignment.topLeft,
        end: Alignment.bottomRight,
      ),
    ),
  ];

  void _nextPage() {
    if (_currentPage < _pages.length - 1) {
      _pageController.nextPage(
        duration: const Duration(milliseconds: 400),
        curve: Curves.easeInOut,
      );
    } else {
      // Onboarding bittiğinde login ekranına yönlendir
      Navigator.of(context).pushReplacementNamed('/login');
    }
  }

  void _previousPage() {
    if (_currentPage > 0) {
      _pageController.previousPage(
        duration: const Duration(milliseconds: 400),
        curve: Curves.easeInOut,
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    final page = _pages[_currentPage];
    return Scaffold(
      body: AnimatedContainer(
        duration: const Duration(milliseconds: 600),
        decoration: BoxDecoration(gradient: page.gradient),
        child: SafeArea(
          child: Column(
            children: [
              Expanded(
                child: PageView.builder(
                  controller: _pageController,
                  itemCount: _pages.length,
                  onPageChanged: (index) {
                    setState(() {
                      _currentPage = index;
                    });
                  },
                  itemBuilder: (context, index) {
                    final page = _pages[index];
                    return Padding(
                      padding: const EdgeInsets.symmetric(
                        horizontal: 24.0,
                        vertical: 32.0,
                      ),
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Container(
                            decoration: BoxDecoration(
                              boxShadow: [
                                BoxShadow(
                                  color: Colors.black.withOpacity(0.08),
                                  blurRadius: 32,
                                  offset: const Offset(0, 16),
                                ),
                              ],
                              borderRadius: BorderRadius.circular(32),
                            ),
                            child: ClipRRect(
                              borderRadius: BorderRadius.circular(32),
                              child: Image.asset(
                                page.image,
                                width: 180,
                                height: 180,
                                fit: BoxFit.cover,
                              ),
                            ),
                          ),
                          const SizedBox(height: 32),
                          Text(
                            page.title,
                            style: const TextStyle(
                              fontSize: 30,
                              fontWeight: FontWeight.bold,
                              color: Colors.white,
                              letterSpacing: 1.2,
                            ),
                            textAlign: TextAlign.center,
                          ),
                          const SizedBox(height: 18),
                          Text(
                            page.description,
                            style: const TextStyle(
                              fontSize: 18,
                              color: Colors.white70,
                              height: 1.4,
                            ),
                            textAlign: TextAlign.center,
                          ),
                        ],
                      ),
                    );
                  },
                ),
              ),
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: List.generate(
                  _pages.length,
                  (index) => _buildDot(index),
                ),
              ),
              const SizedBox(height: 24),
              Padding(
                padding: const EdgeInsets.symmetric(horizontal: 32.0),
                child: Row(
                  children: [
                    Expanded(
                      child: ElevatedButton(
                        onPressed: _currentPage == 0 ? null : _previousPage,
                        style: ElevatedButton.styleFrom(
                          backgroundColor: Colors.white,
                          foregroundColor: page.gradient.colors.first,
                          padding: const EdgeInsets.symmetric(vertical: 16),
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(16),
                          ),
                          elevation: 2,
                        ),
                        child: const Text(
                          'Geri',
                          style: TextStyle(
                            fontSize: 18,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                      ),
                    ),
                    const SizedBox(width: 16),
                    Expanded(
                      child: ElevatedButton(
                        onPressed: _nextPage,
                        style: ElevatedButton.styleFrom(
                          backgroundColor: Colors.white,
                          foregroundColor: page.gradient.colors.first,
                          padding: const EdgeInsets.symmetric(vertical: 16),
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(16),
                          ),
                          elevation: 2,
                        ),
                        child: Text(
                          _currentPage == _pages.length - 1 ? 'Başla' : 'İleri',
                          style: const TextStyle(
                            fontSize: 18,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                      ),
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 32),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildDot(int index) {
    return AnimatedContainer(
      duration: const Duration(milliseconds: 300),
      margin: const EdgeInsets.symmetric(horizontal: 4),
      width: _currentPage == index ? 16 : 8,
      height: 8,
      decoration: BoxDecoration(
        color: _currentPage == index
            ? Colors.deepPurple
            : Colors.deepPurple[100],
        borderRadius: BorderRadius.circular(4),
      ),
    );
  }
}

class _OnboardPageData {
  final String title;
  final String description;
  final String image;
  final Gradient gradient;
  _OnboardPageData({
    required this.title,
    required this.description,
    required this.image,
    required this.gradient,
  });
}
