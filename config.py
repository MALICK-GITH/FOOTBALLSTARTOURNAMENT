import os
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Application
    SECRET_KEY: str = os.getenv("SECRET_KEY", "change-this-secret-key-in-production-min-32-chars")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_DAYS: int = 30
    
    # Database
    # Pour Render/PostgreSQL, utiliser la variable d'environnement DATABASE_URL
    # Pour SQLite local, utiliser sqlite:///./efootball_tournament.db
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./efootball_tournament.db")
    
    # Admin
    ADMIN_EMAIL: str = os.getenv("ADMIN_EMAIL", "admin@tournament.com")
    ADMIN_PASSWORD: str = os.getenv("ADMIN_PASSWORD", "ChangeMe123!")
    
    # File Upload
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "static/uploads")
    MAX_UPLOAD_SIZE: int = int(os.getenv("MAX_UPLOAD_SIZE", "5242880"))  # 5MB
    ALLOWED_EXTENSIONS: set = set(os.getenv("ALLOWED_EXTENSIONS", "jpg,jpeg,png,pdf").split(","))
    
    # CORS
    CORS_ORIGINS: list = ["*"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

# Créer le dossier uploads s'il n'existe pas
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(f"{settings.UPLOAD_DIR}/profiles", exist_ok=True)
os.makedirs(f"{settings.UPLOAD_DIR}/payments", exist_ok=True)

