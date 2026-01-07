# 🚀 Guide de Démarrage Rapide

## Installation

### 1. Prérequis
- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

### 2. Installation des dépendances

```bash
pip install -r requirements.txt
```

### 3. Configuration

Copiez le fichier `.env.example` vers `.env` et modifiez les valeurs si nécessaire :

```bash
# Sur Linux/Mac
cp .env.example .env

# Sur Windows
copy .env.example .env
```

Modifiez au minimum :
- `SECRET_KEY` : Changez par une clé secrète aléatoire (minimum 32 caractères)
- `ADMIN_PASSWORD` : Changez le mot de passe admin

### 4. Initialisation de la base de données

```bash
python init_db.py
```

Cela va :
- Créer toutes les tables dans la base de données
- Créer le compte administrateur par défaut

### 5. Démarrage du serveur

```bash
python run.py
```

Ou directement avec uvicorn :

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 6. Accès à l'application

- **Site principal** : http://localhost:8000
- **Interface admin** : http://localhost:8000/admin
- **Documentation API** : http://localhost:8000/docs (Swagger UI)

## 🔑 Connexion Admin

Par défaut :
- **Email** : `admin@tournament.com` (configurable dans `.env`)
- **Password** : `ChangeMe123!` (⚠️ Changez-le immédiatement en production!)

## 📋 Premiers Pas

### 1. Créer un compte utilisateur
- Cliquez sur "Inscription" sur la page d'accueil
- Remplissez le formulaire
- Connectez-vous avec vos identifiants

### 2. Se connecter en tant qu'admin
- Allez sur `/admin`
- Connectez-vous avec les identifiants admin

### 3. Approuver un utilisateur
- Dans l'interface admin, section "Utilisateurs"
- Trouvez l'utilisateur en attente
- Cliquez sur "Approuver"

### 4. Créer un tournoi
- Interface admin → Section "Tournois"
- Cliquez sur "Créer un tournoi"
- Remplissez les informations (nom, description, frais, nombre de participants)

### 5. Démarrer un tournoi
- Une fois les inscriptions validées
- Cliquez sur "Démarrer le tournoi"
- Les brackets seront générés automatiquement

## 🔧 Configuration Avancée

### Base de données PostgreSQL

Pour utiliser PostgreSQL au lieu de SQLite, modifiez `DATABASE_URL` dans `.env` :

```env
DATABASE_URL=postgresql://user:password@localhost/dbname
```

### Déploiement sur Render

1. Créez un nouveau service Web sur Render
2. Connectez votre dépôt Git
3. Configurez les variables d'environnement :
   - `SECRET_KEY`
   - `DATABASE_URL` (ajoutez un service PostgreSQL)
   - `ADMIN_EMAIL`
   - `ADMIN_PASSWORD`
4. Définissez la commande de démarrage : `uvicorn main:app --host 0.0.0.0 --port $PORT`

## 🐛 Dépannage

### Erreur "Module not found"
```bash
pip install -r requirements.txt
```

### Erreur de base de données
```bash
# Supprimez le fichier .db et réinitialisez
rm efootball_tournament.db  # Linux/Mac
del efootball_tournament.db  # Windows
python init_db.py
```

### Port déjà utilisé
Modifiez le port dans `run.py` ou utilisez :
```bash
uvicorn main:app --port 8001
```

## 📚 Documentation API

Une fois le serveur démarré, accédez à :
- **Swagger UI** : http://localhost:8000/docs
- **ReDoc** : http://localhost:8000/redoc

Toutes les routes API sont documentées automatiquement.

## 🔐 Sécurité en Production

⚠️ **Avant de déployer en production :**

1. Changez `SECRET_KEY` par une clé aléatoire forte
2. Changez `ADMIN_PASSWORD`
3. Utilisez PostgreSQL au lieu de SQLite
4. Activez HTTPS
5. Configurez les CORS correctement
6. Utilisez des variables d'environnement pour les secrets
7. Activez les logs et le monitoring
8. Faites des sauvegardes régulières de la base de données

