import 'package:flutter/material.dart';
import '../../theme/app_colors.dart';
import '../../widgets/glass_card.dart';

class HistoryScreen extends StatelessWidget {
  const HistoryScreen({super.key});

  final List<Map<String, String>> _history = const [
    {'prompt': 'Adana\'da üniversite kazandım, yurt için alışveriş', 'date': '12 Mayıs 2026'},
    {'prompt': 'İstanbul\'da yeni işe başlıyorum, ofis hazırlığı', 'date': '8 Mayıs 2026'},
    {'prompt': 'Evleniyorum, ev eşyası alacağım', 'date': '1 Mayıs 2026'},
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
                    Text('Geçmiş', style: Theme.of(context).textTheme.headlineLarge),
                  ],
                ),
              ),
              Expanded(
                child: ListView.separated(
                  padding: const EdgeInsets.all(16),
                  itemCount: _history.length,
                  separatorBuilder: (_, _) => const SizedBox(height: 8),
                  itemBuilder: (context, index) {
                    final item = _history[index];
                    return GlassCard(
                      child: ListTile(
                        leading: Container(
                          width: 40, height: 40,
                          decoration: BoxDecoration(
                            color: AppColors.mintActive.withValues(alpha: 0.15),
                            borderRadius: BorderRadius.circular(10),
                          ),
                          child: const Icon(Icons.history, color: AppColors.mintActive, size: 20),
                        ),
                        title: Text(item['prompt'] ?? '', style: Theme.of(context).textTheme.bodyMedium),
                        subtitle: Text(item['date'] ?? '', style: Theme.of(context).textTheme.bodySmall),
                        trailing: Icon(Icons.chevron_right, color: AppColors.textTertiary, size: 18),
                      ),
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
