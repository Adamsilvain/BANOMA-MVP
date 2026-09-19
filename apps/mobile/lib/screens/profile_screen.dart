import 'package:flutter/material.dart';

class ProfileScreen extends StatelessWidget {
  const ProfileScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Profil')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            const CircleAvatar(
              radius: 50,
              backgroundColor: Color.fromRGBO(15, 82, 186, 1),
              child: Text('AO', style: TextStyle(fontSize: 40, color: Colors.white)),
            ),
            const SizedBox(height: 20),
            const Text('Adama Ouédraogo', style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold)),
            const Text('Chercheur en géographie | Burkina Faso'),
            const Text('Compétences : QGIS, Python, Enseignement'),
            const Text('Langues : Français, Mooré, Anglais'),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: () {},
              style: ElevatedButton.styleFrom(backgroundColor: const Color.fromRGBO(15, 82, 186, 1)),
              child: const Text('Modifier le profil'),
            ),
          ],
        ),
      ),
    );
  }
}
