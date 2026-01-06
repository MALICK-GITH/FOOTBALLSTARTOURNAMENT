# Guide d'installation - eFootKings 2026

## Installation

### 1. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 2. Configuration

Créez un fichier `.env` (optionnel) avec les variables suivantes :

```env
SECRET_KEY=votre-cle-secrete-tres-longue-et-aleatoire
DATABASE_URL=sqlite:///efootkings.db
VERCEL=0
```

Pour PostgreSQL (production) :
```env
DATABASE_URL=postgresql://user:password@localhost/efootkings
```

### 3. Initialiser la base de données

La base de données sera créée automatiquement au premier lancement.

### 4. Lancer l'application

```bash
python app.py
```

L'application sera accessible sur `http://localhost:5000`

## Compte administrateur par défaut

- **Username:** `admin`
- **Password:** `admin123`

⚠️ **IMPORTANT:** Changez le mot de passe admin en production !

## Fonctionnalités

### Pour les utilisateurs

1. **Inscription**
   - Pseudo eFootball (unique)
   - Nom complet / contact (optionnel)
   - Photo de profil (optionnel)
   - Screenshot du paiement Mobile Money (obligatoire)
   - Mot de passe pour connexion

2. **Connexion persistante**
   - Les utilisateurs restent connectés même après fermeture du navigateur
   - Session valide 30 jours

3. **Dashboard utilisateur**
   - Voir les messages de l'admin
   - Historique des matchs
   - Badges et trophées
   - Position dans le bracket

### Pour l'administrateur

1. **Gestion des inscriptions**
   - Valider/refuser les inscriptions
   - Voir les screenshots de paiement
   - Supprimer des utilisateurs
   - Voir le statut en ligne/hors ligne

2. **Gestion du bracket**
   - Modifier les scores en temps réel
   - Le bracket se génère automatiquement à 8 joueurs validés
   - Attribution automatique des badges

3. **Messagerie**
   - Envoyer des messages globaux (tous les utilisateurs)
   - Envoyer des messages ciblés (un utilisateur spécifique)
   - Les utilisateurs ne peuvent pas répondre

## Structure de la base de données

- **User**: Comptes utilisateurs
- **Badge**: Badges et trophées (champion, finaliste, demi-finaliste)
- **Message**: Messages de l'admin
- **MatchHistory**: Historique des matchs pour chaque utilisateur
- **Bracket**: État actuel du bracket
- **AdminUser**: Compte administrateur

## Paiement Mobile Money

- **Numéro:** +225 0500 44 82 08
- **Plateformes:** Wave, MTN Money, Moov Money
- **Screenshot obligatoire** pour validation

## Sécurité

- Mots de passe hashés avec bcrypt
- Uploads sécurisés (vérification type et taille)
- Sessions persistantes sécurisées
- Protection CSRF (Flask par défaut)

## Déploiement

### Vercel

L'application est compatible Vercel. Les fichiers sont stockés dans `/tmp` sur Vercel.

### Autres plateformes

L'application peut être déployée sur n'importe quelle plateforme supportant Flask :
- Heroku
- Railway
- DigitalOcean
- AWS
- etc.

## Support

Pour toute question ou problème, contactez l'administrateur.

