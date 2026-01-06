# Tournoi eFootball 2026 - Site Web

Site web complet pour la gestion d'un tournoi eFootball, développé en HTML/CSS/JavaScript pur (frontend uniquement).

## Fonctionnalités

### Pages disponibles

1. **Accueil (index.html)**
   - Présentation du tournoi
   - Navigation vers toutes les sections

2. **Inscription (inscription.html)**
   - Formulaire d'inscription avec validation côté client
   - Upload de photo de profil (optionnel)
   - Upload de screenshot de paiement Mobile Money (optionnel)
   - Validation des formats d'images (PNG, JPG, JPEG, GIF, WEBP, max 5MB)
   - Prévisualisation des images avant soumission

3. **Connexion (connexion.html)**
   - Authentification des joueurs
   - Redirection vers le bracket après connexion

4. **Admin (admin.html)**
   - Connexion sécurisée (pseudo: `admin`, mot de passe: `admin123`)
   - Gestion des inscriptions (approuver, refuser, supprimer)
   - Visualisation des messages des joueurs
   - Affichage des photos de profil et screenshots
   - Filtrage par statut (En attente, Approuvés, Refusés)

5. **Bracket (bracket.html)**
   - Affichage du tournoi avec les joueurs approuvés
   - Génération automatique du bracket
   - Mise à jour dynamique

## Utilisation

### Pour les joueurs

1. Accédez à la page **Inscription**
2. Remplissez le formulaire (pseudo et mot de passe obligatoires)
3. Optionnellement, uploadez votre photo de profil et le screenshot de paiement
4. Entrez votre numéro de paiement Mobile Money
5. Soumettez le formulaire
6. Attendez la validation par l'administrateur

### Pour l'administrateur

1. Accédez à la page **Admin**
2. Connectez-vous avec :
   - Pseudo: `admin`
   - Mot de passe: `admin123`
3. Gérez les inscriptions :
   - Approuvez les joueurs validés
   - Refusez les inscriptions non conformes
   - Supprimez les inscriptions si nécessaire
4. Consultez les messages des joueurs dans l'onglet "Messages"

## Stockage des données

Les données sont stockées localement dans le navigateur via `localStorage`. Cela signifie que :
- Les données sont conservées entre les sessions
- Chaque navigateur a ses propres données
- Pour un déploiement réel, il faudrait un backend avec une vraie base de données

## Structure des fichiers

```
.
├── index.html          # Page d'accueil
├── inscription.html    # Page d'inscription
├── connexion.html      # Page de connexion
├── admin.html          # Page d'administration
├── bracket.html        # Page du bracket
├── styles.css          # Styles CSS communs
├── script.js           # Scripts communs
├── inscription.js      # Logique d'inscription
├── connexion.js        # Logique de connexion
├── admin.js            # Logique d'administration
└── bracket.js          # Logique du bracket
```

## Caractéristiques techniques

- **100% Frontend** : Aucun backend requis
- **Responsive** : Compatible mobile, tablette et desktop
- **Validation côté client** : Vérification des formats et tailles de fichiers
- **Prévisualisation d'images** : Affichage des images avant soumission
- **Messages de feedback** : Messages de succès et d'erreur clairs
- **Design moderne** : Interface utilisateur soignée et intuitive

## Notes de sécurité

⚠️ **Important** : Ce site utilise `localStorage` pour le stockage des données. En production, il est fortement recommandé de :
- Utiliser un backend sécurisé
- Hasher les mots de passe (actuellement stockés en clair)
- Implémenter une authentification sécurisée
- Valider les données côté serveur
- Protéger contre les attaques XSS et CSRF

## Compatibilité

- Navigateurs modernes (Chrome, Firefox, Safari, Edge)
- Support des fonctionnalités ES6+
- Responsive design pour tous les écrans

