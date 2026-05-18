import 'dart:math';
import 'package:flutter/material.dart';
import '../theme/app_colors.dart';

/// Interactive mind map widget.
/// Displays categories radiating from a central node.
class MindMapWidget extends StatelessWidget {
  final Map<String, dynamic> data;
  final void Function(Map<String, dynamic> node) onNodeTap;
  final void Function(Map<String, dynamic> node) onNodeLongPress;

  const MindMapWidget({
    super.key,
    required this.data,
    required this.onNodeTap,
    required this.onNodeLongPress,
  });

  @override
  Widget build(BuildContext context) {
    final categories = (data['main_categories'] as List<dynamic>?)
            ?.cast<Map<String, dynamic>>() ??
        [];

    return InteractiveViewer(
      minScale: 0.3,
      maxScale: 3.0,
      boundaryMargin: const EdgeInsets.all(200),
      child: SizedBox(
        width: 600,
        height: 600,
        child: CustomPaint(
          painter: _ConnectionPainter(
            categories: categories,
            color: AppColors.deepTeal.withValues(alpha: 0.3),
          ),
          child: Stack(
            children: [
              // Center node
              Center(
                child: _buildNode(
                  emoji: '🎯',
                  label: data['central_topic'] ?? '',
                  color: AppColors.mindMapAgent,
                  isCenter: true,
                ),
              ),

              // Category nodes radiating from center
              ..._buildCategoryNodes(categories),
            ],
          ),
        ),
      ),
    );
  }

  List<Widget> _buildCategoryNodes(List<Map<String, dynamic>> categories) {
    final random = Random(42); // Fixed seed for consistent layout
    final nodes = <Widget>[];

    for (int i = 0; i < categories.length; i++) {
      final cat = categories[i];
      final angle = (2 * pi * i) / categories.length + pi / 2;
      final distance = 180.0 + (random.nextDouble() * 20);
      final x = 300 + distance * cos(angle) - 60;
      final y = 300 + distance * sin(angle) - 40;

      // Determine color based on priority
      Color nodeColor;
      switch (cat['priority']) {
        case 'high':
          nodeColor = AppColors.legalAgent;
          break;
        case 'medium':
          nodeColor = AppColors.amberGold;
          break;
        default:
          nodeColor = AppColors.mindMapAgent;
      }

      nodes.add(
        Positioned(
          left: x,
          top: y,
          child: _buildNode(
            emoji: cat['emoji'] ?? '📦',
            label: cat['name'] ?? '',
            color: nodeColor,
            isCenter: false,
            onTap: () => onNodeTap(cat),
            onLongPress: () => onNodeLongPress(cat),
          ),
        ),
      );
    }

    return nodes;
  }

  Widget _buildNode({
    required String emoji,
    required String label,
    required Color color,
    bool isCenter = false,
    VoidCallback? onTap,
    VoidCallback? onLongPress,
  }) {
    return GestureDetector(
      onTap: onTap,
      onLongPress: onLongPress,
      child: Container(
        width: isCenter ? 120 : 100,
        padding: const EdgeInsets.all(8),
        decoration: BoxDecoration(
          color: color.withValues(alpha: 0.15),
          borderRadius: BorderRadius.circular(isCenter ? 60 : 16),
          border: Border.all(
            color: color.withValues(alpha: 0.4),
            width: isCenter ? 2 : 1,
          ),
          boxShadow: [
            BoxShadow(
              color: color.withValues(alpha: 0.15),
              blurRadius: 12,
              spreadRadius: 2,
            ),
          ],
        ),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Text(emoji, style: TextStyle(fontSize: isCenter ? 32 : 24)),
            const SizedBox(height: 4),
            Text(
              label,
              textAlign: TextAlign.center,
              maxLines: 2,
              overflow: TextOverflow.ellipsis,
              style: TextStyle(
                color: Colors.white.withValues(alpha: 0.9),
                fontSize: isCenter ? 12 : 10,
                fontWeight: isCenter ? FontWeight.w600 : FontWeight.w500,
              ),
            ),
          ],
        ),
      ),
    );
  }
}

// ── Connection Painter ────────────────────────────────────────────────────────

class _ConnectionPainter extends CustomPainter {
  final List<Map<String, dynamic>> categories;
  final Color color;

  _ConnectionPainter({required this.categories, required this.color});

  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()
      ..color = color
      ..strokeWidth = 1.5
      ..style = PaintingStyle.stroke;

    final center = Offset(size.width / 2, size.height / 2);
    final random = Random(42);

    for (int i = 0; i < categories.length; i++) {
      final angle = (2 * pi * i) / categories.length + pi / 2;
      final distance = 180.0 + (random.nextDouble() * 20);
      final endX = center.dx + distance * cos(angle);
      final endY = center.dy + distance * sin(angle);

      final end = Offset(endX, endY);

      // Draw curved line
      final controlX = (center.dx + end.dx) / 2;
      final controlY = (center.dy + end.dy) / 2 - 20;
      final control = Offset(controlX, controlY);

      final path = Path()
        ..moveTo(center.dx, center.dy)
        ..quadraticBezierTo(control.dx, control.dy, end.dx, end.dy);

      canvas.drawPath(path, paint);
    }
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => false;
}
