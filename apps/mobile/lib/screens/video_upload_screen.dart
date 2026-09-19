import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class VideoUploadScreen extends StatefulWidget {
  const VideoUploadScreen({super.key});

  @override
  State<VideoUploadScreen> createState() => _VideoUploadScreenState();
}

class _VideoUploadScreenState extends State<VideoUploadScreen> {
  final _titleController = TextEditingController();
  final _descriptionController = TextEditingController();
  bool _submitting = false;

  // Adresse de l'API Django. En émulateur Android, remplacer 127.0.0.1 par 10.0.2.2.
  static const _apiBaseUrl = 'http://127.0.0.1:8000/api';

  Future<void> _uploadVideo() async {
    setState(() => _submitting = true);
    try {
      final response = await http.post(
        Uri.parse('$_apiBaseUrl/videos/'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'title': _titleController.text,
          'description': _descriptionController.text,
          'user': 1, // TODO: remplacer par l'utilisateur authentifié
          'file_url': 'https://example.com/video.mp4', // TODO: upload réel (S3/MinIO)
        }),
      );
      if (!mounted) return;
      final ok = response.statusCode == 201;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(ok ? 'Vidéo soumise !' : "Erreur lors de l'upload (${response.statusCode})")),
      );
    } catch (e) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Erreur réseau : $e')));
    } finally {
      if (mounted) setState(() => _submitting = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Uploader une vidéo')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            TextField(
              controller: _titleController,
              decoration: const InputDecoration(labelText: 'Titre de la vidéo'),
            ),
            TextField(
              controller: _descriptionController,
              decoration: const InputDecoration(labelText: 'Description'),
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: _submitting ? null : _uploadVideo,
              style: ElevatedButton.styleFrom(backgroundColor: const Color.fromRGBO(15, 82, 186, 1)),
              child: Text(_submitting ? 'Envoi…' : 'Uploader'),
            ),
          ],
        ),
      ),
    );
  }
}
