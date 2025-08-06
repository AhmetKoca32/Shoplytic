import 'package:flutter/material.dart';

class SettingsScreen extends StatefulWidget {
  const SettingsScreen({Key? key}) : super(key: key);

  @override
  State<SettingsScreen> createState() => _SettingsScreenState();
}

class _SettingsScreenState extends State<SettingsScreen>
    with TickerProviderStateMixin {
  late AnimationController _animationController;
  late Animation<double> _fadeAnimation;

  bool _notificationsEnabled = true;
  bool _darkModeEnabled = true;
  bool _soundEnabled = false;
  String _selectedLanguage = 'Türkçe';

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
                              'Ayarlar',
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
                              // Bildirimler Bölümü
                              _buildSettingsSection(
                                title: 'Bildirimler',
                                icon: Icons.notifications,
                                children: [
                                  _buildSwitchTile(
                                    title: 'Push Bildirimleri',
                                    subtitle:
                                        'Önemli güncellemeler için bildirim al',
                                    value: _notificationsEnabled,
                                    onChanged: (value) {
                                      setState(() {
                                        _notificationsEnabled = value;
                                      });
                                    },
                                  ),
                                  _buildSwitchTile(
                                    title: 'Ses Bildirimleri',
                                    subtitle: 'Bildirimler için ses çal',
                                    value: _soundEnabled,
                                    onChanged: (value) {
                                      setState(() {
                                        _soundEnabled = value;
                                      });
                                    },
                                  ),
                                ],
                              ),

                              SizedBox(height: 24),

                              // Görünüm Bölümü
                              _buildSettingsSection(
                                title: 'Görünüm',
                                icon: Icons.palette,
                                children: [
                                  _buildSwitchTile(
                                    title: 'Koyu Tema',
                                    subtitle: 'Göz yormayan koyu tema kullan',
                                    value: _darkModeEnabled,
                                    onChanged: (value) {
                                      setState(() {
                                        _darkModeEnabled = value;
                                      });
                                    },
                                  ),
                                ],
                              ),

                              SizedBox(height: 24),

                              // Dil Bölümü
                              _buildSettingsSection(
                                title: 'Dil',
                                icon: Icons.language,
                                children: [
                                  _buildDropdownTile(
                                    title: 'Uygulama Dili',
                                    subtitle: 'Tercih ettiğiniz dili seçin',
                                    value: _selectedLanguage,
                                    items: [
                                      'Türkçe',
                                      'English',
                                      'Deutsch',
                                      'Français',
                                    ],
                                    onChanged: (value) {
                                      setState(() {
                                        _selectedLanguage = value!;
                                      });
                                    },
                                  ),
                                ],
                              ),

                              SizedBox(height: 24),

                              // Hakkında Bölümü
                              _buildSettingsSection(
                                title: 'Hakkında',
                                icon: Icons.info,
                                children: [
                                  _buildInfoTile(
                                    title: 'Uygulama Versiyonu',
                                    subtitle: 'v1.0.0',
                                  ),
                                  _buildInfoTile(
                                    title: 'Geliştirici',
                                    subtitle: 'Shoplytic Team',
                                  ),
                                  _buildInfoTile(
                                    title: 'Lisans',
                                    subtitle: 'MIT License',
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

  Widget _buildSettingsSection({
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

  Widget _buildSwitchTile({
    required String title,
    required String subtitle,
    required bool value,
    required ValueChanged<bool> onChanged,
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
          trailing: Switch(
            value: value,
            onChanged: onChanged,
            activeColor: Color(0xFFe94560),
            activeTrackColor: Color(0xFFe94560).withOpacity(0.3),
          ),
        ),
      ),
    );
  }

  Widget _buildDropdownTile({
    required String title,
    required String subtitle,
    required String value,
    required List<String> items,
    required ValueChanged<String?> onChanged,
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
          trailing: DropdownButton<String>(
            value: value,
            onChanged: onChanged,
            dropdownColor: Color(0xFF1a1a2e),
            style: TextStyle(color: Colors.white),
            underline: Container(),
            items: items.map((String item) {
              return DropdownMenuItem<String>(value: item, child: Text(item));
            }).toList(),
          ),
        ),
      ),
    );
  }

  Widget _buildInfoTile({required String title, required String subtitle}) {
    return Container(
      margin: EdgeInsets.symmetric(horizontal: 16, vertical: 4),
      decoration: BoxDecoration(
        color: Colors.white.withOpacity(0.05),
        borderRadius: BorderRadius.circular(12),
      ),
      child: Material(
        color: Colors.transparent,
        child: ListTile(
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
        ),
      ),
    );
  }
}
