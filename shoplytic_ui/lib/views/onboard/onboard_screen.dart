import 'package:flutter/material.dart';
import '../../theme/app_colors.dart';

class OnboardScreen extends StatefulWidget {
  const OnboardScreen({super.key});

  @override
  State<OnboardScreen> createState() => _OnboardScreenState();
}

class _OnboardScreenState extends State<OnboardScreen> {
  final PageController _pageController = PageController();
  int _currentPage = 0;

  final List<_OnboardPage> _pages = const [
    _OnboardPage(
      title: 'Hoş Geldin',
      description: 'AI destekli akıllı alışveriş asistanın',
      image: 'assets/images/HayatındanBirCümle.jpg',
    ),
    _OnboardPage(
      title: 'Zihin Haritası',
      description: 'İhtiyaçlarını görselleştir, kategorilere ayır',
      image: 'assets/images/ZihinselHarita.jpg',
    ),
    _OnboardPage(
      title: 'AI Sohbet',
      description: 'Yapay zekayla konuş, anında öneri al',
      image: 'assets/images/ÜrünÖnerileri.jpg',
    ),
    _OnboardPage(
      title: 'Tüketici Hakları',
      description: 'Haklarını öğren, dilekçe hazırla',
      image: 'assets/images/TüketiciHakları.jpg',
    ),
    _OnboardPage(
      title: 'Hazır mısın?',
      description: 'Alışveriş deneyimini dönüştürmeye başla',
      image: 'assets/images/TercihleriniHatırlar.jpg',
    ),
  ];

  @override
  void dispose() {
    _pageController.dispose();
    super.dispose();
  }

  void _onPageChanged(int page) {
    setState(() => _currentPage = page);
  }

  void _goToHome() {
    Navigator.pushReplacementNamed(context, '/home');
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        decoration: const BoxDecoration(
          gradient: AppColors.backgroundDark,
        ),
        child: SafeArea(
          child: Column(
            children: [
              // Skip button
              Padding(
                padding: const EdgeInsets.only(right: 20, top: 12),
                child: Align(
                  alignment: Alignment.topRight,
                  child: TextButton(
                    onPressed: _goToHome,
                    child: Text(
                      _currentPage == _pages.length - 1 ? '' : 'Skip',
                      style: TextStyle(
                        color: AppColors.textSecondary.withValues(alpha: 0.6),
                        fontSize: 15,
                        fontWeight: FontWeight.w500,
                      ),
                    ),
                  ),
                ),
              ),

              // Pages
              Expanded(
                child: PageView.builder(
                  controller: _pageController,
                  onPageChanged: _onPageChanged,
                  itemCount: _pages.length,
                  itemBuilder: (context, index) {
                    final page = _pages[index];
                    return Padding(
                      padding: const EdgeInsets.symmetric(horizontal: 32),
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          // Image
                          Container(
                            height: 240,
                            width: 240,
                            decoration: BoxDecoration(
                              shape: BoxShape.circle,
                              boxShadow: [
                                BoxShadow(
                                  color: AppColors.deepTeal.withValues(alpha: 0.2),
                                  blurRadius: 40,
                                  spreadRadius: 8,
                                ),
                              ],
                            ),
                            child: ClipOval(
                              child: Image.asset(
                                page.image,
                                fit: BoxFit.cover,
                                errorBuilder: (context, error, stackTrace) =>
                                    Container(
                                      color: AppColors.surfaceDark,
                                      child: Icon(
                                        Icons.shopping_bag_outlined,
                                        size: 80,
                                        color: AppColors.deepTeal.withValues(alpha: 0.5),
                                      ),
                                    ),
                              ),
                            ),
                          ),
                          const SizedBox(height: 48),

                          // Title
                          Text(
                            page.title,
                            style: Theme.of(context).textTheme.displaySmall,
                            textAlign: TextAlign.center,
                          ),
                          const SizedBox(height: 12),

                          // Description
                          Text(
                            page.description,
                            style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                                  color: AppColors.textSecondary.withValues(alpha: 0.7),
                                ),
                            textAlign: TextAlign.center,
                          ),
                        ],
                      ),
                    );
                  },
                ),
              ),

              // Bottom section
              Padding(
                padding: const EdgeInsets.only(bottom: 40, left: 32, right: 32),
                child: Column(
                  children: [
                    // Dot indicators
                    Row(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: List.generate(
                        _pages.length,
                        (index) => AnimatedContainer(
                          duration: const Duration(milliseconds: 300),
                          margin: const EdgeInsets.symmetric(horizontal: 5),
                          width: _currentPage == index ? 28 : 8,
                          height: 8,
                          decoration: BoxDecoration(
                            borderRadius: BorderRadius.circular(4),
                            color: _currentPage == index
                                ? AppColors.mintActive
                                : AppColors.glassBorder,
                          ),
                        ),
                      ),
                    ),
                    const SizedBox(height: 32),

                    // Action button
                    SizedBox(
                      width: double.infinity,
                      child: ElevatedButton(
                        onPressed: _currentPage == _pages.length - 1
                            ? _goToHome
                            : () => _pageController.nextPage(
                                  duration: const Duration(milliseconds: 400),
                                  curve: Curves.easeInOut,
                                ),
                        child: Text(
                          _currentPage == _pages.length - 1
                              ? "Başla"
                              : "Devam",
                        ),
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class _OnboardPage {
  final String title;
  final String description;
  final String image;

  const _OnboardPage({
    required this.title,
    required this.description,
    required this.image,
  });
}
