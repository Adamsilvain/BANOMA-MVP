import 'package:flutter/material.dart';
import 'profile_screen.dart';
import 'video_upload_screen.dart';
import 'banobot_screen.dart';

class HomeScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('BANOMA - D\'où vient l\'intelligence'),
        backgroundColor: Color.fromRGBO(15, 82, 186, 1),
      ),
      body: ListView(
        children: [
          ListTile(
            leading: Icon(Icons.person),
            title: Text('Voir mon profil'),
            onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => ProfileScreen())),
          ),
          ListTile(
            leading: Icon(Icons.videocam),
            title: Text('Uploader une vidéo'),
            onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => VideoUploadScreen())),
          ),
          ListTile(
            leading: Icon(Icons.smart_toy),
            title: Text('Demander à BanoBot'),
            onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => BanoBotScreen())),
          ),
        ],
      ),
    );
  }
}
