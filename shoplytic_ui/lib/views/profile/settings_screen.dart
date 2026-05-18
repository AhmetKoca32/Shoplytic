import 'package:flutter/material.dart';
import '../../theme/app_colors.dart';
import '../../widgets/glass_card.dart';

class SettingsScreen extends StatefulWidget {
  const SettingsScreen({super.key});

  @override
  State<SettingsScreen> createState() => _SettingsScreenState();
}

class _SettingsScreenState extends State<SettingsScreen> {
  bool _notifications = true;
  bool _darkMode = true;

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
                    Text('Ayarlar', style: Theme.of(context).textTheme.headlineLarge),
                  ],
                ),
              ),
              Expanded(
                child: ListView(
                  padding: const EdgeInsets.all(16),
                  children: [
                    GlassCard(
                      child: SwitchListTile(
                        title: Text('Bildirimler', style: Theme.of(context).textTheme.titleMedium),
                        subtitle: Text('AI öneri bildirimleri', style: Theme.of(context).textTheme.bodySmall),
                        value: _notifications,
                        activeTrackColor: AppColors.mintActive,
                        onChanged: (v) => setState(() => _notifications = v),
                      ),
                    ),
                    const SizedBox(height: 8),
                    GlassCard(
                      child: SwitchListTile(
                        title: Text('Karanlık Tema', style: Theme.of(context).textTheme.titleMedium),
                        subtitle: Text('Varsayılan koyu tema', style: Theme.of(context).textTheme.bodySmall),
                        value: _darkMode,
                        activeTrackColor: AppColors.mintActive,
                        onChanged: (v) => setState(() => _darkMode = v),
                      ),
                    ),
                    const SizedBox(height: 8),
                    GlassCard(
                      child: ListTile(
                        leading: Container(
                          width: 44, height: 44,
                          decoration: BoxDecoration(
                            color: AppColors.amberGold.withValues(alpha: 0.15),
                            borderRadius: BorderRadius.circular(12),
                          ),
                          child: const Icon(Icons.language, color: AppColors.amberGold, size: 22),
                        ),
                        title: Text('Dil', style: Theme.of(context).textTheme.titleMedium),
                        subtitle: Text('Türkçe', style: Theme.of(context).textTheme.bodySmall),
                        trailing: Icon(Icons.chevron_right, color: AppColors.textTertiary),
                      ),
                    ),
                    const SizedBox(height: 8),
                    GlassCard(
                      child: ListTile(
                        leading: Container(
                          width: 44, height: 44,
                          decoration: BoxDecoration(
                            color: AppColors.legalAgent.withValues(alpha: 0.15),
                            borderRadius: BorderRadius.circular(12),
                          ),
                          child: const Icon(Icons.key, color: AppColors.legalAgent, size: 22),
                        ),
                        title: Text('API Key', style: Theme.of(context).textTheme.titleMedium),
                        subtitle: Text('Google Gemini API anahtarı', style: Theme.of(context).textTheme.bodySmall),
                        trailing: Icon(Icons.chevron_right, color: AppColors.textTertiary),
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
