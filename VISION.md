# BANOMA — Vision produit consolidée

**Ce document est la référence officielle du projet.** Il fusionne et tranche entre les versions
précédentes du white paper (docx v2.0 — juillet 2025 — et .md v1.0 — janvier 2026 — qui se
contredisaient sur plusieurs points techniques et business). En cas de nouveau document
contradictoire à l'avenir, c'est CE fichier qui fait foi jusqu'à mise à jour explicite.

## Positionnement

BANOMA — *Bangré Nooma*, « Rien de tel que la connaissance » — est une plateforme scientifique
africaine de nouvelle génération, fusion de TikTok (découverte vidéo courte), Facebook
(publication sociale), YouTube (vidéo longue/éducative), LinkedIn (profils scientifiques) et
Udemy/Coursera (marketplace), le tout spécialisé dans le savoir scientifique et technique.

## Stack technique retenue (tranchée)

| Couche | Choix | Statut |
|---|---|---|
| Backend API | Django REST Framework (Python) | ✅ Construit |
| API | REST (GraphQL réévalué si le feed devient complexe) | ✅ |
| Base de données | PostgreSQL (+ champs JSONB pour contenu flexible) | ✅ |
| Cache / files | Redis + Celery | ✅ |
| Mobile | Flutter | ✅ Construit |
| Web | Next.js | ✅ Construit |
| Vidéo | FFmpeg → HLS, stockage S3/MinIO | ⚠️ Transcodage basique fait, upload S3 pas branché |
| IA | À terme : API LLM (Claude/GPT) + NMT pour traduction locale | ❌ Stub FastAPI actuel à remplacer |
| Paiements | Stripe + Mobile Money (CinetPay : Wave/Orange/Moov) + wallet interne | ⚠️ Stripe + squelette Mobile Money faits, wallet pas fait |

## Modèle économique (tranché)

**Règle d'or : 70 % des revenus d'une vente reviennent au créateur, 30 % à la plateforme.**
C'est l'argument de différenciation principal face à YouTube (55 %), Udemy (jusqu'à 75 % de
commission), Coursera (50 %). ✅ Implémenté et testé (`Purchase.platform_commission` /
`creator_revenue`).

Reporting et levée de fonds en **USD** (cohérent avec les investisseurs ciblés : Banque Mondiale,
Partech Africa, Mastercard Foundation...). Les paiements côté utilisateurs restent multi-devises
(XOF pour l'Afrique de l'Ouest en priorité, USD/EUR pour la diaspora et les institutions).

## Les fonctionnalités du produit

### Déjà construites
- Authentification JWT (inscription/connexion)
- Profils scientifiques : bio, compétences, langues, **Score de Crédibilité Scientifique (SCS)**,
  badges, publications/DOI
- Marketplace du savoir : cours, ebooks, datasets, prestations, code source — split 70/30 vérifié
- Upload vidéo avec transcodage FFmpeg → HLS (via Celery)
- Paiement Stripe fonctionnel, squelette Mobile Money

### À construire — dans l'ordre de dépendance logique, pas encore priorisé
1. **Feed vidéo façon TikTok** : scroll vertical, autoplay adaptatif, chapitrage auto par IA,
   overlays interactifs (quiz, CTA marketplace), indicateur qualité réseau / mode économie de
   données
2. **Publication sociale façon Facebook** : posts riches (texte/image/vidéo/PDF/dataset), threads
   scientifiques avec versioning et citations, suggestions IA de références/bibliographie
3. **BanoBot** : vraie IA (API LLM), traduction dans les 12 langues africaines cibles (mooré,
   dioula, fulfuldé, arabe hassaniya, swahili...), résumé, **détection de plagiat**, modération de
   désinformation
4. **Gamification** : XP, niveaux nommés (Apprenti → Praticien → Expert → Maître → Légende),
   badges thématiques, classements, concours panafricains, BANOMA Awards
5. **Débat Arena** : débats modérés par IA, votes en temps réel, journalisation des résultats
6. **Labs Virtuels** : sandboxes de simulation, notebooks partagés, visualisations 3D
7. **Wallet interne** multi-devises avec KYC/KYB pour les vendeurs, paiement à la vue
8. **Mode École / Université / ONG** : portails institutionnels, SSO, analytics dédiés
9. Messagerie (chat 1:1/groupes, appels WebRTC)
10. Mode hors-ligne, sync différentiel, support multilingue complet de l'interface

## Ce que ce document remplace

- `BANOMA_WhitePaper_Complet.docx` (v2.0, juillet 2025) — conservé comme archive historique
- `WHITE_PAPER_BANOMA.md` (v1.0, janvier 2026) — conservé comme archive historique
- Les deux restent des documents de référence pour le contexte business (marché, concurrence,
  levée de fonds), mais pour toute décision technique ou produit, **ce fichier fait autorité**.
