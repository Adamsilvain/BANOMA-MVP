# BANOMA

**Bangrê Nooma — « D'où vient l'intelligence »**

Plateforme qui connecte les talents scientifiques et techniques aux opportunités mondiales :
vitrine interactive pour les experts, mise en relation avec des opportunités (missions, emplois,
collaborations, formations), et monétisation des savoir-faire.

## Choix d'architecture

Après comparaison de deux bases de code (NestJS/TypeScript vs Flutter/Django), le backend retenu
est **Django** :
- l'application mobile Flutter y était déjà branchée
- l'admin Django intégré donne une interface de gestion (utilisateurs, vidéos, paiements,
  opportunités) sans rien développer en plus
- une stack Python/Django est plus simple à maintenir pour un porteur de projet seul ou une petite
  équipe qu'un empilement NestJS + Prisma + Bull

## Structure du monorepo
```
apps/
  web/       — Frontend Next.js (vitrine + marketplace, consomme l'API Django)
  mobile/    — Application Flutter (accueil, profil, upload vidéo, BanoBot)
services/
  api/       — Backend Django REST Framework (auth JWT, profils, opportunités,
               candidatures, paiements) + tâches Celery (transcodage vidéo)
  ai/        — Microservice FastAPI (matching talent↔opportunité, résumé de profil)
infra/
  k8s/       — Manifests Kubernetes (API, worker Celery)
  helm/      — Chart Helm
```

## Démarrage local (Docker)
```bash
cp .env.example .env   # puis compléter JWT/Stripe/Mobile Money selon besoin
docker-compose up --build
```
- Web : http://localhost:3000
- API Django : http://localhost:8000/api/
- Admin Django : http://localhost:8000/admin/
- Service IA : http://localhost:8001/docs
- MinIO console : http://localhost:9001

## Démarrage local (sans Docker)

### API Django
```bash
cd services/api
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Worker Celery (transcodage vidéo — nécessite ffmpeg + Redis en local)
```bash
cd services/api
celery -A banoma_project worker --loglevel=info
```

### App mobile Flutter
```bash
cd apps/mobile
flutter pub get
flutter run
```
Sur émulateur Android, remplacer `127.0.0.1` par `10.0.2.2` dans `lib/services/api_config.dart`.

### Frontend web
```bash
cd apps/web
npm install
npm run dev
```

## Endpoints API principaux
| Endpoint | Méthode | Description |
|---|---|---|
| `/api/auth/register/` | POST | Inscription (crée User + Profile) |
| `/api/auth/login/` | POST | Connexion, renvoie un JWT |
| `/api/talents/?skill=xxx` | GET | Vitrine des talents, filtrable |
| `/api/opportunities/` | GET/POST | Liste / publication d'opportunités |
| `/api/applications/` | POST | Candidater à une opportunité (auth requise) |
| `/api/videos/` | POST | Soumettre une vidéo de portfolio (déclenche le transcodage Celery) |
| `/api/payments/` | POST | Créer un paiement (Stripe ou Mobile Money) |

## État d'avancement
- [x] Backend Django validé : `manage.py check`, migrations générées et appliquées, endpoints
      `health` et `register` testés avec un vrai serveur
- [x] Auth JWT (inscription/connexion), profils, opportunités, candidatures
- [x] Paiements : Stripe Checkout opérationnel, squelette Mobile Money (Orange/Moov) prêt à
      brancher sur le prestataire retenu
- [x] Upload vidéo → tâche Celery → transcodage FFmpeg en HLS
- [x] Microservice IA (matching, résumé) — baseline simple à faire évoluer
- [x] Frontend web Next.js et app Flutter branchés sur l'API Django
- [ ] Upload effectif du résultat du transcodage vers MinIO/S3 (TODO dans `banoma_api/tasks.py`)
- [ ] Authentification côté Flutter (stockage/refresh du JWT) et côté Next.js
- [ ] Intégration Mobile Money réelle (dépend du prestataire choisi : Orange Money / Moov Money)
- [ ] Tests automatisés (`pytest-django`, `flutter test`)
- [ ] Observabilité et durcissement sécurité avant mise en production

## Secrets à configurer avant déploiement
Voir `.env.example` — `DJANGO_SECRET_KEY`, `DATABASE_URL`, clés Stripe, identifiants Mobile Money,
clés S3/MinIO. Ne jamais committer de valeurs réelles.

## Contact
Adama Ouédraogo
