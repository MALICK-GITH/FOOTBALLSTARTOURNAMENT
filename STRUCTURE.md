# 📁 Structure du Projet eFootKings 2026 🇨🇮

## Structure complète des fichiers

```
kingsefootball2026/
│
├── 📄 app.py                          # Application Flask principale
│   └── Routes : /, /register, /bracket, /admin/*
│
├── 📄 init.py                         # Script d'initialisation (création dossiers)
│
├── 📄 requirements.txt                # Dépendances Python
│   └── Flask, Werkzeug, Gunicorn
│
├── 📄 vercel.json                     # Configuration Vercel pour déploiement
│
├── 📄 package.json                    # Scripts npm pour Vercel
│
├── 📄 .gitignore                      # Fichiers à ignorer par Git
│
├── 📄 README.md                       # Documentation du projet
│
├── 📄 STRUCTURE.md                    # Ce fichier (structure du projet)
│
├── 📁 api/
│   └── 📄 index.py                    # Point d'entrée serverless pour Vercel
│
├── 📁 templates/                      # Templates HTML Jinja2
│   ├── 📄 base.html                   # Template de base (navigation, footer)
│   ├── 📄 index.html                  # Page d'accueil
│   ├── 📄 register.html               # Formulaire d'inscription
│   ├── 📄 bracket.html                # Affichage du bracket
│   ├── 📄 admin_login.html            # Page de connexion admin
│   └── 📄 admin_dashboard.html        # Dashboard administrateur
│
└── 📁 static/                         # Fichiers statiques
    ├── 📁 css/
    │   └── 📄 style.css               # Styles personnalisés (thème sombre, jaune)
    └── 📁 js/
        └── 📄 main.js                 # JavaScript principal
```

## 📂 Dossiers créés automatiquement

Ces dossiers sont créés automatiquement lors du premier lancement :

```
kingsefootball2026/
│
├── 📁 data/                           # Données JSON (créé par app.py)
│   ├── 📄 players.json                # Liste des joueurs inscrits
│   ├── 📄 bracket.json                # Données du bracket
│   └── 📄 admin.json                  # Identifiants admin (hashés)
│
└── 📁 uploads/                        # Screenshots de paiement (créé par app.py)
    └── 📄 [fichiers uploadés]         # Images des paiements Mobile Money
```

## 🗂️ Description des fichiers principaux

### **app.py** (Application Flask)
- **Routes publiques** :
  - `/` → Page d'accueil
  - `/register` → Formulaire d'inscription
  - `/bracket` → Affichage du bracket
  - `/uploads/<filename>` → Accès aux screenshots

- **Routes admin** :
  - `/admin/login` → Connexion admin
  - `/admin/logout` → Déconnexion
  - `/admin/dashboard` → Dashboard de gestion
  - `/admin/validate/<player_id>` → Valider/refuser un joueur
  - `/admin/update-bracket` → Mettre à jour les scores

### **Templates HTML**

1. **base.html** : Template de base avec :
   - Navigation responsive
   - Footer
   - Intégration Bootstrap 5, Font Awesome, Animate.css
   - Gestion des messages flash

2. **index.html** : Page d'accueil avec :
   - Hero section
   - Images du tournoi (3 images)
   - Règles du tournoi
   - Informations de paiement
   - Boutons CTA

3. **register.html** : Formulaire d'inscription avec :
   - Champ pseudo eFootball (obligatoire)
   - Champ contact (optionnel)
   - Upload screenshot paiement
   - Preview de l'image

4. **bracket.html** : Affichage du bracket avec :
   - Quarts de finale
   - Demi-finales
   - Finale
   - Affichage des scores et gagnants

5. **admin_login.html** : Page de connexion sécurisée

6. **admin_dashboard.html** : Dashboard avec :
   - Statistiques (total, validés, en attente)
   - Liste des joueurs avec actions
   - Gestion du bracket (scores)

### **Fichiers statiques**

- **style.css** : 
  - Thème sombre (#111)
  - Accents jaunes (#ffcc00)
  - Animations et hover effects
  - Responsive design

- **main.js** :
  - Auto-dismiss des alerts
  - Validation de formulaires
  - Preview d'images
  - Gestion des boutons admin

## 🔧 Configuration

### **vercel.json**
Configuration pour déploiement Vercel :
- Build avec `@vercel/python`
- Routes pour fichiers statiques
- Variables d'environnement

### **requirements.txt**
Dépendances Python :
- Flask 3.0.0
- Werkzeug 3.0.1 (hashing passwords)
- Gunicorn 21.2.0 (serveur production)

## 📊 Flux de données

```
Inscription → players.json
     ↓
Validation admin → players.json (status: validated)
     ↓
8 joueurs validés → bracket.json (quarterfinals générés)
     ↓
Mise à jour scores → bracket.json (semifinals, final, winner)
```

## 🎨 Technologies utilisées

- **Backend** : Flask (Python)
- **Frontend** : HTML5, CSS3, JavaScript
- **Framework CSS** : Bootstrap 5
- **Icônes** : Font Awesome 6.4.0
- **Polices** : Google Fonts (Poppins)
- **Animations** : Animate.css 4.1.1
- **Stockage** : JSON files
- **Déploiement** : Vercel (serverless)

## 🚀 Commandes utiles

```bash
# Initialiser le projet
python init.py

# Lancer en local
python app.py

# Tester avec Vercel local
vercel dev

# Déployer sur Vercel
vercel
```

## 📝 Notes importantes

1. **Sécurité** : Changez le `SECRET_KEY` et le mot de passe admin en production
2. **Données** : Les fichiers JSON sont créés automatiquement
3. **Uploads** : Les screenshots sont stockés dans `uploads/`
4. **Limite** : Maximum 8 joueurs validés pour générer le bracket

---

✅ Structure complète et prête pour le déploiement !

