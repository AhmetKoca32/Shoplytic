import 'package:flutter/material.dart';

class FavoritesScreen extends StatefulWidget {
  const FavoritesScreen({Key? key}) : super(key: key);

  @override
  State<FavoritesScreen> createState() => _FavoritesScreenState();
}

class _FavoritesScreenState extends State<FavoritesScreen>
    with TickerProviderStateMixin {
  late AnimationController _animationController;
  late Animation<double> _fadeAnimation;

  final List<Map<String, dynamic>> _favoriteItems = [
    {
      'name': 'Laptop Stand',
      'category': 'Teknoloji',
      'price': '₺299',
      'rating': 4.8,
      'image': '💻',
      'isFavorite': true,
    },
    {
      'name': 'Kışlık Mont',
      'category': 'Kıyafet',
      'price': '₺899',
      'rating': 4.6,
      'image': '🧥',
      'isFavorite': true,
    },
    {
      'name': 'Yatak Takımı',
      'category': 'Ev Eşyaları',
      'price': '₺450',
      'rating': 4.9,
      'image': '🛏️',
      'isFavorite': true,
    },
    {
      'name': 'Akıllı Telefon',
      'category': 'Teknoloji',
      'price': '₺12,999',
      'rating': 4.7,
      'image': '📱',
      'isFavorite': true,
    },
    {
      'name': 'Kitap Seti',
      'category': 'Kitap & Kırtasiye',
      'price': '₺180',
      'rating': 4.5,
      'image': '📚',
      'isFavorite': true,
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
                              'Favoriler',
                              style: TextStyle(
                                fontSize: 24,
                                fontWeight: FontWeight.bold,
                                color: Colors.white,
                              ),
                            ),
                            Spacer(),
                            IconButton(
                              onPressed: () {
                                // TODO: Implement sort
                              },
                              icon: Icon(Icons.sort, color: Colors.white),
                            ),
                          ],
                        ),
                      ),

                      // Stats
                      Container(
                        padding: EdgeInsets.symmetric(horizontal: 20),
                        child: Row(
                          children: [
                            Expanded(
                              child: _buildStatCard(
                                title: 'Toplam Favori',
                                value: '${_favoriteItems.length}',
                                icon: Icons.favorite,
                              ),
                            ),
                            SizedBox(width: 12),
                            Expanded(
                              child: _buildStatCard(
                                title: 'Kategoriler',
                                value:
                                    '${_favoriteItems.map((item) => item['category']).toSet().length}',
                                icon: Icons.category,
                              ),
                            ),
                          ],
                        ),
                      ),

                      SizedBox(height: 24),

                      // Favorites Grid
                      Expanded(
                        child: _favoriteItems.isEmpty
                            ? _buildEmptyState()
                            : GridView.builder(
                                padding: EdgeInsets.symmetric(horizontal: 20),
                                gridDelegate:
                                    SliverGridDelegateWithFixedCrossAxisCount(
                                      crossAxisCount: 2,
                                      childAspectRatio: 0.8,
                                      crossAxisSpacing: 12,
                                      mainAxisSpacing: 12,
                                    ),
                                itemCount: _favoriteItems.length,
                                itemBuilder: (context, index) {
                                  final item = _favoriteItems[index];
                                  return _buildFavoriteCard(item, index);
                                },
                              ),
                      ),

                      SizedBox(height: 20),
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

  Widget _buildStatCard({
    required String title,
    required String value,
    required IconData icon,
  }) {
    return Container(
      padding: EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.white.withOpacity(0.1),
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: Colors.white.withOpacity(0.2)),
      ),
      child: Column(
        children: [
          Container(
            padding: EdgeInsets.all(8),
            decoration: BoxDecoration(
              color: Color(0xFFe94560).withOpacity(0.2),
              borderRadius: BorderRadius.circular(12),
            ),
            child: Icon(icon, color: Color(0xFFe94560), size: 24),
          ),
          SizedBox(height: 8),
          Text(
            value,
            style: TextStyle(
              fontSize: 24,
              fontWeight: FontWeight.bold,
              color: Colors.white,
            ),
          ),
          Text(
            title,
            style: TextStyle(
              fontSize: 12,
              color: Colors.white.withOpacity(0.7),
            ),
            textAlign: TextAlign.center,
          ),
        ],
      ),
    );
  }

  Widget _buildFavoriteCard(Map<String, dynamic> item, int index) {
    return Container(
      decoration: BoxDecoration(
        color: Colors.white.withOpacity(0.1),
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: Colors.white.withOpacity(0.2)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Product Image
          Container(
            height: 120,
            decoration: BoxDecoration(
              color: _getCategoryColor(item['category']).withOpacity(0.2),
              borderRadius: BorderRadius.only(
                topLeft: Radius.circular(16),
                topRight: Radius.circular(16),
              ),
            ),
            child: Center(
              child: Text(item['image'], style: TextStyle(fontSize: 48)),
            ),
          ),

          // Product Info
          Padding(
            padding: EdgeInsets.all(12),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  children: [
                    Expanded(
                      child: Text(
                        item['name'],
                        style: TextStyle(
                          color: Colors.white,
                          fontWeight: FontWeight.w600,
                          fontSize: 14,
                        ),
                        maxLines: 1,
                        overflow: TextOverflow.ellipsis,
                      ),
                    ),
                    GestureDetector(
                      onTap: () {
                        setState(() {
                          _favoriteItems[index]['isFavorite'] =
                              !item['isFavorite'];
                        });
                      },
                      child: Icon(
                        item['isFavorite']
                            ? Icons.favorite
                            : Icons.favorite_border,
                        color: item['isFavorite']
                            ? Color(0xFFe94560)
                            : Colors.white.withOpacity(0.6),
                        size: 20,
                      ),
                    ),
                  ],
                ),

                SizedBox(height: 4),

                Text(
                  item['category'],
                  style: TextStyle(
                    color: Colors.white.withOpacity(0.7),
                    fontSize: 12,
                  ),
                ),

                SizedBox(height: 8),

                Row(
                  children: [
                    Icon(Icons.star, color: Colors.amber, size: 16),
                    SizedBox(width: 4),
                    Text(
                      '${item['rating']}',
                      style: TextStyle(
                        color: Colors.white,
                        fontSize: 12,
                        fontWeight: FontWeight.w500,
                      ),
                    ),
                    Spacer(),
                    Text(
                      item['price'],
                      style: TextStyle(
                        color: Color(0xFFe94560),
                        fontSize: 14,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ],
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildEmptyState() {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(
            Icons.favorite_border,
            size: 64,
            color: Colors.white.withOpacity(0.6),
          ),
          SizedBox(height: 16),
          Text(
            'Henüz favori ürününüz yok',
            style: TextStyle(
              fontSize: 18,
              fontWeight: FontWeight.w600,
              color: Colors.white,
            ),
            textAlign: TextAlign.center,
          ),
          SizedBox(height: 8),
          Text(
            'Beğendiğiniz ürünleri favorilere ekleyerek\nburada görüntüleyebilirsiniz',
            style: TextStyle(
              fontSize: 14,
              color: Colors.white.withOpacity(0.8),
            ),
            textAlign: TextAlign.center,
          ),
        ],
      ),
    );
  }

  Color _getCategoryColor(String category) {
    switch (category.toLowerCase()) {
      case 'ev eşyaları':
        return Color(0xFFe94560);
      case 'teknoloji':
        return Color(0xFF0f0f23);
      case 'kıyafet':
        return Color(0xFF16213e);
      case 'kitap & kırtasiye':
        return Color(0xFF1a1a2e);
      default:
        return Color(0xFFe94560);
    }
  }
}
