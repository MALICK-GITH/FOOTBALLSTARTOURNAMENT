# Structure du Projet eFootball Mobile 2026 Tournament Platform

## 📁 Organisation des Fichiers

```
kingsefootball2026/
├── main.py                 # Point d'entrée FastAPI
├── config.py              # Configuration (settings, secrets)
├── database.py            # Configuration SQLAlchemy
├── models.py              # Modèles de base de données
├── schemas.py             # Schémas Pydantic (validation)
├── auth.py                # Authentification et sécurité
├── init_db.py             # Initialisation de la base de données
├── run.py                 # Script de démarrage
├── requirements.txt       # Dépendances Python
├── README.md              # Documentation principale
│
├── routes/                # Routes API
│   ├── __init__.py
│   ├── users.py          # Gestion des utilisateurs
│   ├── admin.py          # Routes d'administration
│   ├── tournaments.py    # Gestion des tournois
│   ├── matches.py        # Gestion des matchs
│   └── messages.py       # Messages administrateur
│
├── templates/             # Pages HTML
│   ├── index.html        # Page d'accueil
│   ├── admin.html        # Interface d'administration
│   └── brackets.html     # Affichage des brackets
│
└── static/               # Fichiers statiques
    ├── css/
    │   └── style.css     # Styles CSS
    ├── js/
    │   ├── app.js        # JavaScript principal
    │   └── admin.js      # JavaScript admin
    └── uploads/          # Fichiers uploadés (créé automatiquement)
        ├── profiles/     # Photos de profil
        └── payments/     # Preuves de paiement
```

## 🔧 Technologies Utilisées

### Backend
- **FastAPI** : Framework web moderne et rapide
- **SQLAlchemy** : ORM pour la base de données
- **Pydantic** : Validation des données
- **JWT** : Authentification par tokens
- **Bcrypt** : Hash des mots de passe
- **Alembic** : Migrations de base de données (optionnel)

### Frontend
- **HTML5** : Structure
- **CSS3** : Styles modernes avec variables CSS
- **JavaScript (Vanilla)** : Interactivité, pas de framework

### Base de données
- **SQLite** : Par défaut (développement)
- **PostgreSQL** : Pour la production (configurable)

## 🚀 Fonctionnalités Implémentées

### 👤 Utilisateurs
- ✅ Inscription avec validation
- ✅ Connexion avec sessions persistantes
- ✅ Gestion de profil
- ✅ Upload photo de profil
- ✅ Upload preuve de paiement
- ✅ Statuts d'inscription (pending/approved/rejected)

### 👑 Administration
- ✅ Interface admin complète
- ✅ Gestion des utilisateurs (approuver/refuser/bloquer)
- ✅ Gestion des inscriptions
- ✅ Création de tournois
- ✅ Génération automatique de brackets
- ✅ Modification manuelle des brackets
- ✅ Mise à jour des scores de matchs
- ✅ Messages/annonces globales
- ✅ Logs d'activité complets

### 🏆 Tournois
- ✅ Création de tournois
- ✅ Inscription aux tournois
- ✅ Génération automatique de brackets
- ✅ Affichage des brackets
- ✅ Gestion des matchs
- ✅ Système d'élimination directe

### 💬 Messages
- ✅ Messages administrateur visibles par tous
- ✅ Messages importants (highlight)
- ✅ Affichage chronologique

## 🔐 Sécurité

- ✅ Mots de passe hashés avec bcrypt
- ✅ Tokens JWT pour l'authentification
- ✅ Sessions persistantes sécurisées
- ✅ Validation stricte des fichiers uploadés
- ✅ Protection contre les injections SQL (ORM)
- ✅ Logs d'audit pour toutes les actions sensibles
- ✅ Séparation frontend/backend

## 📊 Base de Données

### Modèles Principaux

1. **User** : Utilisateurs du système
2. **Tournament** : Tournois
3. **TournamentRegistration** : Inscriptions aux tournois
4. **Match** : Matchs individuels
5. **Bracket** : Positions dans les brackets
6. **AdminMessage** : Messages administrateur
7. **ActivityLog** : Logs d'activité

## 🎨 Interface

- Design moderne inspiré e-sport
- Couleurs sombres avec accents colorés
- Responsive (mobile-friendly)
- Animations légères
- UI intuitive et professionnelle

## 📝 Configuration

Toutes les configurations sont dans `config.py` et peuvent être surchargées via des variables d'environnement dans `.env`:

- `SECRET_KEY` : Clé secrète pour JWT
- `DATABASE_URL` : URL de connexion à la base de données
- `ADMIN_EMAIL` : Email du compte admin
- `ADMIN_PASSWORD` : Mot de passe admin
- `UPLOAD_DIR` : Dossier d'upload
- `MAX_UPLOAD_SIZE` : Taille max des fichiers

## 🔄 Workflow

1. **Initialisation** : `python init_db.py`
2. **Démarrage** : `python run.py` ou `uvicorn main:app --reload`
3. **Accès** : http://localhost:8000
4. **Admin** : http://localhost:8000/admin

## 📌 Points Importants

- Toutes les données sont sauvegardées automatiquement
- Les sessions persistent même après fermeture du navigateur
- Les brackets sont générés automatiquement au démarrage d'un tournoi
- Seul l'admin peut modifier les brackets et scores
- Toutes les actions sont loggées pour l'audit

## 🚧 Améliorations Futures Possibles

- Notifications en temps réel (WebSockets)
- Système de paiement intégré
- Statistiques et classements avancés
- Mode tournoi suisse
- Intégration avec des APIs externes
- Dashboard analytics

