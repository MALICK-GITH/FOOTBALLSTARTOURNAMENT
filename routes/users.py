from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from fastapi.responses import JSONResponse, FileResponse
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional
import os
import shutil
from pathlib import Path

from database import get_db
from models import User, RegistrationStatus, ActivityLog
from schemas import UserCreate, UserLogin, UserResponse, UserUpdate, Token
from auth import (
    get_current_active_user,
    authenticate_user,
    create_access_token,
    get_password_hash,
    get_current_admin
)
from config import settings

router = APIRouter(prefix="/api/users", tags=["users"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Inscription d'un nouvel utilisateur"""
    # Vérifier si l'email existe déjà
    if db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cet email est déjà utilisé"
        )
    
    # Vérifier si le username existe déjà
    if db.query(User).filter(User.username == user_data.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ce nom d'utilisateur est déjà utilisé"
        )
    
    # Créer l'utilisateur
    hashed_password = get_password_hash(user_data.password)
    db_user = User(
        email=user_data.email,
        username=user_data.username,
        full_name=user_data.full_name,
        phone=user_data.phone,
        hashed_password=hashed_password,
        registration_status=RegistrationStatus.PENDING
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Log activité
    log = ActivityLog(
        action="USER_REGISTERED",
        details=f"Utilisateur {db_user.email} inscrit",
        user_id=db_user.id
    )
    db.add(log)
    db.commit()
    
    return db_user


@router.post("/login", response_model=Token)
async def login(
    user_data: UserLogin,
    db: Session = Depends(get_db)
):
    """Connexion d'un utilisateur"""
    user = authenticate_user(db, user_data.email, user_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Compte désactivé"
        )
    
    # Mettre à jour last_login
    from datetime import datetime
    user.last_login = datetime.utcnow()
    db.commit()
    
    # Créer le token
    expires_delta = None
    if user_data.remember_me:
        from datetime import timedelta
        expires_delta = timedelta(days=30)
    
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=expires_delta
    )
    
    # Log activité
    log = ActivityLog(
        action="USER_LOGIN",
        details=f"Utilisateur {user.email} connecté",
        user_id=user.id
    )
    db.add(log)
    db.commit()
    
    response = JSONResponse(
        content={
            "access_token": access_token,
            "token_type": "bearer",
            "user": UserResponse.from_orm(user).dict()
        }
    )
    # Cookie pour session persistante
    if user_data.remember_me:
        response.set_cookie(
            key="session_token",
            value=access_token,
            max_age=30 * 24 * 60 * 60,  # 30 jours
            httponly=True,
            samesite="lax"
        )
    
    return response


@router.post("/logout")
async def logout():
    """Déconnexion"""
    response = JSONResponse(content={"message": "Déconnecté avec succès"})
    response.delete_cookie(key="session_token")
    return response


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_active_user)):
    """Obtenir les informations de l'utilisateur connecté"""
    return current_user


@router.put("/me", response_model=UserResponse)
async def update_current_user(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Mettre à jour les informations de l'utilisateur connecté"""
    # Vérifier si le username est déjà utilisé
    if user_data.username and user_data.username != current_user.username:
        if db.query(User).filter(User.username == user_data.username).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ce nom d'utilisateur est déjà utilisé"
            )
        current_user.username = user_data.username
    
    if user_data.full_name:
        current_user.full_name = user_data.full_name
    if user_data.phone is not None:
        current_user.phone = user_data.phone
    
    db.commit()
    db.refresh(current_user)
    
    # Log activité
    log = ActivityLog(
        action="USER_UPDATED",
        details=f"Utilisateur {current_user.email} a mis à jour son profil",
        user_id=current_user.id
    )
    db.add(log)
    db.commit()
    
    return current_user


def allowed_file(filename: str) -> bool:
    """Vérifier si le fichier est autorisé"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in settings.ALLOWED_EXTENSIONS


@router.post("/upload-profile-picture")
async def upload_profile_picture(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Uploader une photo de profil"""
    if not file.filename or not allowed_file(file.filename):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Type de fichier non autorisé"
        )
    
    # Vérifier la taille
    contents = await file.read()
    if len(contents) > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Fichier trop volumineux"
        )
    
    # Générer un nom de fichier unique
    file_ext = Path(file.filename).suffix
    filename = f"profile_{current_user.id}_{int(__import__('time').time())}{file_ext}"
    filepath = os.path.join(settings.UPLOAD_DIR, "profiles", filename)
    
    # Supprimer l'ancienne photo si elle existe
    if current_user.profile_picture:
        old_path = os.path.join(settings.UPLOAD_DIR, current_user.profile_picture)
        if os.path.exists(old_path):
            os.remove(old_path)
    
    # Sauvegarder le fichier
    with open(filepath, "wb") as f:
        f.write(contents)
    
    # Mettre à jour l'utilisateur
    current_user.profile_picture = f"profiles/{filename}"
    db.commit()
    
    # Log activité
    log = ActivityLog(
        action="PROFILE_PICTURE_UPLOADED",
        details=f"Photo de profil uploadée",
        user_id=current_user.id
    )
    db.add(log)
    db.commit()
    
    return {"message": "Photo de profil uploadée avec succès", "filename": current_user.profile_picture}


@router.post("/upload-payment-proof")
async def upload_payment_proof(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Uploader une preuve de paiement"""
    if not file.filename or not allowed_file(file.filename):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Type de fichier non autorisé"
        )
    
    # Vérifier la taille
    contents = await file.read()
    if len(contents) > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Fichier trop volumineux"
        )
    
    # Générer un nom de fichier unique
    file_ext = Path(file.filename).suffix
    filename = f"payment_{current_user.id}_{int(__import__('time').time())}{file_ext}"
    filepath = os.path.join(settings.UPLOAD_DIR, "payments", filename)
    
    # Supprimer l'ancienne preuve si elle existe
    if current_user.payment_proof:
        old_path = os.path.join(settings.UPLOAD_DIR, current_user.payment_proof)
        if os.path.exists(old_path):
            os.remove(old_path)
    
    # Sauvegarder le fichier
    with open(filepath, "wb") as f:
        f.write(contents)
    
    # Mettre à jour l'utilisateur
    current_user.payment_proof = f"payments/{filename}"
    db.commit()
    
    # Log activité
    log = ActivityLog(
        action="PAYMENT_PROOF_UPLOADED",
        details=f"Preuve de paiement uploadée",
        user_id=current_user.id
    )
    db.add(log)
    db.commit()
    
    return {"message": "Preuve de paiement uploadée avec succès", "filename": current_user.payment_proof}

