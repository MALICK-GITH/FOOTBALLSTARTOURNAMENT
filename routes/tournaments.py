from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import math

from database import get_db
from models import (
    Tournament, TournamentRegistration, Match, Bracket, User,
    RegistrationStatus, MatchStatus, RoundType
)
from schemas import TournamentResponse, MatchResponse, BracketResponse
from auth import get_current_active_user, get_current_admin
from datetime import datetime

router = APIRouter(prefix="/api/tournaments", tags=["tournaments"])


@router.get("/", response_model=List[TournamentResponse])
async def get_tournaments(
    db: Session = Depends(get_db)
):
    """Obtenir tous les tournois actifs"""
    tournaments = db.query(Tournament).filter(Tournament.is_active == True).all()
    return tournaments


@router.get("/{tournament_id}", response_model=TournamentResponse)
async def get_tournament(
    tournament_id: int,
    db: Session = Depends(get_db)
):
    """Obtenir un tournoi spécifique"""
    tournament = db.query(Tournament).filter(Tournament.id == tournament_id).first()
    if not tournament:
        raise HTTPException(status_code=404, detail="Tournoi non trouvé")
    return tournament


@router.post("/{tournament_id}/register")
async def register_to_tournament(
    tournament_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """S'inscrire à un tournoi"""
    tournament = db.query(Tournament).filter(Tournament.id == tournament_id).first()
    if not tournament:
        raise HTTPException(status_code=404, detail="Tournoi non trouvé")
    
    if not tournament.is_active:
        raise HTTPException(status_code=400, detail="Tournoi non actif")
    
    if tournament.is_started:
        raise HTTPException(status_code=400, detail="Tournoi déjà commencé")
    
    if current_user.registration_status != RegistrationStatus.APPROVED:
        raise HTTPException(status_code=400, detail="Votre inscription n'est pas approuvée")
    
    # Vérifier si déjà inscrit
    existing = db.query(TournamentRegistration).filter(
        TournamentRegistration.user_id == current_user.id,
        TournamentRegistration.tournament_id == tournament_id
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Déjà inscrit à ce tournoi")
    
    # Vérifier les places disponibles
    if tournament.current_participants >= tournament.max_participants:
        raise HTTPException(status_code=400, detail="Tournoi complet")
    
    # Créer l'inscription
    registration = TournamentRegistration(
        user_id=current_user.id,
        tournament_id=tournament_id,
        status=RegistrationStatus.PENDING,
        payment_proof=current_user.payment_proof
    )
    db.add(registration)
    
    # Mettre à jour le nombre de participants
    tournament.current_participants += 1
    
    db.commit()
    db.refresh(registration)
    
    return {"message": "Inscription réussie", "registration": registration.id}


def generate_brackets(tournament_id: int, db: Session):
    """Générer automatiquement les brackets pour un tournoi"""
    # Obtenir tous les participants approuvés
    registrations = db.query(TournamentRegistration).filter(
        TournamentRegistration.tournament_id == tournament_id,
        TournamentRegistration.status == RegistrationStatus.APPROVED
    ).all()
    
    if len(registrations) < 2:
        raise HTTPException(status_code=400, detail="Pas assez de participants")
    
    # Trier les participants par date d'inscription
    participants = [reg.user for reg in registrations]
    
    # Calculer le nombre de rounds nécessaires
    num_participants = len(participants)
    next_power_of_2 = 2 ** math.ceil(math.log2(num_participants))
    
    # Supprimer les anciens brackets et matchs
    db.query(Bracket).filter(Bracket.tournament_id == tournament_id).delete()
    db.query(Match).filter(Match.tournament_id == tournament_id).delete()
    
    # Créer les matchs du premier round
    round_number = 1
    round_type = RoundType.ROUND_OF_32  # À ajuster selon le nombre de participants
    
    if next_power_of_2 <= 4:
        round_type = RoundType.ROUND_OF_16
    elif next_power_of_2 <= 8:
        round_type = RoundType.QUARTERFINAL
    elif next_power_of_2 <= 16:
        round_type = RoundType.ROUND_OF_16
    else:
        round_type = RoundType.ROUND_OF_32
    
    matches = []
    match_number = 1
    
    # Créer les matchs pour les participants pairs
    for i in range(0, len(participants) - 1, 2):
        match = Match(
            tournament_id=tournament_id,
            round_type=round_type,
            round_number=round_number,
            match_number=match_number,
            player1_id=participants[i].id,
            player2_id=participants[i + 1].id if i + 1 < len(participants) else None,
            status=MatchStatus.PENDING
        )
        db.add(match)
        matches.append(match)
        match_number += 1
    
    # Si nombre impair, le dernier participant passe directement au round suivant
    if len(participants) % 2 == 1:
        # Créer un match avec un joueur automatique
        pass
    
    db.commit()
    
    # Générer les brackets pour l'affichage
    for i, match in enumerate(matches):
        if match.player1_id:
            bracket1 = Bracket(
                tournament_id=tournament_id,
                round_type=round_type,
                round_number=round_number,
                position=i * 2,
                user_id=match.player1_id,
                match_id=match.id
            )
            db.add(bracket1)
        
        if match.player2_id:
            bracket2 = Bracket(
                tournament_id=tournament_id,
                round_type=round_type,
                round_number=round_number,
                position=i * 2 + 1,
                user_id=match.player2_id,
                match_id=match.id
            )
            db.add(bracket2)
    
    db.commit()
    
    return {"message": "Brackets générés avec succès"}


@router.post("/{tournament_id}/start")
async def start_tournament(
    tournament_id: int,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Démarrer un tournoi et générer les brackets"""
    tournament = db.query(Tournament).filter(Tournament.id == tournament_id).first()
    if not tournament:
        raise HTTPException(status_code=404, detail="Tournoi non trouvé")
    
    if tournament.is_started:
        raise HTTPException(status_code=400, detail="Tournoi déjà commencé")
    
    # Générer les brackets
    generate_brackets(tournament_id, db)
    
    # Marquer le tournoi comme commencé
    tournament.is_started = True
    tournament.start_date = datetime.utcnow()
    db.commit()
    
    return {"message": "Tournoi démarré avec succès"}


@router.get("/{tournament_id}/brackets", response_model=List[BracketResponse])
async def get_tournament_brackets(
    tournament_id: int,
    db: Session = Depends(get_db)
):
    """Obtenir les brackets d'un tournoi"""
    brackets = db.query(Bracket).filter(
        Bracket.tournament_id == tournament_id
    ).order_by(Bracket.round_number, Bracket.position).all()
    return brackets


@router.get("/{tournament_id}/matches", response_model=List[MatchResponse])
async def get_tournament_matches(
    tournament_id: int,
    db: Session = Depends(get_db)
):
    """Obtenir tous les matchs d'un tournoi"""
    matches = db.query(Match).filter(
        Match.tournament_id == tournament_id
    ).order_by(Match.round_number, Match.match_number).all()
    return matches

