# 🚀 Guide de Déploiement sur Render

## Configuration pour Render

### 📋 Fichiers nécessaires

Render utilise ces fichiers automatiquement :
- ✅ `requirements.txt` - Dépendances Python
- ✅ `main.py` - Point d'entrée de l'application
- ✅ `render.yaml` - Configuration Render (optionnel mais recommandé)

### ⚙️ Configuration dans Render Dashboard

#### 1. **Build Command** (Commande de build)
```
pip install -r requirements.txt
```

#### 2. **Start Command** (Commande de démarrage) ⭐ **IMPORTANT**
```
uvicorn main:app --host 0.0.0.0 --port $PORT
```

**⚠️ Ne PAS utiliser `run.py`** - Render gère le port automatiquement via `$PORT`

### 🔐 Variables d'environnement à configurer

Dans Render Dashboard → Environment Variables, ajoutez :

| Variable | Valeur | Exemple |
|----------|--------|---------|
| `SECRET_KEY` | Clé secrète (min 32 chars) | `votre-cle-secrete-super-longue-et-aleatoire-123456789` |
| `DATABASE_URL` | URL PostgreSQL (auto-générée si vous créez une DB) | `postgresql://user:pass@host/db` |
| `ADMIN_EMAIL` | Email du compte admin | `admin@tournament.com` |
| `ADMIN_PASSWORD` | Mot de passe admin | `ChangeMe123!` (⚠️ Changez-le!) |
| `UPLOAD_DIR` | Dossier uploads (optionnel) | `static/uploads` |
| `PYTHON_VERSION` | Version Python (optionnel) | `3.11.0` |

### 📝 Étapes de déploiement

#### Option A : Déploiement automatique avec render.yaml

1. **Poussez votre code sur GitHub/GitLab/Bitbucket**
2. **Dans Render Dashboard** :
   - Cliquez sur "New" → "Blueprint"
   - Connectez votre dépôt
   - Render détectera automatiquement `render.yaml`
   - Configurez les variables d'environnement manquantes
   - Déployez !

#### Option B : Déploiement manuel

1. **Créez un Web Service** :
   - Dans Render Dashboard → "New" → "Web Service"
   - Connectez votre dépôt Git

2. **Configurez le service** :
   - **Name** : `efootball-tournament-platform`
   - **Environment** : `Python 3`
   - **Build Command** : `pip install -r requirements.txt`
   - **Start Command** : `uvicorn main:app --host 0.0.0.0 --port $PORT`

3. **Créez une base de données PostgreSQL** :
   - "New" → "PostgreSQL"
   - Choisissez un nom (ex: `efootball-db`)
   - Render génère automatiquement `DATABASE_URL`

4. **Ajoutez les variables d'environnement** :
   - Dans votre service web → "Environment"
   - Ajoutez toutes les variables listées ci-dessus
   - Pour `DATABASE_URL`, copiez depuis votre base de données PostgreSQL

5. **Déployez** :
   - Cliquez sur "Create Web Service"
   - Render build et démarre automatiquement

### 🔍 Vérifications après déploiement

1. **Vérifiez les logs** :
   - Render Dashboard → Votre service → "Logs"
   - Cherchez : "Application startup complete"
   - Pas d'erreurs rouges

2. **Testez l'application** :
   - Accédez à votre URL Render (ex: `https://efootball-tournament.onrender.com`)
   - Vérifiez que la page d'accueil s'affiche
   - Testez `/admin` avec les identifiants admin

3. **Vérifiez la base de données** :
   - Les tables doivent être créées automatiquement au premier démarrage
   - Le compte admin doit être créé automatiquement

### ⚠️ Points importants

#### 1. **Le PORT est géré par Render**
```bash
# ❌ NE PAS FAIRE
uvicorn main:app --port 8000

# ✅ CORRECT
uvicorn main:app --host 0.0.0.0 --port $PORT
```

#### 2. **Pas de reload en production**
```bash
# ❌ NE PAS UTILISER
uvicorn main:app --reload

# ✅ CORRECT
uvicorn main:app --host 0.0.0.0 --port $PORT
```

#### 3. **Base de données PostgreSQL recommandée**
- SQLite fonctionne mais ne persiste pas entre les redémarrages
- PostgreSQL est gratuit sur Render (plan free)
- `DATABASE_URL` est fourni automatiquement

#### 4. **Fichiers statiques**
- Les uploads (`static/uploads/`) ne persistent pas entre les builds
- Utilisez un service de stockage (S3, Cloudinary) pour la production
- Ou activez le "Persistent Disk" sur Render (payant)

### 🔧 Commandes de démarrage alternatives

Si `uvicorn` ne fonctionne pas, essayez :

```bash
# Option 1 (recommandée)
uvicorn main:app --host 0.0.0.0 --port $PORT

# Option 2 (si problème avec uvicorn)
python -m uvicorn main:app --host 0.0.0.0 --port $PORT

# Option 3 (via gunicorn si installé)
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
```

### 📊 Monitoring

**Logs en temps réel** :
- Render Dashboard → Votre service → "Logs"
- Tous les prints/erreurs Python apparaissent ici

**Health Check** :
- Render vérifie automatiquement que votre service répond
- Si `/` ne répond pas, le service est marqué comme down

### 🐛 Résolution de problèmes

#### Erreur "Port already in use"
- Vérifiez que vous utilisez `$PORT` et pas un port fixe

#### Erreur "Module not found"
- Vérifiez que `requirements.txt` contient toutes les dépendances
- Les logs de build montrent quels modules échouent

#### Erreur de connexion à la base de données
- Vérifiez que `DATABASE_URL` est correctement configurée
- Assurez-vous que la base PostgreSQL est créée et accessible
- Pour SQLite, utilisez un chemin absolu : `/tmp/efootball.db`

#### Erreur "Application failed to respond"
- Vérifiez les logs pour voir l'erreur exacte
- Vérifiez que `main:app` est correct (app doit être dans main.py)

### 📝 Résumé des commandes

| Action | Commande |
|--------|----------|
| **Build** | `pip install -r requirements.txt` |
| **Start** | `uvicorn main:app --host 0.0.0.0 --port $PORT` |
| **Version Python** | `3.11.0` (recommandé) |

### ✅ Checklist avant déploiement

- [ ] `requirements.txt` est à jour
- [ ] `main.py` existe et contient `app = FastAPI(...)`
- [ ] Toutes les variables d'environnement sont configurées
- [ ] Base de données PostgreSQL créée (ou SQLite configuré)
- [ ] `SECRET_KEY` est aléatoire et sécurisé
- [ ] `ADMIN_PASSWORD` est changé
- [ ] Start Command utilise `$PORT`
- [ ] Testé en local avec `uvicorn main:app`

Une fois déployé, votre application sera accessible via l'URL fournie par Render ! 🎉

