import 'dart:math';

import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:provider/provider.dart';

import '../../../providers/mind_map_provider.dart';

class MindMapScreen extends StatefulWidget {
  const MindMapScreen({Key? key}) : super(key: key);

  @override
  State<MindMapScreen> createState() => _MindMapScreenState();
}

class _MindMapScreenState extends State<MindMapScreen>
    with TickerProviderStateMixin {
  late AnimationController _animationController;
  late Animation<double> _fadeAnimation;
  late Animation<double> _scaleAnimation;

  MindMapNode? _selectedNode;
  bool _showProducts = false;

  // Kategori merkezlerini painter'dan almak için
  Map<MindMapNode, Offset> _categoryCenters = {};

  @override
  void initState() {
    super.initState();
    _animationController = AnimationController(
      duration: const Duration(milliseconds: 800),
      vsync: this,
    );

    _fadeAnimation = Tween<double>(begin: 0.0, end: 1.0).animate(
      CurvedAnimation(parent: _animationController, curve: Curves.easeInOut),
    );

    _scaleAnimation = Tween<double>(begin: 0.8, end: 1.0).animate(
      CurvedAnimation(parent: _animationController, curve: Curves.elasticOut),
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
    return Consumer<MindMapProvider>(
      builder: (context, provider, _) {
        return Scaffold(
          body: Stack(
            children: [
              // Background
              Container(
                decoration: const BoxDecoration(
                  gradient: LinearGradient(
                    begin: Alignment.topLeft,
                    end: Alignment.bottomRight,
                    colors: [Color(0xFF667eea), Color(0xFF764ba2)],
                  ),
                ),
              ),
              
              // Content
              SafeArea(
                child: Column(
                  children: [
                    // Header
                    _buildHeader(provider),

                    // Mind Map Content
                    Expanded(
                      child: _showProducts && _selectedNode != null
                          ? _buildProductList(_selectedNode!)
                          : _buildMindMapWithGesture(provider),
                    ),
                  ],
                ),
              ),
            ],
          ),
        );
      },
    );
  }

  Widget _buildHeader(MindMapProvider provider) {
    return Container(
      padding: const EdgeInsets.all(16),
      child: Row(
        children: [
          // Back Button
          if (_showProducts)
            IconButton(
              onPressed: () {
                setState(() {
                  _showProducts = false;
                  _selectedNode = null;
                });
              },
              icon: const Icon(Icons.arrow_back, color: Colors.white),
            ),
          
          // Title
          Expanded(
            child: Text(
              _showProducts ? _selectedNode?.title ?? '' : 'Zihin Haritası',
              style: GoogleFonts.poppins(
                fontSize: 24,
                fontWeight: FontWeight.bold,
                color: Colors.white,
              ),
            ),
          ),

          // Action Buttons
          if (!_showProducts) ...[
            IconButton(
              onPressed: () {
                provider.clearError();
                Navigator.pop(context);
              },
              icon: const Icon(Icons.refresh, color: Colors.white),
            ),
            IconButton(
              onPressed: () => Navigator.pop(context),
              icon: const Icon(Icons.close, color: Colors.white),
            ),
          ],
        ],
      ),
    );
  }

  Widget _buildMindMapWithGesture(MindMapProvider provider) {
    final categories = provider.root.children;
    return LayoutBuilder(
      builder: (context, constraints) {
        final width = constraints.maxWidth * 0.9;
        final height = constraints.maxHeight * 0.7;
        return Center(
          child: SizedBox(
            width: width,
            height: height,
            child: Stack(
              children: [
                // Mind map çizimi
                CustomPaint(
                  painter: ModernMindMapPainter(
                    categories: categories,
                    categoryCenters: _categoryCenters,
                  ),
                  size: Size(width, height),
                ),
                // Gesture layer
                Positioned.fill(
                  child: GestureDetector(
                    onTapUp: (details) {
                      final tap = details.localPosition;
                      for (final entry in _categoryCenters.entries) {
                        final center = entry.value;
                        // Kategori düğüm yarıçapı: 50/2 = 25
                        if ((tap - center).distance < 55) {
                          setState(() {
                            _selectedNode = entry.key;
                            _showProducts = true;
                          });
                          break;
                        }
                      }
                    },
                    child: Container(color: Colors.transparent),
                  ),
                ),
              ],
            ),
          ),
        );
      },
    );
  }



  Widget _buildProductList(MindMapNode node) {
    final products = node.products ?? [];

    return Container(
      margin: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Category Info
          Container(
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(
              color: Colors.white.withOpacity(0.1),
              borderRadius: BorderRadius.circular(12),
            ),
            child: Row(
              children: [
                Container(
                  padding: const EdgeInsets.all(8),
                  decoration: BoxDecoration(
                    color: _getCategoryColor(node.title),
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: Icon(
                    _getCategoryIcon(node.title),
                    color: Colors.white,
                    size: 24,
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        node.title,
                        style: GoogleFonts.poppins(
                          fontSize: 20,
                          fontWeight: FontWeight.bold,
                          color: Colors.white,
                        ),
                      ),
                      Text(
                        '${products.length} ürün bulundu',
                        style: GoogleFonts.poppins(
                          fontSize: 14,
                          color: Colors.white70,
                        ),
                      ),
                    ],
                  ),
                ),
                Container(
                  padding: const EdgeInsets.symmetric(
                    horizontal: 8,
                    vertical: 4,
                  ),
                  decoration: BoxDecoration(
                    color: Colors.white.withOpacity(0.2),
                    borderRadius: BorderRadius.circular(12),
                  ),
                  child: Text(
                    'Öncelik: ${node.priority ?? 1}',
                    style: GoogleFonts.poppins(
                      fontSize: 12,
                      color: Colors.white,
                      fontWeight: FontWeight.w500,
                    ),
                  ),
                ),
              ],
            ),
          ),

          const SizedBox(height: 16),

          // Products List
          Expanded(
            child: ListView.builder(
              itemCount: products.length,
              itemBuilder: (context, index) {
                final product = products[index];
                return _buildProductCard(product, index);
              },
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildProductCard(String product, int index) {
    return Container(
      margin: const EdgeInsets.only(bottom: 8),
      child: AnimatedBuilder(
        animation: _animationController,
        builder: (context, child) {
          return Transform.translate(
            offset: Offset(0, 50 * (1 - _fadeAnimation.value)),
            child: Opacity(
              opacity: _fadeAnimation.value,
              child: Container(
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: Colors.white.withOpacity(0.1),
                  borderRadius: BorderRadius.circular(12),
                  border: Border.all(color: Colors.white.withOpacity(0.2)),
                ),
                child: Row(
                  children: [
                    Container(
                      width: 40,
                      height: 40,
                      decoration: BoxDecoration(
                        color: _getCategoryColor(_selectedNode?.title ?? ''),
                        borderRadius: BorderRadius.circular(8),
                      ),
                      child: Center(
                        child: Text(
                          '${index + 1}',
                          style: GoogleFonts.poppins(
                            color: Colors.white,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                      ),
                    ),
                    const SizedBox(width: 12),
                    Expanded(
                      child: Text(
                        product,
                        style: GoogleFonts.poppins(
                          fontSize: 16,
                          color: Colors.white,
                          fontWeight: FontWeight.w500,
                        ),
                      ),
                    ),
                    IconButton(
                      onPressed: () {
                        // TODO: Ürün detayına git
                        ScaffoldMessenger.of(context).showSnackBar(
                          SnackBar(
                            content: Text('$product detayları açılacak'),
                            backgroundColor: _getCategoryColor(
                              _selectedNode?.title ?? '',
                            ),
                          ),
                        );
                      },
                      icon: const Icon(
                        Icons.arrow_forward_ios,
                        color: Colors.white70,
                      ),
                    ),
                  ],
                ),
              ),
            ),
          );
        },
      ),
    );
  }

  Color _getCategoryColor(String category) {
    switch (category.toLowerCase()) {
      case 'ev eşyaları':
        return const Color(0xFF4CAF50);
      case 'teknoloji':
        return const Color(0xFF2196F3);
      case 'kıyafet':
        return const Color(0xFFE91E63);
      case 'kitap & kırtasiye':
        return const Color(0xFFFF9800);
      default:
        return const Color(0xFF9C27B0);
    }
  }

  IconData _getCategoryIcon(String category) {
    switch (category.toLowerCase()) {
      case 'ev eşyaları':
        return Icons.home;
      case 'teknoloji':
        return Icons.computer;
      case 'kıyafet':
        return Icons.checkroom;
      case 'kitap & kırtasiye':
        return Icons.book;
      default:
        return Icons.category;
    }
  }
}

class ModernMindMapPainter extends CustomPainter {
  final List<MindMapNode> categories;
  final Map<MindMapNode, Offset> categoryCenters;

  ModernMindMapPainter({
    required this.categories,
    required this.categoryCenters,
  });

  @override
  void paint(Canvas canvas, Size size) {
    final center = Offset(size.width / 2, size.height / 2);
    final radius = size.width * 0.3;

    // Ana düğüm (merkez)
    _drawCenterNode(canvas, center, 'Ana Fikir');

    // Kategorileri çiz
    for (int i = 0; i < categories.length; i++) {
      final angle = (2 * pi * i) / categories.length;
      final categoryCenter = Offset(
        center.dx + radius * cos(angle),
        center.dy + radius * sin(angle),
      );
      // Bağlantı çizgisi
      _drawConnection(canvas, center, categoryCenter);
      // Kategori düğümü
      _drawCategoryNode(canvas, categoryCenter, categories[i]);
      // Merkezleri kaydet
      categoryCenters[categories[i]] = categoryCenter;
    }
  }

  void _drawCenterNode(Canvas canvas, Offset center, String title) {
    final rect = Rect.fromCenter(
      center: center, width: 120, height: 60,
    );
    
    // Gölge
    canvas.drawShadow(
      Path()
        ..addRRect(RRect.fromRectAndRadius(rect, const Radius.circular(30))),
      Colors.black.withOpacity(0.3),
      8,
      false,
    );
    
    // Ana düğüm
    canvas.drawRRect(
      RRect.fromRectAndRadius(rect, const Radius.circular(30)),
      Paint()
        ..color = Colors.white
        ..style = PaintingStyle.fill,
    );

    // Border
    canvas.drawRRect(
      RRect.fromRectAndRadius(rect, const Radius.circular(30)),
      Paint()
        ..color = Colors.white.withOpacity(0.3)
        ..style = PaintingStyle.stroke
        ..strokeWidth = 2,
    );
    
    // Text
    _drawText(canvas, center, title, Colors.black, 16, FontWeight.bold);
  }

  void _drawCategoryNode(Canvas canvas, Offset center, MindMapNode category) {
    final rect = Rect.fromCenter(center: center, width: 100, height: 50,
    );
    
    final color = _getCategoryColor(category.title);
    
    // Gölge
    canvas.drawShadow(
      Path()
        ..addRRect(RRect.fromRectAndRadius(rect, const Radius.circular(25))),
      color.withOpacity(0.3),
      6,
      false,
    );
    
    // Kategori düğümü
    canvas.drawRRect(
      RRect.fromRectAndRadius(rect, const Radius.circular(25)),
      Paint()
        ..color = color
        ..style = PaintingStyle.fill,
    );
    
    // Text
    _drawText(
      canvas,
      center,
      category.title,
      Colors.white,
      14,
      FontWeight.w600,
    );
  }

  void _drawConnection(Canvas canvas, Offset from, Offset to) {
    canvas.drawLine(
      from,
      to,
      Paint()
        ..color = Colors.white.withOpacity(0.6)
        ..strokeWidth = 3
        ..strokeCap = StrokeCap.round,
    );
  }

  void _drawText(
    Canvas canvas,
    Offset center,
    String text,
    Color color,
    double fontSize,
    FontWeight weight,
  ) {
    final textSpan = TextSpan(
      text: text,
      style: TextStyle(color: color, fontSize: fontSize, fontWeight: weight),
    );

    final textPainter = TextPainter(
      text: textSpan,
      textAlign: TextAlign.center,
      textDirection: TextDirection.ltr,
    );
    
    textPainter.layout();
    textPainter.paint(
      canvas,
      Offset(
        center.dx - textPainter.width / 2,
        center.dy - textPainter.height / 2,
      ),
    );
  }

  Color _getCategoryColor(String category) {
    switch (category.toLowerCase()) {
      case 'ev eşyaları':
        return const Color(0xFF4CAF50);
      case 'teknoloji':
        return const Color(0xFF2196F3);
      case 'kıyafet':
        return const Color(0xFFE91E63);
      case 'kitap & kırtasiye':
        return const Color(0xFFFF9800);
      default:
        return const Color(0xFF9C27B0);
    }
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => true;
}
