# eFootKings 2026 🇨🇮 - ORACXPRED

Plateforme web complète et professionnelle pour le tournoi eFootball Mobile 2026.

## 🎮 Fonctionnalités principales

### 👥 Comptes utilisateurs
- ✅ Création de compte avec pseudo eFootball unique
- ✅ Nom complet / contact (optionnel)
- ✅ Photo de profil (PNG, JPG, JPEG, GIF, WEBP, max 5MB)
- ✅ Screenshot du paiement Mobile Money obligatoire
- ✅ **Connexion persistante** : les utilisateurs restent connectés même après fermeture du navigateur
- ✅ Déconnexion possible, reconnexion automatique
- ✅ Historique complet de toutes les actions

### 💰 Gestion des inscriptions et paiements
- ✅ Limite à **8 joueurs maximum**
- ✅ Paiement Mobile Money obligatoire via Wave, MTN Money, Moov Money
- ✅ Numéro : **+225 0500 44 82 08**
- ✅ Screenshot du paiement requis pour validation
- ✅ L'administrateur peut valider ou rejeter l'inscription
- ✅ Sauvegarde immédiate dans la base de données
- ✅ L'administrateur peut supprimer les inscriptions si nécessaire

### 🏆 Bracket dynamique
- ✅ Élimination directe : quart → demi → finale
- ✅ L'administrateur peut modifier scores, matchs et bracket à tout moment
- ✅ **Mise à jour automatique et instantanée** pour tous les utilisateurs
- ✅ Gestion automatique des badges et trophées :
  - 🥇 Champion
  - 🥈 Finaliste
  - 🥉 Demi-finaliste

### 💬 Messagerie admin
- ✅ L'administrateur peut envoyer des messages **globaux** ou **ciblés**
- ✅ Les utilisateurs ne peuvent pas répondre
- ✅ Messages en temps réel, style WhatsApp/Facebook
- ✅ Notifications visibles pour nouveaux messages
- ✅ Utilisation : annonces, résultats, nouvelles fonctionnalités, rappels

### 💾 Sauvegarde et persistance totale
- ✅ Base de données robuste : **SQLAlchemy** (SQLite/PostgreSQL/MySQL)
- ✅ Toutes les actions et fichiers sont sauvegardés instantanément
- ✅ Chaque modification (scores, bracket, badges, messages) est stockée
- ✅ Historique horodaté complet pour restaurer n'importe quel état antérieur

### 👨‍💼 Supervision administrateur
- ✅ L'administrateur voit tous les utilisateurs en temps réel :
  - Pseudo, nom complet, photo, statut en ligne/hors ligne
  - Historique des matchs et positions dans le bracket
  - Validation des paiements et inscriptions
- ✅ Contrôle total : suppression, modification, messages

### 🎨 Interface et UX
- ✅ Interface moderne, attractive, responsive (mobile et desktop)
- ✅ Bracket visuel et interactif, avec scores et badges
- ✅ Notifications visibles pour messages et changements de bracket
- ✅ Historique complet pour chaque utilisateur : matchs joués, scores et positions

### ⚙️ Automatisation complète
- ✅ Calcul automatique du classement et des prochains matchs
- ✅ Gestion automatique des badges et trophées
- ✅ Synchronisation instantanée pour tous les utilisateurs après toute modification

### 🔒 Sécurité et fiabilité
- ✅ Mots de passe hashés (bcrypt)
- ✅ Uploads sécurisés avec contrôle de type et taille
- ✅ Protection contre suppression accidentelle ou crash du serveur
- ✅ Connexion persistante et fiable, aucune donnée ne peut être perdue

## 🚀 Installation

### 1. Prérequis
- Python 3.8+
- pip

### 2. Installation des dépendances

```bash
pip install -r requirements.txt
```

### 3. Configuration (optionnel)

Créez un fichier `.env` :

```env
SECRET_KEY=votre-cle-secrete-tres-longue-et-aleatoire
DATABASE_URL=sqlite:///efootkings.db
VERCEL=0
```

Pour PostgreSQL (production) :
```env
DATABASE_URL=postgresql://user:password@localhost/efootkings
```

### 4. Lancer l'application

```bash
python app.py
```

L'application sera accessible sur `http://localhost:5000`

## 🔐 Compte administrateur par défaut

- **Username:** `admin`
- **Password:** `admin123`

⚠️ **IMPORTANT:** Changez le mot de passe admin en production !

## 📦 Technologies utilisées

### Backend
- **Flask 3.0** : Framework web Python
- **Flask-Login** : Gestion des sessions utilisateurs
- **Flask-SQLAlchemy** : ORM pour la base de données
- **bcrypt** : Hashage sécurisé des mots de passe
- **SQLite/PostgreSQL/MySQL** : Base de données

### Frontend
- **Bootstrap 5** : Framework CSS responsive
- **Font Awesome** : Icônes
- **Google Fonts (Poppins)** : Police de caractères
- **Animate.css** : Animations
- **JavaScript** : Mises à jour en temps réel (AJAX)

## 📁 Structure du projet

```
kingsefootball2026/
├── app.py                      # Application Flask principale
├── requirements.txt            # Dépendances Python
├── vercel.json                 # Configuration Vercel
├── SETUP.md                    # Guide d'installation détaillé
├── templates/                  # Templates HTML
│   ├── base.html
│   ├── index.html
│   ├── register.html
│   ├── user_login.html
│   ├── user_dashboard.html
│   ├── bracket.html
│   ├── admin_login.html
│   ├── admin_dashboard.html
│   └── admin_messages.html
├── static/                     # Fichiers statiques
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
├── uploads/                    # Fichiers uploadés (créé automatiquement)
│   ├── profiles/               # Photos de profil
│   └── payments/               # Screenshots de paiement
└── efootkings.db              # Base de données SQLite (créé automatiquement)
```

## 🗄️ Structure de la base de données

- **User** : Comptes utilisateurs avec connexion persistante
- **Badge** : Badges et trophées (champion, finaliste, demi-finaliste)
- **Message** : Messages de l'admin (globaux ou ciblés)
- **MatchHistory** : Historique des matchs pour chaque utilisateur
- **Bracket** : État actuel du bracket (JSON dans la base)
- **AdminUser** : Compte administrateur

## 💳 Paiement Mobile Money

- **Numéro:** +225 0500 44 82 08
- **Plateformes supportées:** Wave, MTN Money, Moov Money
- **Screenshot obligatoire** pour validation de l'inscription

## 🔄 Mises à jour en temps réel

- Le bracket se met à jour automatiquement toutes les 5 secondes
- Les messages non lus sont vérifiés toutes les 30 secondes
- Les utilisateurs voient les changements instantanément

## 📝 Notes importantes

- Les données sont stockées dans une base de données SQLAlchemy (persistance totale)
- Les fichiers uploadés sont sauvegardés dans `uploads/`
- Le tournoi est limité à **8 joueurs maximum**
- Le bracket est généré automatiquement quand 8 joueurs sont validés
- Les badges sont attribués automatiquement selon les résultats

## 🚀 Déploiement

### Vercel

L'application est compatible Vercel. Les fichiers sont stockés dans `/tmp` sur Vercel.

```bash
vercel
```

### Autres plateformes

L'application peut être déployée sur n'importe quelle plateforme supportant Flask :
- Heroku
- Railway
- DigitalOcean
- AWS
- etc.

## 📞 Support

Pour toute question ou problème, contactez l'administrateur.

---

Développé avec ❤️ pour la communauté eFootball Mobile - ORACXPRED / eFootKings 2026
