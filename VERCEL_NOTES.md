# 📝 Notes pour le déploiement sur Vercel

## ⚠️ Limitations importantes

### Système de fichiers
Vercel utilise un système de fichiers **read-only** (sauf `/tmp`). Les fichiers dans `/tmp` ne persistent **PAS** entre les invocations serverless.

**Conséquence** : Les données (joueurs, bracket) seront perdues à chaque redémarrage de la fonction serverless.

## 🔧 Solutions recommandées

### Option 1 : Base de données (Recommandé)
Utilisez une base de données pour stocker les données de manière persistante :

- **Vercel Postgres** (recommandé)
- **Supabase** (gratuit)
- **MongoDB Atlas** (gratuit)
- **PlanetScale** (MySQL serverless)

### Option 2 : Vercel KV (Key-Value Store)
Utilisez Vercel KV pour stocker les données JSON.

### Option 3 : Service externe
- **Firebase Firestore**
- **AWS DynamoDB**
- **Google Cloud Firestore**

## 🚀 Déploiement actuel

Le code actuel utilise `/tmp` pour les fichiers, ce qui fonctionne mais :
- ✅ L'application démarre sans erreur
- ❌ Les données ne persistent pas entre les redémarrages
- ⚠️ Les uploads de fichiers fonctionnent temporairement

## 📋 Modifications apportées

1. **Détection Vercel** : Le code détecte automatiquement si on est sur Vercel
2. **Utilisation de `/tmp`** : Tous les fichiers sont stockés dans `/tmp`
3. **Gestion d'erreurs** : Toutes les opérations de fichiers sont protégées par try/except
4. **Valeurs par défaut** : Si les fichiers n'existent pas, des valeurs par défaut sont utilisées

## 🔄 Prochaines étapes recommandées

Pour une solution de production, migrez vers une base de données :

1. Créez un compte sur Vercel Postgres ou Supabase
2. Modifiez `app.py` pour utiliser la base de données au lieu de fichiers JSON
3. Les données seront persistantes et l'application sera plus robuste

## 🧪 Test local avec Vercel

```bash
# Installer Vercel CLI
npm i -g vercel

# Tester localement
vercel dev
```

## 📞 Support

Si vous rencontrez des erreurs :
1. Vérifiez les logs dans le dashboard Vercel
2. Assurez-vous que `VERCEL=1` est défini dans les variables d'environnement
3. Vérifiez que tous les fichiers sont bien déployés

---

**Note** : Pour un tournoi réel, utilisez une base de données pour garantir la persistance des données.

