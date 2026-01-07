from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List

from database import get_db
from models import AdminMessage, ActivityLog
from schemas import AdminMessageCreate, AdminMessageResponse
from auth import get_current_active_user, get_current_admin

router = APIRouter(prefix="/api/messages", tags=["messages"])


@router.get("/", response_model=List[AdminMessageResponse])
async def get_messages(
    db: Session = Depends(get_db)
):
    """Obtenir tous les messages actifs"""
    messages = db.query(AdminMessage).filter(
        AdminMessage.is_active == True
    ).order_by(desc(AdminMessage.is_important), desc(AdminMessage.created_at)).all()
    return messages


@router.post("/", response_model=AdminMessageResponse)
async def create_message(
    message: AdminMessageCreate,
    current_user = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Créer un nouveau message admin (admin uniquement)"""
    db_message = AdminMessage(
        **message.dict(),
        created_by=current_user.id
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    
    # Log activité
    log = ActivityLog(
        action="MESSAGE_CREATED",
        details=f"Message '{db_message.title}' créé",
        user_id=current_user.id
    )
    db.add(log)
    db.commit()
    
    return db_message


@router.put("/{message_id}", response_model=AdminMessageResponse)
async def update_message(
    message_id: int,
    message: AdminMessageCreate,
    current_user = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Mettre à jour un message (admin uniquement)"""
    db_message = db.query(AdminMessage).filter(AdminMessage.id == message_id).first()
    if not db_message:
        raise HTTPException(status_code=404, detail="Message non trouvé")
    
    db_message.title = message.title
    db_message.content = message.content
    db_message.is_important = message.is_important
    db.commit()
    db.refresh(db_message)
    
    # Log activité
    log = ActivityLog(
        action="MESSAGE_UPDATED",
        details=f"Message '{db_message.title}' mis à jour",
        user_id=current_user.id
    )
    db.add(log)
    db.commit()
    
    return db_message


@router.delete("/{message_id}")
async def delete_message(
    message_id: int,
    current_user = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Supprimer un message (admin uniquement)"""
    db_message = db.query(AdminMessage).filter(AdminMessage.id == message_id).first()
    if not db_message:
        raise HTTPException(status_code=404, detail="Message non trouvé")
    
    # Log activité
    log = ActivityLog(
        action="MESSAGE_DELETED",
        details=f"Message '{db_message.title}' supprimé",
        user_id=current_user.id
    )
    db.add(log)
    
    db_message.is_active = False
    db.commit()
    
    return {"message": "Message supprimé"}

