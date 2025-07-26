import 'package:flutter/material.dart';

class ProfileScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Profil')),
      body: Padding(
        padding: EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            CircleAvatar(
              radius: 50,
              backgroundColor: Color.fromRGBO(15, 82, 186, 1),
              child: Text('AO', style: TextStyle(fontSize: 40, color: Colors.white)),
            ),
            SizedBox(height: 20),
            Text('Adama Ouédraogo', style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold)),
            Text('Chercheur en IA | Burkina Faso'),
            Text('Compétences : QGIS, Python, Enseignement'),
            Text('Langues : Français, Mooré, Anglais'),
            SizedBox(height: 20),
            ElevatedButton(
              onPressed: () {},
              child: Text('Modifier le profil'),
              style: ElevatedButton.styleFrom(primary: Color.fromRGBO(15, 82, 186, 1)),
            ),
          ],
        ),
      ),
    );
  }
}
