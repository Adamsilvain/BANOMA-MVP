import 'package:flutter/material.dart';
import 'screens/home_screen.dart';

void main() {
  runApp(const BanomaApp());
}

class BanomaApp extends StatelessWidget {
  const BanomaApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'BANOMA',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        primaryColor: const Color.fromRGBO(15, 82, 186, 1), // Bleu saphir
        colorScheme: ColorScheme.fromSeed(seedColor: const Color.fromRGBO(15, 82, 186, 1)),
        visualDensity: VisualDensity.adaptivePlatformDensity,
      ),
      home: const HomeScreen(),
    );
  }
}
