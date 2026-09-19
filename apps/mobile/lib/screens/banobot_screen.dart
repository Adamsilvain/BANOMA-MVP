import 'package:flutter/material.dart';

class BanoBotScreen extends StatefulWidget {
  const BanoBotScreen({super.key});

  @override
  State<BanoBotScreen> createState() => _BanoBotScreenState();
}

class _BanoBotScreenState extends State<BanoBotScreen> {
  final _queryController = TextEditingController();
  String _response = '';

  Future<void> _askBanoBot() async {
    // TODO: brancher sur le microservice IA réel (ex: POST /recommend ou /summarize
    // du service FastAPI de BANOMA) au lieu de cette réponse simulée.
    setState(() {
      _response = 'BanoBot : Voici un résumé de votre texte : [Résumé simulé]';
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('BanoBot')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            TextField(
              controller: _queryController,
              decoration: const InputDecoration(labelText: 'Posez une question à BanoBot'),
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: _askBanoBot,
              style: ElevatedButton.styleFrom(backgroundColor: const Color.fromRGBO(15, 82, 186, 1)),
              child: const Text('Demander'),
            ),
            const SizedBox(height: 20),
            Text(_response, style: const TextStyle(fontSize: 16)),
          ],
        ),
      ),
    );
  }
}
