from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from database import get_db
from models import Match, Tournament, User, MatchStatus
from schemas import MatchResponse, MatchBase
from auth import get_current_admin

router = APIRouter(prefix="/api/matches", tags=["matches"])


@router.put("/{match_id}/score", response_model=MatchResponse)
async def update_match_score(
    match_id: int,
    match_data: MatchBase,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Mettre à jour le score d'un match (admin uniquement)"""
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Match non trouvé")
    
    # Mettre à jour les scores
    if match_data.player1_score is not None:
        match.player1_score = match_data.player1_score
    if match_data.player2_score is not None:
        match.player2_score = match_data.player2_score
    
    # Déterminer le gagnant
    if match.player1_score is not None and match.player2_score is not None:
        if match.player1_score > match.player2_score:
            match.winner_id = match.player1_id
        elif match.player2_score < match.player1_score:
            match.winner_id = match.player2_id
        # En cas d'égalité, pas de gagnant pour l'instant
        
        match.status = MatchStatus.PLAYED
        match.is_manually_set = True
    
    if match_data.notes:
        match.notes = match_data.notes
    
    db.commit()
    db.refresh(match)
    
    return match


@router.get("/{match_id}", response_model=MatchResponse)
async def get_match(
    match_id: int,
    db: Session = Depends(get_db)
):
    """Obtenir un match spécifique"""
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Match non trouvé")
    return match

