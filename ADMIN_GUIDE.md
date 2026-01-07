# 👑 Guide de Gestion des Administrateurs

## Comment le système reconnaît un administrateur

Le système utilise le champ `role` dans la table `User` pour identifier les administrateurs :

```python
# Deux rôles possibles
UserRole.ADMIN   # = "admin"
UserRole.PLAYER  # = "player" (défaut)
```

**Chaque route d'administration vérifie le rôle :**
```python
# Dans routes/admin.py, routes/tournaments.py, etc.
@router.get("/admin/users")
async def get_all_users(
    current_user: User = Depends(get_current_admin)  # ⭐ Vérifie que c'est un admin
):
    # ...
```

## Méthodes de création d'un compte administrateur

### ✅ Méthode 1 : Création automatique (recommandé)

Lors du **premier démarrage** de l'application, un compte admin est créé automatiquement si il n'existe pas.

**Configuration dans `.env` :**
```env
ADMIN_EMAIL=admin@tournament.com
ADMIN_PASSWORD=ChangeMe123!
```

**Lors du démarrage (`python run.py`) :**
- Le système vérifie si un utilisateur avec cet email existe
- Si non → création automatique avec `role=ADMIN`
- Si oui → rien n'est fait (sécurité)

### ✅ Méthode 2 : Script d'initialisation

```bash
python init_db.py
```

Ce script :
1. Crée toutes les tables
2. Crée le compte admin par défaut (si il n'existe pas)

### ✅ Méthode 3 : Promouvoir un utilisateur existant

Vous pouvez modifier directement la base de données pour promouvoir un utilisateur :

**Option A : Via Python (script temporaire)**

Créez un fichier `promote_admin.py` :

```python
from database import SessionLocal
from models import User, UserRole

# Remplacez par l'email de l'utilisateur à promouvoir
EMAIL_TO_PROMOTE = "user@example.com"

db = SessionLocal()
try:
    user = db.query(User).filter(User.email == EMAIL_TO_PROMOTE).first()
    if user:
        user.role = UserRole.ADMIN
        user.is_verified = True
        db.commit()
        print(f"✅ {user.email} est maintenant administrateur!")
    else:
        print(f"❌ Utilisateur {EMAIL_TO_PROMOTE} non trouvé")
finally:
    db.close()
```

Puis exécutez : `python promote_admin.py`

**Option B : Via SQL direct (SQLite)**

```bash
sqlite3 efootball_tournament.db
```

```sql
-- Voir tous les utilisateurs
SELECT id, email, username, role FROM users;

-- Promouvoir un utilisateur (remplacez 1 par l'ID)
UPDATE users SET role = 'admin' WHERE id = 1;

-- Vérifier
SELECT id, email, username, role FROM users WHERE role = 'admin';
```

**Option C : Ajouter une route admin (recommandé pour production)**

Ajoutez cette route dans `routes/admin.py` :

```python
@router.put("/users/{user_id}/promote-admin")
async def promote_to_admin(
    user_id: int,
    current_user: User = Depends(get_current_admin),  # Seul un admin peut promouvoir
    db: Session = Depends(get_db)
):
    """Promouvoir un utilisateur en administrateur"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    
    if user.role == UserRole.ADMIN:
        raise HTTPException(status_code=400, detail="Déjà administrateur")
    
    user.role = UserRole.ADMIN
    user.is_verified = True
    db.commit()
    
    # Log activité
    log = ActivityLog(
        action="USER_PROMOTED_TO_ADMIN",
        details=f"Utilisateur {user.email} promu administrateur par {current_user.email}",
        user_id=current_user.id
    )
    db.add(log)
    db.commit()
    
    return {"message": "Utilisateur promu administrateur avec succès"}
```

## Vérifier si un utilisateur est admin

### Côté Backend (Python)

```python
from models import UserRole

if user.role == UserRole.ADMIN:
    print("C'est un administrateur")
```

### Côté Frontend (JavaScript)

```javascript
// Dans app.js, après la connexion
if (currentUser.role === 'admin') {
    // Afficher les liens admin
    console.log("Utilisateur est admin");
}
```

## Protection des routes admin

**Toutes les routes administratives utilisent `Depends(get_current_admin)` :**

```python
# Exemple dans routes/admin.py
@router.get("/users")
async def get_all_users(
    current_user: User = Depends(get_current_admin),  # ⭐ Protection
    db: Session = Depends(get_db)
):
    # Seul un admin peut accéder ici
    users = db.query(User).all()
    return users
```

Si un utilisateur non-admin tente d'accéder :
- Code HTTP 403 (Forbidden)
- Message : "Accès administrateur requis"

## Sécurité

⚠️ **Points importants :**

1. **Un seul admin par défaut** : Seul le premier compte admin est créé automatiquement
2. **Pas de promotion automatique** : Les nouveaux utilisateurs sont toujours `PLAYER` par défaut
3. **Protection des admins** : Un admin ne peut pas être bloqué/supprimé par un autre admin (voir `routes/admin.py`)
4. **Logs d'audit** : Toutes les actions admin sont loggées dans `ActivityLog`

## Exemple : Créer plusieurs admins

```python
# Script create_admins.py
from database import SessionLocal
from models import User, UserRole
from auth import get_password_hash

admins = [
    {"email": "admin1@tournament.com", "username": "admin1", "password": "SecurePass123!"},
    {"email": "admin2@tournament.com", "username": "admin2", "password": "SecurePass456!"},
]

db = SessionLocal()
try:
    for admin_data in admins:
        # Vérifier si existe déjà
        existing = db.query(User).filter(User.email == admin_data["email"]).first()
        if not existing:
            admin = User(
                email=admin_data["email"],
                username=admin_data["username"],
                full_name=f"Admin {admin_data['username']}",
                hashed_password=get_password_hash(admin_data["password"]),
                role=UserRole.ADMIN,
                is_active=True,
                is_verified=True
            )
            db.add(admin)
            print(f"✅ Admin créé : {admin_data['email']}")
        else:
            print(f"⚠️  {admin_data['email']} existe déjà")
    
    db.commit()
finally:
    db.close()
```

## Résumé

| Méthode | Quand l'utiliser | Avantages |
|---------|------------------|-----------|
| **Automatique** | Premier démarrage | Simple, aucune action requise |
| **Script init_db.py** | Installation initiale | Contrôle explicite |
| **Promotion manuelle** | Ajouter un admin après création | Flexibilité |
| **Route admin** | Interface graphique | Utilisateur-friendly |

Le champ `role = "admin"` est la **seule** façon dont le système distingue un administrateur d'un joueur normal.

