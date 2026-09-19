# BANOMA

**Bangré Nooma — « Rien de tel que la connaissance »**

Plateforme scientifique africaine de nouvelle génération : réseau social scientifique · vidéo
éducative · marketplace du savoir · IA (BanoBot) · gamification.

📄 **Voir [`VISION.md`](./VISION.md) pour la vision produit de référence** — ce fichier fusionne
et tranche les versions antérieures du white paper qui se contredisaient entre elles.

## Choix d'architecture

Après comparaison de deux bases de code (NestJS/TypeScript vs Flutter/Django), le backend retenu
est **Django** — ce qui correspond à la stack prévue par le white paper (section 7.1) :
- l'application mobile Flutter y était déjà branchée
- l'admin Django intégré donne une interface de gestion (utilisateurs, vidéos, paiements, ventes)
  sans rien développer en plus
- conforme à la stack cible du white paper : Django REST Framework + PostgreSQL + Redis + Celery

## Structure du monorepo
```
apps/
  web/       — Frontend Next.js (vitrine talents + boutique, consomme l'API Django)
  mobile/    — Application Flutter (accueil, profil, upload vidéo, BanoBot)
services/
  api/       — Backend Django REST Framework (auth JWT, profils certifiables, marketplace
               du savoir, paiements) + tâches Celery (transcodage vidéo)
  ai/        — Microservice IA (baseline actuelle — à remplacer par une vraie API LLM, voir plus bas)
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

## Modèle de données (aligné sur le white paper v2.0)
`User` (talent/créateur) — `Profile` (vitrine certifiable : badges, SCS, publications/DOI) —
`Badge` — `Publication` (diplômes, certifications, publications, projets) —
`Product` (marketplace : cours, ebooks, datasets, prestations, code source) —
`Purchase` (achat, split automatique **70 % créateur / 30 % plateforme**) —
`Payment` (Stripe, PayPal à venir, ou Mobile Money via CinetPay).

## Endpoints API principaux
| Endpoint | Méthode | Description |
|---|---|---|
| `/api/auth/register/` | POST | Inscription (crée User + Profile) |
| `/api/auth/login/` | POST | Connexion, renvoie un JWT |
| `/api/talents/?skill=xxx` | GET | Vitrine des talents, filtrable |
| `/api/products/?type=COURS` | GET/POST | Marketplace du savoir |
| `/api/products/mine/` | GET | Ma boutique personnelle (auth requise) |
| `/api/purchases/` | POST | Acheter un article — calcule le split 70/30 et initie le paiement |
| `/api/purchases/mine/` | GET | Mes achats |
| `/api/sales/mine/` | GET | Mes ventes et revenus (auth requise) |
| `/api/videos/` | POST | Soumettre une vidéo éducative (déclenche le transcodage Celery) |

## État d'avancement
- [x] Backend Django validé de bout en bout avec un vrai serveur : inscription, connexion JWT,
      publication d'un article, achat avec calcul réel du split 70/30
      (testé : 5000 XOF → 3500 créateur / 1500 plateforme)
- [x] Auth JWT, profils certifiables (badges, publications/DOI)
- [x] Marketplace du savoir avec règle d'or 70/30 conforme au white paper
- [x] Paiements : Stripe Checkout opérationnel, squelette Mobile Money (Wave/Orange/Moov via
      CinetPay à finaliser), PayPal pas encore implémenté
- [x] Upload vidéo → tâche Celery → transcodage FFmpeg en HLS
- [x] Frontend web Next.js (vitrine talents + boutique) et app Flutter branchés sur l'API Django

### Écart encore important avec le white paper v2.0
- [ ] **BanoBot** : actuellement un microservice FastAPI avec matching par mots-clés — le white
      paper prévoit une vraie IA (API Claude/GPT) multilingue, avec recherche documentaire,
      génération de contenu assistée et modération de désinformation
- [ ] **Feed vidéo éducatif** : chapitrage automatique, sous-titrage multilingue, transcodage
      adaptatif 144p–1080p, analytics d'attention — seuls l'upload brut et le transcodage HLS de
      base existent
- [ ] **Gamification** : XP, niveaux (Apprenti → Légende), badges thématiques, classements,
      concours panafricains — pas commencé
- [ ] **Messagerie** (chat 1:1/groupes, appels WebRTC) — pas commencée
- [ ] Support multilingue (12 langues dont mooré, dioula, fulfuldé), mode hors-ligne
- [ ] Elasticsearch (recherche full-text), S3 + CloudFront (stockage/CDN vidéo)
- [ ] 2FA TOTP, RBAC à 4 niveaux (USER/CREATOR/BUSINESS/ADMIN)
- [ ] Upload effectif du résultat du transcodage vers MinIO/S3 (TODO dans `banoma_api/tasks.py`)
- [ ] Tests automatisés (`pytest-django`, `flutter test`)

## Secrets à configurer avant déploiement
Voir `.env.example` — `DJANGO_SECRET_KEY`, `DATABASE_URL`, clés Stripe, identifiants Mobile Money,
clés S3/MinIO. Ne jamais committer de valeurs réelles.

## Contact
Adama Ouédraogo
