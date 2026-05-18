import 'package:flutter/material.dart';
import '../../theme/app_colors.dart';
import '../../widgets/glass_card.dart';

class LegalScreen extends StatefulWidget {
  const LegalScreen({super.key});

  @override
  State<LegalScreen> createState() => _LegalScreenState();
}

class _LegalScreenState extends State<LegalScreen>
    with SingleTickerProviderStateMixin {
  late TabController _tabController;

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 3, vsync: this);
  }

  @override
  void dispose() {
    _tabController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.transparent,
      body: SafeArea(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Header
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 16),
              child: Text(
                'Tüketici Hakları',
                style: Theme.of(context).textTheme.headlineLarge,
              ),
            ),

            // Tab bar
            Container(
              margin: const EdgeInsets.symmetric(horizontal: 16),
              decoration: BoxDecoration(
                color: AppColors.glassMedium,
                borderRadius: BorderRadius.circular(12),
              ),
              child: TabBar(
                controller: _tabController,
                indicator: BoxDecoration(
                  color: AppColors.legalAgent.withValues(alpha: 0.3),
                  borderRadius: BorderRadius.circular(12),
                ),
                labelColor: AppColors.legalAgent,
                unselectedLabelColor: AppColors.textSecondary,
                labelStyle: TextStyle(
                  fontWeight: FontWeight.w600,
                  fontSize: 13,
                ),
                tabs: const [
                  Tab(text: 'Şikayet Gir'),
                  Tab(text: 'Kanun Maddeleri'),
                  Tab(text: 'Dilekçe'),
                ],
              ),
            ),

            // Tab bar view
            Expanded(
              child: TabBarView(
                controller: _tabController,
                children: [
                  _ComplaintTab(),
                  _LawArticlesTab(),
                  _PetitionTab(),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}

// ── Şikayet Gir Tab ──────────────────────────────────────────────────────────

class _ComplaintTab extends StatefulWidget {
  @override
  State<_ComplaintTab> createState() => _ComplaintTabState();
}

class _ComplaintTabState extends State<_ComplaintTab> {
  final TextEditingController _controller = TextEditingController();
  bool _showResult = false;

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  void _analyze() {
    setState(() => _showResult = true);
  }

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          GlassCard(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  'Şikayetini Detaylıca Yaz',
                  style: Theme.of(context).textTheme.titleMedium,
                ),
                const SizedBox(height: 12),
                TextField(
                  controller: _controller,
                  maxLines: 6,
                  style: Theme.of(context).textTheme.bodyMedium,
                  decoration: const InputDecoration(
                    hintText: 'Aldığım ürün ayıplı çıktı, iade etmek istiyorum...',
                  ),
                ),
                const SizedBox(height: 16),
                SizedBox(
                  width: double.infinity,
                  child: ElevatedButton(
                    onPressed: _analyze,
                    style: ElevatedButton.styleFrom(
                      backgroundColor: AppColors.legalAgent,
                    ),
                    child: const Text('Analiz Et'),
                  ),
                ),
              ],
            ),
          ),

          if (_showResult) ...[
            const SizedBox(height: 16),
            GlassCard(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      Icon(Icons.gavel, color: AppColors.legalAgent, size: 20),
                      const SizedBox(width: 8),
                      Text('Analiz Sonucu', style: Theme.of(context).textTheme.titleMedium),
                    ],
                  ),
                  const SizedBox(height: 12),
                  _resultItem('İhlal Edilen Madde', '6502 Sayılı Kanun Madde 4 - Ayıplı Mal'),
                  const SizedBox(height: 8),
                  _resultItem('Hakların', 'Malın iadesi, bedel iadesi veya ayıp oranında indirim'),
                  const SizedBox(height: 8),
                  _resultItem('Başvuru', 'Tüketici Hakem Heyeti, Ticaret Bakanlığı'),
                ],
              ),
            ),
          ],
        ],
      ),
    );
  }

  Widget _resultItem(String label, String value) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          label,
          style: TextStyle(
            color: AppColors.legalAgent.withValues(alpha: 0.7),
            fontSize: 12,
            fontWeight: FontWeight.w600,
          ),
        ),
        const SizedBox(height: 4),
        Text(
          value,
          style: Theme.of(context).textTheme.bodyMedium,
        ),
      ],
    );
  }
}

// ── Kanun Maddeleri Tab ──────────────────────────────────────────────────────

class _LawArticlesTab extends StatelessWidget {
  final List<Map<String, String>> _articles = const [
    {
      'article': 'Madde 4',
      'title': 'Ayıplı Mal',
      'content': 'Satıcı, ayıplı maldan sorumludur. Tüketici seçimlik haklara sahiptir: malın iadesi, bedel iadesi, ayıp oranında bedel indirimi.',
    },
    {
      'article': 'Madde 8',
      'title': 'Cayma Hakkı',
      'content': 'Tüketici, mesafeli sözleşmelerde 14 gün içinde hiçbir gerekçe göstermeksizin ve cezai şart ödemeksizin cayma hakkına sahiptir.',
    },
    {
      'article': 'Madde 12',
      'title': 'Taksitli Satışlar',
      'content': 'Tüketici, taksitli satışlarda borcun tamamını veya bir kısmını erken ödeme hakkına sahiptir.',
    },
    {
      'article': 'Madde 48/A',
      'title': 'Garanti Belgesi',
      'content': 'Garanti belgesi ile satılan malların tamir süresi 20 iş gününü geçemez.',
    },
  ];

  @override
  Widget build(BuildContext context) {
    return ListView.separated(
      padding: const EdgeInsets.all(16),
      itemCount: _articles.length,
      separatorBuilder: (_, _) => const SizedBox(height: 12),
      itemBuilder: (context, index) {
        final article = _articles[index];
        return GlassCard(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                children: [
                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                    decoration: BoxDecoration(
                      color: AppColors.legalAgent.withValues(alpha: 0.2),
                      borderRadius: BorderRadius.circular(6),
                    ),
                    child: Text(
                      article['article'] ?? '',
                      style: TextStyle(
                        color: AppColors.legalAgent,
                        fontWeight: FontWeight.w600,
                        fontSize: 12,
                      ),
                    ),
                  ),
                  const SizedBox(width: 8),
                  Text(
                    article['title'] ?? '',
                    style: Theme.of(context).textTheme.titleMedium,
                  ),
                ],
              ),
              const SizedBox(height: 8),
              Text(
                article['content'] ?? '',
                style: Theme.of(context).textTheme.bodySmall?.copyWith(
                      height: 1.4,
                    ),
              ),
            ],
          ),
        );
      },
    );
  }
}

// ── Dilekçe Tab ──────────────────────────────────────────────────────────────

class _PetitionTab extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: GlassCard(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                const Icon(Icons.description_outlined, color: AppColors.legalAgent, size: 20),
                const SizedBox(width: 8),
                Text('Dilekçe Önizleme', style: Theme.of(context).textTheme.titleMedium),
              ],
            ),
            const SizedBox(height: 16),
            Container(
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: AppColors.glassMedium,
                borderRadius: BorderRadius.circular(12),
                border: Border.all(color: AppColors.glassBorder),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  _petitionLine('TÜKETİCİ HAKEM HEYETİ BAŞKANLIĞI\'NA'),
                  const SizedBox(height: 16),
                  _petitionLine('ŞİKAYET EDEN: [Adınız ve Soyadınız]'),
                  _petitionLine('ADRES: [Adresiniz]'),
                  const SizedBox(height: 16),
                  _petitionLine('KONU: Ayıplı mal nedeniyle şikayet'),
                  const SizedBox(height: 16),
                  _petitionLine('AÇIKLAMALAR:'),
                  const SizedBox(height: 8),
                  _petitionLine('... Şikayet detayları otomatik olarak doldurulacak ...'),
                  const SizedBox(height: 16),
                  _petitionLine('HUKUKİ DAYANAK: 6502 Sayılı Tüketicinin Korunması Hakkında Kanun'),
                  const SizedBox(height: 16),
                  _petitionLine('SONUÇ VE TALEP: Yukarıda açıklanan nedenlerle talebimin kabulüne karar verilmesini arz ederim.'),
                ],
              ),
            ),
            const SizedBox(height: 16),
            SizedBox(
              width: double.infinity,
              child: ElevatedButton.icon(
                onPressed: () {},
                icon: const Icon(Icons.download, size: 18),
                label: const Text('PDF Olarak İndir'),
                style: ElevatedButton.styleFrom(
                  backgroundColor: AppColors.legalAgent,
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _petitionLine(String text) {
    return Text(
      text,
      style: TextStyle(
        fontFamily: 'JetBrainsMono',
        fontSize: 11,
        color: AppColors.textSecondary,
        height: 1.5,
      ),
    );
  }
}
