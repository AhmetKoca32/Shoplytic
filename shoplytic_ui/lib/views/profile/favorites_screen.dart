import 'package:flutter/material.dart';
import '../../theme/app_colors.dart';
import '../../widgets/product_card.dart';

class FavoritesScreen extends StatelessWidget {
  const FavoritesScreen({super.key});

  final List<Map<String, dynamic>> _favorites = const [
    {'name': 'Lenovo ThinkPad E15', 'price': 15999.99, 'platform': 'Trendyol', 'rating': 4.5, 'review_count': 1250},
    {'name': 'Logitech Mouse', 'price': 599.99, 'platform': 'Trendyol', 'rating': 4.7, 'review_count': 3200},
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      extendBody: true,
      body: Container(
        decoration: const BoxDecoration(gradient: AppColors.backgroundDark),
        child: SafeArea(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Padding(
                padding: const EdgeInsets.fromLTRB(24, 16, 24, 8),
                child: Row(
                  children: [
                    IconButton(
                      icon: const Icon(Icons.arrow_back, color: AppColors.textPrimary),
                      onPressed: () => Navigator.pop(context),
                    ),
                    const SizedBox(width: 8),
                    Text('Favoriler', style: Theme.of(context).textTheme.headlineLarge),
                  ],
                ),
              ),
              Expanded(
                child: ListView.separated(
                  padding: const EdgeInsets.all(16),
                  itemCount: _favorites.length,
                  separatorBuilder: (_, _) => const SizedBox(height: 12),
                  itemBuilder: (context, index) {
                    final item = _favorites[index];
                    return ProductCard(
                      name: item['name'] ?? '',
                      price: (item['price'] ?? 0).toDouble(),
                      platform: item['platform'] ?? '',
                      rating: (item['rating'] ?? 0).toDouble(),
                      reviewCount: item['review_count'] ?? 0,
                    );
                  },
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
