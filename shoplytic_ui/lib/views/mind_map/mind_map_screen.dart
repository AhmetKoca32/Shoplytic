import 'package:flutter/material.dart';
import '../../theme/app_colors.dart';
import '../../widgets/mind_map_widget.dart';
import '../../widgets/product_card.dart';

class MindMapScreen extends StatefulWidget {
  const MindMapScreen({super.key});

  @override
  State<MindMapScreen> createState() => _MindMapScreenState();
}

class _MindMapScreenState extends State<MindMapScreen> {
  bool _hasMindMap = false;

  // Mock data for UI demonstration
  final Map<String, dynamic> _mockMindMap = {
    'central_topic': 'Adana\'da Üniversite',
    'user_summary': 'Adana\'da üniversite kazanan öğrenci için yurt ve eğitim hazırlığı',
    'main_categories': [
      {'name': 'Akademik', 'emoji': '📚', 'priority': 'high', 'estimated_budget': '5000-10000 TL'},
      {'name': 'Teknoloji', 'emoji': '💻', 'priority': 'high', 'estimated_budget': '15000-25000 TL'},
      {'name': 'Kırtasiye', 'emoji': '✏️', 'priority': 'medium', 'estimated_budget': '500-1000 TL'},
      {'name': 'Giyim', 'emoji': '👕', 'priority': 'medium', 'estimated_budget': '3000-5000 TL'},
      {'name': 'Yurt Eşyası', 'emoji': '🛏️', 'priority': 'medium', 'estimated_budget': '5000-8000 TL'},
    ],
    'total_estimated_budget': '28500-49000 TL',
  };

  final List<Map<String, dynamic>> _mockProducts = [
    {
      'name': 'Lenovo ThinkPad E15',
      'price': 15999.99,
      'platform': 'Trendyol',
      'rating': 4.5,
      'review_count': 1250,
    },
    {
      'name': 'Samsung Galaxy Tab A9+',
      'price': 8499.00,
      'platform': 'Hepsiburada',
      'rating': 4.3,
      'review_count': 890,
    },
    {
      'name': 'Logitech Mouse',
      'price': 599.99,
      'platform': 'Trendyol',
      'rating': 4.7,
      'review_count': 3200,
    },
  ];

  @override
  void initState() {
    super.initState();
    // Simulate having a mind map after prompt
    Future.delayed(const Duration(milliseconds: 500), () {
      if (mounted) {
        setState(() => _hasMindMap = true);
      }
    });
  }

  void _onNodeTap(Map<String, dynamic> node) {
    showModalBottomSheet(
      context: context,
      backgroundColor: Colors.transparent,
      isScrollControlled: true,
      builder: (context) => _ProductBottomSheet(
        category: node,
        products: _mockProducts,
      ),
    );
  }

  void _onNodeLongPress(Map<String, dynamic> node) {
    showModalBottomSheet(
      context: context,
      backgroundColor: Colors.transparent,
      isScrollControlled: true,
      builder: (context) => _ChatPanel(category: node),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.transparent,
      body: SafeArea(
        child: Column(
          children: [
            // Header
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 16),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Text(
                    'Zihin Haritası',
                    style: Theme.of(context).textTheme.headlineLarge,
                  ),
                  TextButton.icon(
                    onPressed: () {
                      // Navigate to home tab to enter new prompt
                    },
                    icon: const Icon(Icons.add, color: AppColors.mintActive),
                    label: Text(
                      'Yeni Prompt',
                      style: TextStyle(color: AppColors.mintActive),
                    ),
                  ),
                ],
              ),
            ),

            // Mind map or empty state
            Expanded(
              child: _hasMindMap
                  ? MindMapWidget(
                      data: _mockMindMap,
                      onNodeTap: _onNodeTap,
                      onNodeLongPress: _onNodeLongPress,
                    )
                  : _buildEmptyState(),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildEmptyState() {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Container(
            width: 80,
            height: 80,
            decoration: BoxDecoration(
              shape: BoxShape.circle,
              color: AppColors.glassMedium,
            ),
            child: Icon(
              Icons.psychology_outlined,
              size: 40,
              color: AppColors.textSecondary.withValues(alpha: 0.5),
            ),
          ),
          const SizedBox(height: 24),
          Text(
            'Henüz bir zihin haritan yok',
            style: Theme.of(context).textTheme.titleLarge,
          ),
          const SizedBox(height: 8),
          Text(
            'Ana sayfadan prompt girerek başla',
            style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                  color: AppColors.textTertiary,
                ),
          ),
        ],
      ),
    );
  }
}

// ── Product Bottom Sheet ──────────────────────────────────────────────────────

class _ProductBottomSheet extends StatelessWidget {
  final Map<String, dynamic> category;
  final List<Map<String, dynamic>> products;

  const _ProductBottomSheet({
    required this.category,
    required this.products,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      height: MediaQuery.of(context).size.height * 0.6,
      decoration: BoxDecoration(
        gradient: LinearGradient(
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
          colors: [
            AppColors.surfaceDark,
            AppColors.darkNavy,
          ],
        ),
        borderRadius: const BorderRadius.vertical(top: Radius.circular(24)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Handle
          Center(
            child: Container(
              margin: const EdgeInsets.only(top: 12),
              width: 40,
              height: 4,
              decoration: BoxDecoration(
                color: AppColors.glassBorder,
                borderRadius: BorderRadius.circular(2),
              ),
            ),
          ),
          const SizedBox(height: 16),

          // Category title
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 24),
            child: Row(
              children: [
                Text(category['emoji'] ?? '📦', style: const TextStyle(fontSize: 24)),
                const SizedBox(width: 12),
                Text(
                  category['name'] ?? '',
                  style: Theme.of(context).textTheme.headlineMedium,
                ),
              ],
            ),
          ),
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 24),
            child: Text(
              'Bütçe: ${category['estimated_budget'] ?? ''}',
              style: Theme.of(context).textTheme.bodySmall?.copyWith(
                    color: AppColors.amberGold,
                  ),
            ),
          ),
          const SizedBox(height: 20),

          // Product list
          Expanded(
            child: ListView.separated(
              padding: const EdgeInsets.symmetric(horizontal: 24),
              itemCount: products.length,
              separatorBuilder: (_, _) => const SizedBox(height: 12),
              itemBuilder: (context, index) {
                final product = products[index];
                return ProductCard(
                  name: product['name'] ?? '',
                  price: (product['price'] ?? 0).toDouble(),
                  platform: product['platform'] ?? '',
                  rating: (product['rating'] ?? 0).toDouble(),
                  reviewCount: product['review_count'] ?? 0,
                );
              },
            ),
          ),
        ],
      ),
    );
  }
}

// ── Chat Panel ───────────────────────────────────────────────────────────────

class _ChatPanel extends StatefulWidget {
  final Map<String, dynamic> category;

  const _ChatPanel({required this.category});

  @override
  State<_ChatPanel> createState() => _ChatPanelState();
}

class _ChatPanelState extends State<_ChatPanel> {
  final TextEditingController _controller = TextEditingController();
  final List<Map<String, String>> _messages = [];

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  void _sendMessage() {
    final text = _controller.text.trim();
    if (text.isEmpty) return;

    setState(() {
      _messages.add({'role': 'user', 'content': text});
      _messages.add({
        'role': 'ai',
        'content': 'Bu kategori özelinde yardımcı oluyorum. Şu an mock yanıt — backend bağlandığında gerçek AI yanıtı gelecek.',
      });
      _controller.clear();
    });
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      height: MediaQuery.of(context).size.height * 0.65,
      decoration: BoxDecoration(
        gradient: LinearGradient(
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
          colors: [AppColors.surfaceDark, AppColors.darkNavy],
        ),
        borderRadius: const BorderRadius.vertical(top: Radius.circular(24)),
      ),
      child: Column(
        children: [
          // Handle + title
          Center(
            child: Container(
              margin: const EdgeInsets.only(top: 12),
              width: 40, height: 4,
              decoration: BoxDecoration(
                color: AppColors.glassBorder,
                borderRadius: BorderRadius.circular(2),
              ),
            ),
          ),
          Padding(
            padding: const EdgeInsets.all(16),
            child: Row(
              children: [
                Text(widget.category['emoji'] ?? '', style: const TextStyle(fontSize: 20)),
                const SizedBox(width: 8),
                Text(
                  '${widget.category['name'] ?? ''} - Sohbet',
                  style: Theme.of(context).textTheme.titleLarge,
                ),
              ],
            ),
          ),
          Divider(color: AppColors.glassBorder, height: 1),

          // Messages
          Expanded(
            child: _messages.isEmpty
                ? Center(
                    child: Text(
                      'Bu kategori hakkında soru sor',
                      style: TextStyle(color: AppColors.textTertiary),
                    ),
                  )
                : ListView.builder(
                    padding: const EdgeInsets.all(16),
                    itemCount: _messages.length,
                    itemBuilder: (context, index) {
                      final msg = _messages[index];
                      final isUser = msg['role'] == 'user';
                      return Align(
                        alignment: isUser ? Alignment.centerRight : Alignment.centerLeft,
                        child: Container(
                          margin: const EdgeInsets.only(bottom: 8),
                          padding: const EdgeInsets.symmetric(
                            horizontal: 16, vertical: 12,
                          ),
                          decoration: BoxDecoration(
                            color: isUser
                                ? AppColors.deepTeal.withValues(alpha: 0.3)
                                : AppColors.glassMedium,
                            borderRadius: BorderRadius.circular(16).copyWith(
                              bottomRight: isUser ? const Radius.circular(4) : null,
                              bottomLeft: !isUser ? const Radius.circular(4) : null,
                            ),
                          ),
                          constraints: BoxConstraints(
                            maxWidth: MediaQuery.of(context).size.width * 0.75,
                          ),
                          child: Text(
                            msg['content'] ?? '',
                            style: Theme.of(context).textTheme.bodyMedium,
                          ),
                        ),
                      );
                    },
                  ),
          ),

          // Input
          Padding(
            padding: const EdgeInsets.all(16),
            child: Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _controller,
                    style: Theme.of(context).textTheme.bodyMedium,
                    decoration: const InputDecoration(
                      hintText: 'Sorunu yaz...',
                    ),
                    onSubmitted: (_) => _sendMessage(),
                  ),
                ),
                const SizedBox(width: 8),
                IconButton(
                  onPressed: _sendMessage,
                  icon: const Icon(Icons.send_rounded, color: AppColors.mintActive),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
