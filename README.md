# eFootball Mobile 2026 Tournament Platform

Plateforme professionnelle complète pour l'organisation de tournois eFootball Mobile 2026 avec gestion d'inscriptions payantes, brackets dynamiques et administration complète.

## 🚀 Installation

1. Créer un environnement virtuel :
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

2. Installer les dépendances :
```bash
pip install -r requirements.txt
```

3. Configurer les variables d'environnement :
```bash
cp .env.example .env
# Modifier .env avec vos valeurs
```

4. Initialiser la base de données :
```bash
python init_db.py
```

5. Lancer le serveur :
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Accéder à l'application : http://localhost:8000

## 📁 Structure du projet

```
├── main.py                 # Point d'entrée FastAPI
├── config.py              # Configuration
├── database.py            # Configuration base de données
├── models.py              # Modèles SQLAlchemy
├── schemas.py             # Schémas Pydantic
├── auth.py                # Authentification
├── routes/
│   ├── users.py           # Routes utilisateurs
│   ├── admin.py           # Routes admin
│   ├── tournaments.py     # Routes tournois
│   └── messages.py        # Routes messages
├── static/
│   ├── css/
│   ├── js/
│   └── uploads/           # Fichiers uploadés
└── templates/
    ├── index.html
    ├── admin.html
    └── ...
```

## 🔐 Compte administrateur

Par défaut, un compte admin est créé avec :
- Email : défini dans `.env` (ADMIN_EMAIL)
- Mot de passe : défini dans `.env` (ADMIN_PASSWORD)

⚠️ **Changez ces valeurs en production !**

## 🛡️ Sécurité

- Mots de passe hashés avec bcrypt
- Protection CSRF
- Validation stricte des fichiers
- Sessions sécurisées
- Logs d'audit

