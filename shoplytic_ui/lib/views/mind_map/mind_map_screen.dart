import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../../../providers/mind_map_provider.dart';

class MindMapScreen extends StatelessWidget {
  final void Function(MindMapNode node)? onNodeTap;
  const MindMapScreen({Key? key, this.onNodeTap}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Consumer<MindMapProvider>(
      builder: (context, provider, _) {
        return Stack(
          children: [
            Positioned.fill(
              child: Image.asset(
                'assets/images/login_screen_background_image.jpg',
                fit: BoxFit.cover,
              ),
            ),
            Positioned.fill(
              child: Container(color: Colors.black.withOpacity(0.4)),
            ),
            Positioned.fill(
              child: InteractiveViewer(
                minScale: 0.05,
                maxScale: 2.5,
                boundaryMargin: const EdgeInsets.all(800),
                child: MindMapCanvas(root: provider.root, onNodeTap: onNodeTap),
              ),
            ),
          ],
        );
      },
    );
  }
}

class MindMapCanvas extends StatefulWidget {
  final MindMapNode root;
  final void Function(MindMapNode node)? onNodeTap;
  const MindMapCanvas({required this.root, this.onNodeTap, Key? key})
    : super(key: key);

  @override
  State<MindMapCanvas> createState() => _MindMapCanvasState();
}

class _MindMapCanvasState extends State<MindMapCanvas> {
  // Node positions for hit testing
  final Map<MindMapNode, Rect> _nodeRects = {};

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTapUp: (details) {
        final tapPos = details.localPosition;
        for (final entry in _nodeRects.entries) {
          if (entry.value.contains(tapPos)) {
            widget.onNodeTap?.call(entry.key);
            break;
          }
        }
      },
      child: CustomPaint(
        painter: MindMapPainter(widget.root, _nodeRects),
        size: const Size(4000, 2000),
      ),
    );
  }
}

class MindMapPainter extends CustomPainter {
  final MindMapNode root;
  final Map<MindMapNode, Rect> nodeRects;
  final double nodeWidth = 120;
  final double nodeHeight = 48;
  final double verticalSpacing = 60;

  MindMapPainter(this.root, this.nodeRects);

  double _calculateTreeWidth(MindMapNode node) {
    if (node.children.isEmpty) return nodeWidth;

    double width = 0;
    for (var child in node.children) {
      width += _calculateTreeWidth(child);
    }
    width += (node.children.length - 1) * 32; // Ortalama spacing varsayım
    return width < nodeWidth ? nodeWidth : width;
  }

  double _calculateDynamicSpacing(int childCount, double availableWidth) {
    const double minSpacing = 16;
    const double maxSpacing = 96;

    if (childCount <= 1) return 0;

    double spacing =
        (availableWidth - (childCount * nodeWidth)) / (childCount - 1);
    return spacing.clamp(minSpacing, maxSpacing);
  }

  @override
  void paint(Canvas canvas, Size size) {
    nodeRects.clear();
    final treeWidth = _calculateTreeWidth(root);
    final startY = size.height / 2;
    final rootX = size.width / 2;

    _drawNode(canvas, root, rootX, startY, treeWidth, 0);
  }

  double _drawNode(
    Canvas canvas,
    MindMapNode node,
    double x,
    double y,
    double width,
    int depth,
  ) {
    final rect = Rect.fromCenter(
      center: Offset(x, y),
      width: nodeWidth,
      height: nodeHeight,
    );
    nodeRects[node] = rect;
    final rrect = RRect.fromRectAndRadius(rect, Radius.circular(12));
    canvas.drawRRect(rrect, Paint()..color = Colors.brown[100]!);
    canvas.drawShadow(
      Path()..addRRect(rrect),
      Colors.brown.withOpacity(0.2),
      6,
      false,
    );

    final textSpan = TextSpan(
      text: node.title,
      style: const TextStyle(
        fontWeight: FontWeight.bold,
        fontSize: 16,
        color: Colors.black,
      ),
    );
    final tp = TextPainter(
      text: textSpan,
      textAlign: TextAlign.center,
      textDirection: TextDirection.ltr,
    );
    tp.layout(maxWidth: nodeWidth - 12);
    tp.paint(canvas, Offset(x - tp.width / 2, y - tp.height / 2));

    if (node.children.isNotEmpty) {
      final childWidths = node.children.map(_calculateTreeWidth).toList();
      final totalChildWidth = childWidths.reduce((a, b) => a + b);
      final dynamicSpacing = _calculateDynamicSpacing(
        node.children.length,
        width,
      );
      final childrenWidth =
          totalChildWidth + (node.children.length - 1) * dynamicSpacing;

      double childX = x - childrenWidth / 2 + childWidths[0] / 2;

      for (int i = 0; i < node.children.length; i++) {
        final child = node.children[i];
        final childTreeWidth = childWidths[i];
        final childCenterX = childX;
        final childCenterY =
            y + nodeHeight / 2 + verticalSpacing + nodeHeight / 2;

        canvas.drawLine(
          Offset(x, y + nodeHeight / 2),
          Offset(childCenterX, childCenterY - nodeHeight / 2),
          Paint()
            ..color = Colors.brown
            ..strokeWidth = 2,
        );

        _drawNode(
          canvas,
          child,
          childCenterX,
          y + nodeHeight + verticalSpacing,
          childTreeWidth,
          depth + 1,
        );
        childX += childTreeWidth + dynamicSpacing;
      }
    }

    return x;
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => true;
}
