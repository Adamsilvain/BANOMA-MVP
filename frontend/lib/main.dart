import 'package:flutter/material.dart';
import 'screens/home_screen.dart';

void main() {
  runApp(BanomaApp());
}

class BanomaApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'BANOMA',
      theme: ThemeData(
        primaryColor: Color.fromRGBO(15, 82, 186, 1), // Bleu saphir
        visualDensity: VisualDensity.adaptivePlatformDensity,
      ),
      home: HomeScreen(),
    );
  }
}
