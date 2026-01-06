# Configuration Render.com

## Problème résolu

L'application doit écouter sur `0.0.0.0` et utiliser le port de la variable d'environnement `PORT`.

## Solutions

### Option 1 : Utiliser gunicorn (recommandé)

Dans les paramètres Render.com, configurez la **Start Command** :
```
gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 2 --timeout 120 app:app
```

### Option 2 : Utiliser le Procfile

Le fichier `Procfile` contient déjà :
```
web: gunicorn app:app
```

Render devrait le détecter automatiquement. Si ce n'est pas le cas, utilisez l'Option 1.

### Option 3 : Utiliser python app.py (si nécessaire)

Si vous devez utiliser `python app.py`, le code a été modifié pour :
- Écouter sur `0.0.0.0` au lieu de `127.0.0.1`
- Utiliser le port de la variable d'environnement `PORT`
- Désactiver le mode debug en production

## Configuration dans Render.com

1. Allez dans les paramètres de votre service web
2. Dans **Start Command**, entrez :
   ```
   gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 2 --timeout 120 app:app
   ```
3. Sauvegardez et redéployez

## Variables d'environnement

Assurez-vous d'avoir configuré :
- `SECRET_KEY` : Une clé secrète aléatoire
- `PORT` : Automatiquement défini par Render (ne pas définir manuellement)
- `DATABASE_URL` : URL de votre base de données (si vous utilisez PostgreSQL)

## Vérification

Après le déploiement, vérifiez les logs. Vous devriez voir :
- `Starting Flask app on 0.0.0.0:XXXX` (si python app.py)
- Ou `Listening at: http://0.0.0.0:XXXX` (si gunicorn)

Si vous voyez encore `127.0.0.1:5000`, les modifications n'ont pas été prises en compte.

