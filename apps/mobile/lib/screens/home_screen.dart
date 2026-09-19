import 'package:flutter/material.dart';
import 'profile_screen.dart';
import 'video_upload_screen.dart';
import 'banobot_screen.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("BANOMA - D'où vient l'intelligence"),
        backgroundColor: const Color.fromRGBO(15, 82, 186, 1),
      ),
      body: ListView(
        children: [
          ListTile(
            leading: const Icon(Icons.person),
            title: const Text('Voir mon profil'),
            onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => const ProfileScreen())),
          ),
          ListTile(
            leading: const Icon(Icons.videocam),
            title: const Text('Uploader une vidéo'),
            onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => const VideoUploadScreen())),
          ),
          ListTile(
            leading: const Icon(Icons.smart_toy),
            title: const Text('Demander à BanoBot'),
            onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => const BanoBotScreen())),
          ),
        ],
      ),
    );
  }
}
