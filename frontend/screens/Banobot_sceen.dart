import 'package:flutter/material.dart';

class BanoBotScreen extends StatefulWidget {
  @override
  _BanoBotScreenState createState() => _BanoBotScreenState();
}

class _BanoBotScreenState extends State<BanoBotScreen> {
  final _queryController = TextEditingController();
  String _response = '';

  Future<void> _askBanoBot() async {
    // Simulation d'appel à une API IA
    setState(() {
      _response = 'BanoBot : Voici un résumé de votre texte : [Résumé simulé]';
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('BanoBot')),
      body: Padding(
        padding: EdgeInsets.all(16.0),
        child: Column(
          children: [
            TextField(
              controller: _queryController,
              decoration: InputDecoration(labelText: 'Posez une question à BanoBot'),
            ),
            SizedBox(height: 20),
            ElevatedButton(
              onPressed: _askBanoBot,
              child: Text('Demander'),
              style: ElevatedButton.styleFrom(primary: Color.fromRGBO(15, 82, 186, 1)),
            ),
            SizedBox(height: 20),
            Text(_response, style: TextStyle(fontSize: 16)),
          ],
        ),
      ),
    );
  }
}
