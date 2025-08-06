import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:shoplytic_ui/views/mind_map/mind_map_screen.dart';

import '../../../providers/mind_map_provider.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({Key? key}) : super(key: key);

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  final TextEditingController _promptController = TextEditingController();
  int _selectedIndex = 0;

  @override
  void dispose() {
    _promptController.dispose();
    super.dispose();
  }

  void _onNavBarTapped(int index) {
    setState(() {
      _selectedIndex = index;
    });
  }

  Widget _buildNavItem({
    required IconData icon,
    required String label,
    required int index,
  }) {
    final bool isSelected = _selectedIndex == index;
    return GestureDetector(
      onTap: () => _onNavBarTapped(index),
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 300),
        curve: Curves.easeOutCubic,
        margin: const EdgeInsets.symmetric(vertical: 4, horizontal: 2),
        padding: EdgeInsets.symmetric(
          horizontal: isSelected ? 18 : 12,
          vertical: isSelected ? 10 : 6,
        ),
        decoration: isSelected
            ? BoxDecoration(
                gradient: LinearGradient(
                  colors: [Color(0xFF7F7FD5), Color(0xFF91EAE4)],
                  begin: Alignment.topLeft,
                  end: Alignment.bottomRight,
                ),
                boxShadow: [
                  BoxShadow(
                    color: Color(0xFF7F7FD5).withOpacity(0.18),
                    blurRadius: 16,
                    offset: Offset(0, 4),
                  ),
                ],
                borderRadius: BorderRadius.circular(18),
              )
            : null,
        child: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            AnimatedScale(
              scale: isSelected ? 1.18 : 1.0,
              duration: const Duration(milliseconds: 300),
              curve: Curves.easeOutBack,
              child: Icon(
                icon,
                color: isSelected ? Colors.white : Colors.grey[400],
                size: 28,
              ),
            ),
            AnimatedSwitcher(
              duration: const Duration(milliseconds: 300),
              transitionBuilder: (child, anim) =>
                  FadeTransition(opacity: anim, child: child),
              child: isSelected
                  ? Padding(
                      key: ValueKey(label),
                      padding: const EdgeInsets.only(left: 8),
                      child: Text(
                        label,
                        style: const TextStyle(
                          color: Colors.white,
                          fontWeight: FontWeight.bold,
                          fontSize: 16,
                        ),
                      ),
                    )
                  : const SizedBox.shrink(),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildMainContent() {
    return Stack(
      fit: StackFit.expand,
      children: [
        Image.asset(
          'assets/images/login_screen_background_image.jpg',
          fit: BoxFit.cover,
        ),
        Container(color: Colors.black.withOpacity(0.25)),
        SafeArea(
          child: Center(
            child: Padding(
              padding: const EdgeInsets.symmetric(horizontal: 32.0),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Text(
                    'Hayatında bir şey mi değişti?',
                    style: const TextStyle(
                      fontSize: 28,
                      fontWeight: FontWeight.bold,
                      color: Colors.white,
                      letterSpacing: 1.1,
                      shadows: [
                        Shadow(
                          color: Colors.black38,
                          blurRadius: 8,
                          offset: Offset(0, 2),
                        ),
                      ],
                    ),
                    textAlign: TextAlign.center,
                  ),
                  Text(
                    'Gel beraber alışverişini yapalım!',
                    style: const TextStyle(
                      fontSize: 28,
                      fontWeight: FontWeight.bold,
                      color: Colors.white,
                      letterSpacing: 1.1,
                      shadows: [
                        Shadow(
                          color: Colors.black38,
                          blurRadius: 8,
                          offset: Offset(0, 2),
                        ),
                      ],
                    ),
                    textAlign: TextAlign.center,
                  ),
                  const SizedBox(height: 32),
                  Container(
                    decoration: BoxDecoration(
                      color: Colors.white.withOpacity(0.9),
                      borderRadius: BorderRadius.circular(20),
                      boxShadow: [
                        BoxShadow(
                          color: Colors.black.withOpacity(0.08),
                          blurRadius: 16,
                          offset: const Offset(0, 8),
                        ),
                      ],
                    ),
                    child: TextField(
                      controller: _promptController,
                      style: const TextStyle(
                        fontSize: 18,
                        color: Colors.black87,
                      ),
                      decoration: const InputDecoration(
                        hintText:
                            'Hayatımda bir şey değişti...\n(ör: Üniversiteye başlayacağım)',
                        hintStyle: TextStyle(
                          color: Colors.black38,
                          fontSize: 16,
                        ),
                        border: InputBorder.none,
                        contentPadding: EdgeInsets.symmetric(
                          horizontal: 20,
                          vertical: 20,
                        ),
                      ),
                      minLines: 2,
                      maxLines: 4,
                    ),
                  ),
                  const SizedBox(height: 24),
                  Consumer<MindMapProvider>(
                    builder: (context, mindMapProvider, child) {
                      return Column(
                        children: [
                          if (mindMapProvider.isLoading)
                            const Padding(
                              padding: EdgeInsets.only(bottom: 16),
                              child: CircularProgressIndicator(
                                valueColor: AlwaysStoppedAnimation<Color>(
                                  Colors.white,
                                ),
                              ),
                            ),
                          if (mindMapProvider.error != null)
                            Container(
                              width: double.infinity,
                              padding: const EdgeInsets.all(12),
                              margin: const EdgeInsets.only(bottom: 16),
                              decoration: BoxDecoration(
                                color: Colors.red.withOpacity(0.1),
                                borderRadius: BorderRadius.circular(8),
                                border: Border.all(
                                  color: Colors.red.withOpacity(0.3),
                                ),
                              ),
                              child: Text(
                                mindMapProvider.error!,
                                style: const TextStyle(color: Colors.red),
                                textAlign: TextAlign.center,
                              ),
                            ),
                          SizedBox(
                            width: double.infinity,
                            child: ElevatedButton(
                              onPressed: mindMapProvider.isLoading
                                  ? null
                                  : () async {
                                      if (_promptController.text
                                          .trim()
                                          .isNotEmpty) {
                                        await mindMapProvider.generateMindMap(
                                          _promptController.text.trim(),
                                          'user_${DateTime.now().millisecondsSinceEpoch}',
                                        );

                                        if (mindMapProvider.error == null) {
                                          setState(() {
                                            _selectedIndex =
                                                1; // Zihin haritası sekmesine geç
                                          });
                                        }
                                      } else {
                                        ScaffoldMessenger.of(
                                          context,
                                        ).showSnackBar(
                                          const SnackBar(
                                            content: Text(
                                              'Lütfen bir durum açıklayın',
                                            ),
                                            backgroundColor: Colors.orange,
                                          ),
                                        );
                                      }
                                    },
                              style: ElevatedButton.styleFrom(
                                backgroundColor: Colors.white,
                                foregroundColor: const Color(0xFF7F7FD5),
                                padding: const EdgeInsets.symmetric(
                                  vertical: 16,
                                ),
                                shape: RoundedRectangleBorder(
                                  borderRadius: BorderRadius.circular(16),
                                ),
                                elevation: 2,
                              ),
                              child: const Text(
                                'Gönder',
                                style: TextStyle(
                                  fontSize: 18,
                                  fontWeight: FontWeight.bold,
                                ),
                              ),
                            ),
                          ),
                        ],
                      );
                    },
                  ),
                ],
              ),
            ),
          ),
        ),
      ],
    );
  }

  @override
  Widget build(BuildContext context) {
    final screens = [
      _buildMainContent(),
      const MindMapScreen(),
      const Center(child: Text("Sohbet", style: TextStyle(fontSize: 24))),
      const Center(child: Text("Profil", style: TextStyle(fontSize: 24))),
    ];

    return Scaffold(
      body: IndexedStack(index: _selectedIndex, children: screens),
      bottomNavigationBar: Container(
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: const BorderRadius.only(
            topLeft: Radius.circular(24),
            topRight: Radius.circular(24),
          ),
          boxShadow: [
            BoxShadow(
              color: Colors.black.withOpacity(0.08),
              blurRadius: 16,
              offset: const Offset(0, -2),
            ),
          ],
        ),
        padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.spaceAround,
          children: [
            _buildNavItem(icon: Icons.home, label: 'Ana Sayfa', index: 0),
            _buildNavItem(
              icon: Icons.account_tree,
              label: 'Zihin Haritası',
              index: 1,
            ),
            _buildNavItem(
              icon: Icons.chat_bubble_outline,
              label: 'Sohbet',
              index: 2,
            ),
            _buildNavItem(
              icon: Icons.person_outline,
              label: 'Profil',
              index: 3,
            ),
          ],
        ),
      ),
    );
  }
}
