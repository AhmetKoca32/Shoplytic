import 'package:flutter_test/flutter_test.dart';

import 'package:shoplytic_ui/app.dart';

void main() {
  testWidgets('App launches successfully', (WidgetTester tester) async {
    await tester.pumpWidget(const ShoplyticApp());
    expect(find.text('Shoplytic'), findsWidgets);
  });
}
