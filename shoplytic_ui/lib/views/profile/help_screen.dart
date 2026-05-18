import 'package:flutter/material.dart';
import '../../theme/app_colors.dart';
import '../../widgets/glass_card.dart';

class HelpScreen extends StatelessWidget {
  const HelpScreen({super.key});

  final List<Map<String, String>> _faqs = const [
    {'q': 'Shoplytic nedir?', 'a': 'AI destekli kişiselleştirilmiş alışveriş asistanıdır. Hayatınızdaki değişiklikleri analiz ederek ihtiyaçlarınıza göre alışveriş listesi oluşturur.'},
    {'q': 'Zihin haritası nasıl çalışır?', 'a': 'Girdiğiniz prompt\'u AI analiz eder, kategorilere ayırır ve görsel bir harita oluşturur. Her kategori için ürün önerileri sunar.'},
    {'q': 'Tüketici Hakları modülü nedir?', 'a': '6502 Sayılı Tüketicinin Korunması Hakkında Kanun\'a dayanarak şikayet analizi yapar ve resmi dilekçe oluşturur.'},
    {'q': 'Verilerim güvende mi?', 'a': 'Evet, tüm verileriniz yerel olarak işlenir ve üçüncü taraflarla paylaşılmaz.'},
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
                    Text('Yardım', style: Theme.of(context).textTheme.headlineLarge),
                  ],
                ),
              ),
              Expanded(
                child: ListView.separated(
                  padding: const EdgeInsets.all(16),
                  itemCount: _faqs.length + 1,
                  separatorBuilder: (_, _) => const SizedBox(height: 8),
                  itemBuilder: (context, index) {
                    if (index == _faqs.length) {
                      return Padding(
                        padding: const EdgeInsets.only(top: 16),
                        child: Center(
                          child: Text(
                            'Shoplytic v1.0.0\nBir BTK Akademi Hackathon projesi',
                            textAlign: TextAlign.center,
                            style: TextStyle(color: AppColors.textTertiary, fontSize: 12, height: 1.5),
                          ),
                        ),
                      );
                    }
                    final faq = _faqs[index];
                    return GlassCard(
                      child: ExpansionTile(
                        title: Text(faq['q'] ?? '', style: Theme.of(context).textTheme.titleMedium),
                        children: [
                          Padding(
                            padding: const EdgeInsets.fromLTRB(16, 0, 16, 16),
                            child: Text(
                              faq['a'] ?? '',
                              style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                                    color: AppColors.textSecondary.withValues(alpha: 0.7),
                                  ),
                            ),
                          ),
                        ],
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
