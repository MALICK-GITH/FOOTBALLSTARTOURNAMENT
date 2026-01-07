"""
Script d'initialisation de la base de données
Crée les tables et un compte administrateur par défaut
"""
from database import engine, Base, SessionLocal
from models import User, UserRole
from auth import get_password_hash
from config import settings

def init_db():
    """Initialiser la base de données"""
    print("Création des tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables créées avec succès!")
    
    # Créer l'admin par défaut
    db = SessionLocal()
    try:
        admin_user = db.query(User).filter(User.email == settings.ADMIN_EMAIL).first()
        if not admin_user:
            admin_user = User(
                email=settings.ADMIN_EMAIL,
                username="admin",
                full_name="Administrateur",
                hashed_password=get_password_hash(settings.ADMIN_PASSWORD),
                role=UserRole.ADMIN,
                is_active=True,
                is_verified=True
            )
            db.add(admin_user)
            db.commit()
            print(f"Compte administrateur créé:")
            print(f"  Email: {settings.ADMIN_EMAIL}")
            print(f"  Password: {settings.ADMIN_PASSWORD}")
        else:
            print("Compte administrateur existe déjà")
    finally:
        db.close()

if __name__ == "__main__":
    init_db()

