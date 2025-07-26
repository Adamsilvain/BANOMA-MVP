BANOMA MVP

BANOMA (Bangrê Nooma – D'où vient l'intelligence) est une plateforme sociale interactive pour valoriser les compétences scientifiques, techniques et intellectuelles. Ce dépôt contient le MVP avec une application Flutter (frontend) et une API Django (backend).

Fonctionnalités





Écran d’accueil : Navigation vers le profil, l’upload de vidéos, et BanoBot.



Profil utilisateur : Affichage des compétences et informations.



Upload de vidéos : Soumission de vidéos (simulée).



BanoBot : Interface pour interagir avec un assistant IA (simulé).



API Backend : Gestion des profils et vidéos.

Prérequis





Flutter : SDK 2.12.0 ou supérieur



Python : 3.8 ou supérieur



Django : 4.2.7



Git : Pour cloner le dépôt

Installation

1. Cloner le dépôt

git clone https://github.com/votre-utilisateur/banoma-mvp.git
cd banoma-mvp

2. Configurer le backend





Naviguez dans le dossier backend :

cd backend



Créez un environnement virtuel et installez les dépendances :

python -m venv venv
source venv/bin/activate  # Sur Windows : venv\Scripts\activate
pip install -r requirements.txt



Appliquez les migrations :

python manage.py makemigrations
python manage.py migrate



Créez un superutilisateur :

python manage.py createsuperuser



Lancez le serveur :

python manage.py runserver

3. Configurer le frontend





Naviguez dans le dossier frontend :

cd frontend



Installez les dépendances Flutter :

flutter pub get



Lancez l’application :

flutter run

Structure du projet





frontend/ : Application Flutter





lib/main.dart : Point d’entrée



lib/screens/ : Écrans (accueil, profil, vidéo, BanoBot)



backend/ : API Django





banoma_api/models.py : Modèles de données



banoma_api/views.py : Vues API



banoma_api/serializers.py : Sérialiseurs



banoma_api/urls.py : Routes API

Prochaines étapes





Intégrer AWS S3 pour le stockage vidéo.



Ajouter l’intégration de paiements (Stripe, Momo).



Implémenter BanoBot avec une API IA réelle.



Développer la boutique et les fonctionnalités de gamification.

Contribuer





Forkez le dépôt.



Créez une branche : git checkout -b feature/nouvelle-fonctionnalite.



Soumettez une pull request.

Contact

Adama Ouédraogo
