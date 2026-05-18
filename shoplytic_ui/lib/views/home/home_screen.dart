import 'package:flutter/material.dart';
import '../../theme/app_colors.dart';
import '../../widgets/floating_glass_navbar.dart';
import '../../widgets/glass_card.dart';
import '../../widgets/animated_prompt_input.dart';
import '../mind_map/mind_map_screen.dart';
import '../chat/chat_screen.dart';
import '../legal/legal_screen.dart';
import '../profile/profile_screen.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  int _currentIndex = 0;
  bool _hasPrompt = false;
  String _lastPrompt = '';

  List<Widget> get _screens => [
        _HomeTab(
          onPromptSubmitted: _onPromptSubmitted,
          lastPrompt: _lastPrompt,
          hasPrompt: _hasPrompt,
        ),
        const MindMapScreen(),
        const ChatScreen(),
        const LegalScreen(),
        const ProfileScreen(),
      ];

  void _onPromptSubmitted(String prompt) {
    setState(() {
      _hasPrompt = true;
      _lastPrompt = prompt;
      _currentIndex = 1;
    });
  }

  void _onTabChanged(int index) {
    setState(() => _currentIndex = index);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      extendBody: true,
      body: Container(
        decoration: const BoxDecoration(
          gradient: AppColors.backgroundDark,
        ),
        child: IndexedStack(
          index: _currentIndex,
          children: _screens,
        ),
      ),
      bottomNavigationBar: FloatingGlassNavbar(
        selectedIndex: _currentIndex,
        onItemTapped: _onTabChanged,
      ),
    );
  }
}

class _HomeTab extends StatefulWidget {
  final String lastPrompt;
  final bool hasPrompt;
  final void Function(String) onPromptSubmitted;

  const _HomeTab({
    required this.lastPrompt,
    required this.hasPrompt,
    required this.onPromptSubmitted,
  });

  @override
  State<_HomeTab> createState() => _HomeTabState();
}

class _HomeTabState extends State<_HomeTab> {
  final TextEditingController _controller = TextEditingController();

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return SafeArea(
      child: SingleChildScrollView(
        padding: const EdgeInsets.symmetric(horizontal: 24),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const SizedBox(height: 40),
            Text(
              'Merhaba!',
              style: Theme.of(context).textTheme.displaySmall,
            ),
            const SizedBox(height: 8),
            Text(
              'Hayatındaki değişikliği anlat,\nalışveriş listeni oluşturalım.',
              style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                    color: AppColors.textSecondary.withValues(alpha: 0.7),
                    height: 1.4,
                  ),
            ),
            const SizedBox(height: 32),
            AnimatedPromptInput(
              controller: _controller,
              onSubmitted: widget.onPromptSubmitted,
            ),
            const SizedBox(height: 32),
            if (widget.hasPrompt) ...[
              GlassCard(
                child: ListTile(
                  leading: Container(
                    width: 44,
                    height: 44,
                    decoration: BoxDecoration(
                      color: AppColors.deepTeal.withValues(alpha: 0.2),
                      borderRadius: BorderRadius.circular(12),
                    ),
                    child: const Icon(Icons.history, color: AppColors.mintActive),
                  ),
                  title: Text(
                    'Son Prompt',
                    style: Theme.of(context).textTheme.titleMedium,
                  ),
                  subtitle: Text(
                    widget.lastPrompt,
                    style: Theme.of(context).textTheme.bodySmall,
                    maxLines: 1,
                    overflow: TextOverflow.ellipsis,
                  ),
                  trailing: const Icon(
                    Icons.chevron_right,
                    color: AppColors.textTertiary,
                  ),
                  onTap: () => widget.onPromptSubmitted(widget.lastPrompt),
                ),
              ),
              const SizedBox(height: 12),
            ],
            Text(
              'Örnek Promptlar',
              style: Theme.of(context).textTheme.titleMedium,
            ),
            const SizedBox(height: 12),
            _buildSampleChip('Adana\'da üniversite kazandım, yurt için alışveriş'),
            const SizedBox(height: 8),
            _buildSampleChip('İstanbul\'da yeni işe başlıyorum, ofis hazırlığı'),
            const SizedBox(height: 8),
            _buildSampleChip('Evleniyorum, ev eşyası alacağım'),
            const SizedBox(height: 40),
          ],
        ),
      ),
    );
  }

  Widget _buildSampleChip(String text) {
    return GestureDetector(
      onTap: () {
        _controller.text = text;
        widget.onPromptSubmitted(text);
      },
      child: GlassCard(
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
        child: Row(
          children: [
            Icon(
              Icons.lightbulb_outline,
              size: 18,
              color: AppColors.amberGold.withValues(alpha: 0.7),
            ),
            const SizedBox(width: 12),
            Expanded(
              child: Text(
                text,
                style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                      color: AppColors.textSecondary.withValues(alpha: 0.8),
                    ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
