from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional
from datetime import datetime

from database import get_db
from models import (
    User, Tournament, TournamentRegistration, Match, Bracket,
    ActivityLog, AdminMessage, RegistrationStatus, UserRole
)
from schemas import (
    UserResponse, TournamentCreate, TournamentResponse,
    RegistrationResponse, MatchResponse, AdminMessageCreate, AdminMessageResponse
)
from auth import get_current_admin

router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.get("/users", response_model=List[UserResponse])
async def get_all_users(
    skip: int = 0,
    limit: int = 100,
    status_filter: Optional[str] = None,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Obtenir tous les utilisateurs"""
    query = db.query(User)
    
    if status_filter:
        query = query.filter(User.registration_status == status_filter)
    
    users = query.order_by(desc(User.created_at)).offset(skip).limit(limit).all()
    return users


@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Obtenir un utilisateur spécifique"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return user


@router.put("/users/{user_id}/approve")
async def approve_user(
    user_id: int,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Approuver un utilisateur"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    
    user.registration_status = RegistrationStatus.APPROVED
    user.is_verified = True
    db.commit()
    
    # Log activité
    log = ActivityLog(
        action="USER_APPROVED",
        details=f"Utilisateur {user.email} approuvé par {current_user.email}",
        user_id=current_user.id
    )
    db.add(log)
    db.commit()
    
    return {"message": "Utilisateur approuvé avec succès"}


@router.put("/users/{user_id}/reject")
async def reject_user(
    user_id: int,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Refuser un utilisateur"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    
    user.registration_status = RegistrationStatus.REJECTED
    db.commit()
    
    # Log activité
    log = ActivityLog(
        action="USER_REJECTED",
        details=f"Utilisateur {user.email} refusé par {current_user.email}",
        user_id=current_user.id
    )
    db.add(log)
    db.commit()
    
    return {"message": "Utilisateur refusé"}


@router.put("/users/{user_id}/block")
async def block_user(
    user_id: int,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Bloquer un utilisateur"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    
    if user.role == UserRole.ADMIN:
        raise HTTPException(status_code=400, detail="Impossible de bloquer un administrateur")
    
    user.is_active = False
    db.commit()
    
    # Log activité
    log = ActivityLog(
        action="USER_BLOCKED",
        details=f"Utilisateur {user.email} bloqué par {current_user.email}",
        user_id=current_user.id
    )
    db.add(log)
    db.commit()
    
    return {"message": "Utilisateur bloqué"}


@router.put("/users/{user_id}/unblock")
async def unblock_user(
    user_id: int,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Débloquer un utilisateur"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    
    user.is_active = True
    db.commit()
    
    # Log activité
    log = ActivityLog(
        action="USER_UNBLOCKED",
        details=f"Utilisateur {user.email} débloqué par {current_user.email}",
        user_id=current_user.id
    )
    db.add(log)
    db.commit()
    
    return {"message": "Utilisateur débloqué"}


@router.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Supprimer un utilisateur"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    
    if user.role == UserRole.ADMIN:
        raise HTTPException(status_code=400, detail="Impossible de supprimer un administrateur")
    
    # Log avant suppression
    log = ActivityLog(
        action="USER_DELETED",
        details=f"Utilisateur {user.email} supprimé par {current_user.email}",
        user_id=current_user.id
    )
    db.add(log)
    
    db.delete(user)
    db.commit()
    
    return {"message": "Utilisateur supprimé"}


@router.get("/registrations", response_model=List[RegistrationResponse])
async def get_all_registrations(
    skip: int = 0,
    limit: int = 100,
    status_filter: Optional[str] = None,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Obtenir toutes les inscriptions"""
    query = db.query(TournamentRegistration)
    
    if status_filter:
        query = query.filter(TournamentRegistration.status == status_filter)
    
    registrations = query.order_by(desc(TournamentRegistration.created_at)).offset(skip).limit(limit).all()
    return registrations


@router.get("/activity-logs")
async def get_activity_logs(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Obtenir les logs d'activité"""
    logs = db.query(ActivityLog).order_by(desc(ActivityLog.created_at)).offset(skip).limit(limit).all()
    return logs


@router.post("/tournaments", response_model=TournamentResponse)
async def create_tournament(
    tournament: TournamentCreate,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Créer un nouveau tournoi"""
    db_tournament = Tournament(**tournament.dict())
    db.add(db_tournament)
    db.commit()
    db.refresh(db_tournament)
    
    # Log activité
    log = ActivityLog(
        action="TOURNAMENT_CREATED",
        details=f"Tournoi {db_tournament.name} créé",
        user_id=current_user.id
    )
    db.add(log)
    db.commit()
    
    return db_tournament


@router.put("/users/{user_id}/promote-admin")
async def promote_to_admin(
    user_id: int,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Promouvoir un utilisateur en administrateur (admin uniquement)"""
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

