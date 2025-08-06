import 'package:flutter/material.dart';

class HelpScreen extends StatefulWidget {
  const HelpScreen({Key? key}) : super(key: key);

  @override
  State<HelpScreen> createState() => _HelpScreenState();
}

class _HelpScreenState extends State<HelpScreen> with TickerProviderStateMixin {
  late AnimationController _animationController;
  late Animation<double> _fadeAnimation;

  final List<Map<String, dynamic>> _faqItems = [
    {
      'question': 'Shoplytic nasıl çalışır?',
      'answer':
          'Shoplytic, hayatınızdaki değişiklikleri analiz ederek size en uygun ürün önerilerini sunar. AI teknolojisi kullanarak kişiselleştirilmiş alışveriş deneyimi yaşatır.',
      'isExpanded': false,
    },
    {
      'question': 'Zihin haritası nedir?',
      'answer':
          'Zihin haritası, ihtiyaçlarınızı kategorilere ayırarak görsel bir şekilde sunar. Bu sayede hangi ürünlere ihtiyacınız olduğunu daha kolay anlayabilirsiniz.',
      'isExpanded': false,
    },
    {
      'question': 'Ürün önerileri nasıl belirlenir?',
      'answer':
          'Ürün önerileri, bütçeniz, tercihleriniz ve mevcut durumunuz analiz edilerek belirlenir. AI algoritması en uygun seçenekleri sizin için seçer.',
      'isExpanded': false,
    },
    {
      'question': 'Fiyat karşılaştırması yapabilir miyim?',
      'answer':
          'Evet, Shoplytic farklı mağazalardan fiyat karşılaştırması yaparak en uygun fiyatlı ürünleri size sunar.',
      'isExpanded': false,
    },
    {
      'question': 'Hesabımı nasıl güvenli tutabilirim?',
      'answer':
          'Güçlü bir şifre kullanın, iki faktörlü doğrulamayı etkinleştirin ve şüpheli aktiviteleri hemen bildirin.',
      'isExpanded': false,
    },
  ];

  final List<Map<String, dynamic>> _contactOptions = [
    {
      'title': 'E-posta Desteği',
      'subtitle': '24 saat içinde yanıt',
      'icon': Icons.email,
      'action': 'support@shoplytic.com',
    },
    {
      'title': 'Canlı Sohbet',
      'subtitle': 'Anında yardım',
      'icon': Icons.chat,
      'action': 'Şimdi Başla',
    },
    {
      'title': 'Telefon Desteği',
      'subtitle': 'Pazartesi - Cuma 09:00-18:00',
      'icon': Icons.phone,
      'action': '+90 212 555 0123',
    },
  ];

  @override
  void initState() {
    super.initState();
    _animationController = AnimationController(
      duration: const Duration(milliseconds: 600),
      vsync: this,
    );
    _fadeAnimation = Tween<double>(begin: 0.0, end: 1.0).animate(
      CurvedAnimation(parent: _animationController, curve: Curves.easeOut),
    );
    _animationController.forward();
  }

  @override
  void dispose() {
    _animationController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: _fadeAnimation,
      builder: (context, child) {
        return Opacity(
          opacity: _fadeAnimation.value,
          child: Transform.translate(
            offset: Offset(0, 30 * (1 - _fadeAnimation.value)),
            child: Scaffold(
              resizeToAvoidBottomInset: false,
              backgroundColor: Colors.transparent,
              body: Container(
                decoration: BoxDecoration(
                  gradient: LinearGradient(
                    begin: Alignment.topLeft,
                    end: Alignment.bottomRight,
                    colors: [Color(0xFF0f0f23), Color(0xFF1a1a2e)],
                  ),
                ),
                child: SafeArea(
                  child: Column(
                    children: [
                      // Header
                      Container(
                        padding: EdgeInsets.all(20),
                        child: Row(
                          children: [
                            IconButton(
                              onPressed: () {
                                FocusScope.of(context).unfocus();
                                Navigator.pop(context);
                              },
                              icon: Icon(Icons.arrow_back, color: Colors.white),
                            ),
                            SizedBox(width: 16),
                            Text(
                              'Yardım & Destek',
                              style: TextStyle(
                                fontSize: 24,
                                fontWeight: FontWeight.bold,
                                color: Colors.white,
                              ),
                            ),
                          ],
                        ),
                      ),

                      Expanded(
                        child: SingleChildScrollView(
                          padding: EdgeInsets.symmetric(horizontal: 20),
                          child: Column(
                            children: [
                              // Contact Options
                              _buildSection(
                                title: 'İletişim Seçenekleri',
                                icon: Icons.contact_support,
                                children: _contactOptions
                                    .map(
                                      (option) => _buildContactOption(option),
                                    )
                                    .toList(),
                              ),

                              SizedBox(height: 24),

                              // FAQ Section
                              _buildSection(
                                title: 'Sık Sorulan Sorular',
                                icon: Icons.question_answer,
                                children: _faqItems.asMap().entries.map((
                                  entry,
                                ) {
                                  final index = entry.key;
                                  final item = entry.value;
                                  return _buildFAQItem(item, index);
                                }).toList(),
                              ),

                              SizedBox(height: 24),

                              // Quick Actions
                              _buildSection(
                                title: 'Hızlı İşlemler',
                                icon: Icons.flash_on,
                                children: [
                                  _buildQuickAction(
                                    title: 'Uygulama Hakkında',
                                    subtitle: 'Versiyon ve lisans bilgileri',
                                    icon: Icons.info,
                                    onTap: () {
                                      // TODO: Show app info
                                    },
                                  ),
                                  _buildQuickAction(
                                    title: 'Gizlilik Politikası',
                                    subtitle: 'Veri kullanımı ve gizlilik',
                                    icon: Icons.privacy_tip,
                                    onTap: () {
                                      // TODO: Show privacy policy
                                    },
                                  ),
                                  _buildQuickAction(
                                    title: 'Kullanım Şartları',
                                    subtitle: 'Hizmet şartları ve koşullar',
                                    icon: Icons.description,
                                    onTap: () {
                                      // TODO: Show terms of service
                                    },
                                  ),
                                ],
                              ),

                              SizedBox(height: 40),
                            ],
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ),
          ),
        );
      },
    );
  }

  Widget _buildSection({
    required String title,
    required IconData icon,
    required List<Widget> children,
  }) {
    return Container(
      decoration: BoxDecoration(
        color: Colors.white.withOpacity(0.1),
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: Colors.white.withOpacity(0.2)),
      ),
      child: Column(
        children: [
          // Section Header
          Container(
            padding: EdgeInsets.all(16),
            child: Row(
              children: [
                Container(
                  padding: EdgeInsets.all(8),
                  decoration: BoxDecoration(
                    color: Color(0xFFe94560).withOpacity(0.2),
                    borderRadius: BorderRadius.circular(12),
                  ),
                  child: Icon(icon, color: Color(0xFFe94560), size: 20),
                ),
                SizedBox(width: 12),
                Text(
                  title,
                  style: TextStyle(
                    fontSize: 18,
                    fontWeight: FontWeight.bold,
                    color: Colors.white,
                  ),
                ),
              ],
            ),
          ),

          // Section Content
          ...children,
        ],
      ),
    );
  }

  Widget _buildContactOption(Map<String, dynamic> option) {
    return Container(
      margin: EdgeInsets.symmetric(horizontal: 16, vertical: 4),
      decoration: BoxDecoration(
        color: Colors.white.withOpacity(0.05),
        borderRadius: BorderRadius.circular(12),
      ),
      child: Material(
        color: Colors.transparent,
        child: ListTile(
          leading: Container(
            padding: EdgeInsets.all(8),
            decoration: BoxDecoration(
              color: Color(0xFFe94560).withOpacity(0.2),
              borderRadius: BorderRadius.circular(8),
            ),
            child: Icon(option['icon'], color: Color(0xFFe94560), size: 20),
          ),
          title: Text(
            option['title'],
            style: TextStyle(
              color: Colors.white,
              fontWeight: FontWeight.w500,
              fontSize: 16,
            ),
          ),
          subtitle: Text(
            option['subtitle'],
            style: TextStyle(
              color: Colors.white.withOpacity(0.7),
              fontSize: 14,
            ),
          ),
          trailing: TextButton(
            onPressed: () {
              // TODO: Implement contact action
            },
            child: Text(
              option['action'],
              style: TextStyle(
                color: Color(0xFFe94560),
                fontWeight: FontWeight.w600,
              ),
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildFAQItem(Map<String, dynamic> item, int index) {
    return Container(
      margin: EdgeInsets.symmetric(horizontal: 16, vertical: 4),
      decoration: BoxDecoration(
        color: Colors.white.withOpacity(0.05),
        borderRadius: BorderRadius.circular(12),
      ),
      child: Material(
        color: Colors.transparent,
        child: ExpansionTile(
          title: Text(
            item['question'],
            style: TextStyle(
              color: Colors.white,
              fontWeight: FontWeight.w500,
              fontSize: 16,
            ),
          ),
          iconColor: Color(0xFFe94560),
          collapsedIconColor: Colors.white.withOpacity(0.6),
          children: [
            Container(
              padding: EdgeInsets.fromLTRB(16, 0, 16, 16),
              child: Text(
                item['answer'],
                style: TextStyle(
                  color: Colors.white.withOpacity(0.8),
                  fontSize: 14,
                  height: 1.5,
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildQuickAction({
    required String title,
    required String subtitle,
    required IconData icon,
    required VoidCallback onTap,
  }) {
    return Container(
      margin: EdgeInsets.symmetric(horizontal: 16, vertical: 4),
      decoration: BoxDecoration(
        color: Colors.white.withOpacity(0.05),
        borderRadius: BorderRadius.circular(12),
      ),
      child: Material(
        color: Colors.transparent,
        child: ListTile(
          leading: Container(
            padding: EdgeInsets.all(8),
            decoration: BoxDecoration(
              color: Color(0xFFe94560).withOpacity(0.2),
              borderRadius: BorderRadius.circular(8),
            ),
            child: Icon(icon, color: Color(0xFFe94560), size: 20),
          ),
          title: Text(
            title,
            style: TextStyle(
              color: Colors.white,
              fontWeight: FontWeight.w500,
              fontSize: 16,
            ),
          ),
          subtitle: Text(
            subtitle,
            style: TextStyle(
              color: Colors.white.withOpacity(0.7),
              fontSize: 14,
            ),
          ),
          trailing: Icon(
            Icons.arrow_forward_ios,
            color: Colors.white.withOpacity(0.6),
            size: 16,
          ),
          onTap: onTap,
        ),
      ),
    );
  }
}
