import 'dart:math';

import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:provider/provider.dart';

import '../../../providers/mind_map_provider.dart';
import '../../../widgets/ecommerce_products_widget.dart';

class MindMapScreen extends StatefulWidget {
  const MindMapScreen({Key? key}) : super(key: key);

  @override
  State<MindMapScreen> createState() => _MindMapScreenState();
}

class _MindMapScreenState extends State<MindMapScreen>
    with TickerProviderStateMixin {
  late AnimationController _animationController;
  late AnimationController _loadingController;
  late Animation<double> _fadeAnimation;
  late Animation<double> _scaleAnimation;
  Animation<double>? _rotationAnimation;

  MindMapNode? _selectedNode;
  bool _showProducts = false;
  bool _isLoading = true;

  // Kategori merkezlerini painter'dan almak için
  Map<MindMapNode, Offset> _categoryCenters = {};

  @override
  void initState() {
    super.initState();
    _animationController = AnimationController(
      duration: const Duration(milliseconds: 800),
      vsync: this,
    );

    _loadingController = AnimationController(
      duration: const Duration(milliseconds: 2000),
      vsync: this,
    );

    _fadeAnimation = Tween<double>(begin: 0.0, end: 1.0).animate(
      CurvedAnimation(parent: _animationController, curve: Curves.easeInOut),
    );

    _scaleAnimation = Tween<double>(begin: 0.8, end: 1.0).animate(
      CurvedAnimation(parent: _animationController, curve: Curves.elasticOut),
    );

    _rotationAnimation = Tween<double>(begin: 0.0, end: 1.0).animate(
      CurvedAnimation(parent: _loadingController, curve: Curves.linear),
    );

    _startLoadingAnimation();
  }

  void _startLoadingAnimation() {
    _loadingController.repeat();
    Future.delayed(const Duration(seconds: 2), () {
      if (mounted) {
        setState(() {
          _isLoading = false;
        });
        _loadingController.stop();
        _animationController.forward();
      }
    });
  }

  @override
  void dispose() {
    _animationController.dispose();
    _loadingController.dispose();
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
                    colors: [Color(0xFF0f0f23), Color(0xFF1a1a2e)],
                  ),
                ),
              ),
              
              // Loading Screen
              if (_isLoading)
                _buildLoadingScreen()
              else
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

  Widget _buildLoadingScreen() {
    return Container(
      decoration: const BoxDecoration(
        gradient: LinearGradient(
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
          colors: [Color(0xFF0f0f23), Color(0xFF1a1a2e)],
        ),
      ),
      child: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            AnimatedBuilder(
              animation: _rotationAnimation!,
              builder: (context, child) {
                return Transform.rotate(
                  angle: _rotationAnimation!.value * 2 * 3.14159,
                  child: Container(
                    width: 80,
                    height: 80,
                    decoration: BoxDecoration(
                      gradient: LinearGradient(
                        colors: [Color(0xFFe94560), Color(0xFFc44569)],
                      ),
                      borderRadius: BorderRadius.circular(40),
                      boxShadow: [
                        BoxShadow(
                          color: Color(0xFFe94560).withOpacity(0.3),
                          blurRadius: 20,
                          offset: Offset(0, 10),
                        ),
                      ],
                    ),
                    child: Icon(
                      Icons.psychology,
                      color: Colors.white,
                      size: 40,
                    ),
                  ),
                );
              },
            ),
            SizedBox(height: 32),
            Text(
              'Zihin Haritası Oluşturuluyor...',
              style: GoogleFonts.poppins(
                fontSize: 20,
                fontWeight: FontWeight.w600,
                color: Colors.white,
              ),
            ),
            SizedBox(height: 16),
            Text(
              'AI analiz ediyor ve kategorileri belirliyor',
              style: GoogleFonts.poppins(
                fontSize: 14,
                color: Colors.white.withOpacity(0.8),
              ),
              textAlign: TextAlign.center,
            ),
          ],
        ),
      ),
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
                        // Kategori düğüm yarıçapı: 60/2 = 30 (büyütüldü)
                        if ((tap - center).distance < 65) {
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
    final items = node.items ?? [];

    // E-ticaret ürünlerini al
    final ecommerceProducts = _getEcommerceProducts(node);

    // AI önerilen ürünler için e-ticaret ürünlerinden bazılarını kullan
    final aiRecommendedProducts = ecommerceProducts
        .take(5)
        .toList(); // İlk 5 ürün

    // Eğer e-ticaret ürünleri yoksa, items'ı kullan
    final displayItems = aiRecommendedProducts.isNotEmpty
        ? aiRecommendedProducts
              .map(
                (product) => {
                  'name': product.name,
                  'price': product.price,
                  'platform': product.platform,
                  'rating': product.rating,
                  'image': product.image,
                  'description': product.description,
                },
              )
              .toList()
        : items.map((item) => {'name': item}).toList();

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
                        '${displayItems.length} ürün bulundu',
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

          // E-ticaret ürünleri
          if (ecommerceProducts.isNotEmpty)
            EcommerceProductsWidget(
              products: ecommerceProducts,
              categoryName: node.title,
            ),

          const SizedBox(height: 16),

          // AI önerilen ürünler
          Text(
            'AI Önerilen Ürünler',
            style: GoogleFonts.poppins(
              fontSize: 18,
              fontWeight: FontWeight.bold,
              color: Colors.white,
            ),
          ),

          const SizedBox(height: 8),

          // Products List
          Expanded(
            child: ListView.builder(
              itemCount: displayItems.length,
              itemBuilder: (context, index) {
                final product = displayItems[index];
                return _buildProductCard(product, index);
              },
            ),
          ),
        ],
      ),
    );
  }

  List<EcommerceProduct> _getEcommerceProducts(MindMapNode node) {
    // MindMapNode'dan e-ticaret ürünlerini al
    final ecommerceProducts = <EcommerceProduct>[];

    // Debug: Node verilerini kontrol et
    print('🔍 MindMapNode: ${node.title}');
    print('📦 Products field: ${node.products}');
    print('📦 Products length: ${node.products?.length ?? 0}');

    // Backend'den gelen products verisini kontrol et
    if (node.products != null) {
      for (final product in node.products!) {
        try {
          print('🛍️ Ürün parse ediliyor: $product');
          ecommerceProducts.add(
            EcommerceProduct(
              id: product['id'] ?? '',
              name: product['name'] ?? '',
              price: (product['price'] ?? 0).toDouble(),
              platform: product['platform'] ?? '',
              rating: (product['rating'] ?? 0.0).toDouble(),
              stock: product['stock'] ?? true,
              url: product['url'] ?? '',
              image: product['image'] ?? '',
              category: product['category'] ?? '',
              description: product['description'] ?? '',
            ),
          );
        } catch (e) {
          print('❌ Ürün parse hatası: $e');
        }
      }
    }

    print('✅ E-ticaret ürünleri sayısı: ${ecommerceProducts.length}');
    return ecommerceProducts;
  }

  Widget _buildProductCard(Map<String, dynamic> product, int index) {
    final productName = product['name'] ?? 'Ürün ${index + 1}';
    final productPrice = product['price']?.toString() ?? '';
    final productPlatform = product['platform'] ?? '';
    final productRating = product['rating']?.toString() ?? '';
    final productImage = product['image'] ?? '';

    return Container(
      margin: const EdgeInsets.only(bottom: 12),
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
                  color: const Color(0xFF1a1a2e),
                  borderRadius: BorderRadius.circular(12),
                  border: Border.all(color: Colors.white.withOpacity(0.2)),
                  boxShadow: [
                    BoxShadow(
                      color: Colors.black.withOpacity(0.3),
                      blurRadius: 8,
                      offset: const Offset(0, 4),
                    ),
                  ],
                ),
                child: Row(
                  children: [
                    // Ürün resmi
                    if (productImage.isNotEmpty)
                      Container(
                        width: 80,
                        height: 80,
                        margin: const EdgeInsets.only(right: 16),
                        decoration: BoxDecoration(
                          borderRadius: BorderRadius.circular(8),
                          color: const Color(0xFF0f0f23),
                        ),
                        child: ClipRRect(
                          borderRadius: BorderRadius.circular(8),
                          child: Image.network(
                            productImage,
                            fit: BoxFit.cover,
                            errorBuilder: (context, error, stackTrace) {
                              return const Icon(
                                Icons.image,
                                color: Colors.grey,
                                size: 30,
                              );
                            },
                          ),
                        ),
                      ),
                    // Ürün bilgileri
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            productName,
                            style: GoogleFonts.poppins(
                              fontSize: 16,
                              fontWeight: FontWeight.bold,
                              color: Colors.white,
                            ),
                            maxLines: 2,
                            overflow: TextOverflow.ellipsis,
                          ),
                          const SizedBox(height: 8),
                          Row(
                            children: [
                              if (productPrice.isNotEmpty) ...[
                                Text(
                                  '₺$productPrice',
                                  style: GoogleFonts.poppins(
                                    fontSize: 18,
                                    fontWeight: FontWeight.bold,
                                    color: const Color(0xFFe94560),
                                  ),
                                ),
                                const SizedBox(width: 16),
                              ],
                              if (productRating.isNotEmpty) ...[
                                const Icon(
                                  Icons.star,
                                  color: Colors.amber,
                                  size: 16,
                                ),
                                const SizedBox(width: 4),
                                Text(
                                  productRating,
                                  style: GoogleFonts.poppins(
                                    color: Colors.white,
                                    fontSize: 14,
                                  ),
                                ),
                              ],
                            ],
                          ),
                          const SizedBox(height: 8),
                          if (productPlatform.isNotEmpty)
                            Container(
                              padding: const EdgeInsets.symmetric(
                                horizontal: 8,
                                vertical: 4,
                              ),
                              decoration: BoxDecoration(
                                color: const Color(0xFFe94560),
                                borderRadius: BorderRadius.circular(4),
                              ),
                              child: Text(
                                productPlatform,
                                style: GoogleFonts.poppins(
                                  color: Colors.white,
                                  fontSize: 12,
                                  fontWeight: FontWeight.w500,
                                ),
                              ),
                            ),
                        ],
                      ),
                    ),
                    // Sağ ok ikonu
                    IconButton(
                      onPressed: () {
                        // Ürün detayına git
                        ScaffoldMessenger.of(context).showSnackBar(
                          SnackBar(
                            content: Text('$productName detayları açılacak'),
                            backgroundColor: const Color(0xFFe94560),
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
      case 'akademik malzemeler':
        return const Color(0xFFe94560);
      case 'kırtasiye':
        return const Color(0xFF4CAF50);
      case 'teknoloji':
        return const Color(0xFF2196F3);
      case 'mobilya':
        return const Color(0xFFFF9800);
      case 'ev tekstili':
        return const Color(0xFF9C27B0);
      case 'yazıcı & tarayıcı':
        return const Color(0xFF607D8B);
      case 'ev eşyaları':
        return const Color(0xFFe94560);
      case 'kıyafet':
        return const Color(0xFF16213e);
      case 'kitap & kırtasiye':
        return const Color(0xFF1a1a2e);
      case 'temel ihtiyaçlar':
        return const Color(0xFF607D8B);
      case 'öneriler':
        return const Color(0xFF795548);
      default:
        return const Color(0xFFe94560);
    }
  }

  IconData _getCategoryIcon(String category) {
    switch (category.toLowerCase()) {
      case 'akademik malzemeler':
        return Icons.school;
      case 'kırtasiye':
        return Icons.edit;
      case 'teknoloji':
        return Icons.computer;
      case 'mobilya':
        return Icons.chair;
      case 'ev tekstili':
        return Icons.bed;
      case 'yazıcı & tarayıcı':
        return Icons.print;
      case 'ev eşyaları':
        return Icons.home;
      case 'kıyafet':
        return Icons.checkroom;
      case 'kitap & kırtasiye':
        return Icons.book;
      case 'temel ihtiyaçlar':
        return Icons.shopping_cart;
      case 'öneriler':
        return Icons.recommend;
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
    final radius = size.width * 0.4; // Mesafeyi artırdık: 0.3 -> 0.4

    // Ana düğüm (merkez)
    _drawCenterNode(canvas, center, 'Üniversite Hazırlığı');

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
      center: center,
      width: 140,
      height: 70, // Ana düğümü büyüttük
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
    _drawText(
      canvas,
      center,
      title,
      Colors.black,
      18,
      FontWeight.bold,
    ); // Ana düğüm yazı boyutunu artırdık
  }

  void _drawCategoryNode(Canvas canvas, Offset center, MindMapNode category) {
    final rect = Rect.fromCenter(
      center: center,
      width: 120,
      height: 60, // Kategori düğümlerini büyüttük
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
      16, // Kategori yazı boyutunu artırdık
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
        return const Color(0xFFe94560);
      case 'teknoloji':
        return const Color(0xFF0f0f23);
      case 'kıyafet':
        return const Color(0xFF16213e);
      case 'kitap & kırtasiye':
        return const Color(0xFF1a1a2e);
      default:
        return const Color(0xFFe94560);
    }
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => true;
}
