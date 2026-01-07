from pydantic import BaseModel, EmailStr, validator
from typing import Optional, List
from datetime import datetime
from models import UserRole, RegistrationStatus, MatchStatus, RoundType


# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: str
    phone: Optional[str] = None


class UserCreate(UserBase):
    password: str
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Le mot de passe doit contenir au moins 8 caractères')
        return v


class UserLogin(BaseModel):
    email: EmailStr
    password: str
    remember_me: bool = False


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    username: Optional[str] = None


class UserResponse(UserBase):
    id: int
    role: UserRole
    is_active: bool
    is_verified: bool
    registration_status: RegistrationStatus
    profile_picture: Optional[str] = None
    payment_proof: Optional[str] = None
    created_at: datetime
    last_login: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class UserAdminResponse(UserResponse):
    pass


# Tournament Schemas
class TournamentBase(BaseModel):
    name: str
    description: Optional[str] = None
    registration_fee: float
    max_participants: int


class TournamentCreate(TournamentBase):
    pass


class TournamentResponse(TournamentBase):
    id: int
    current_participants: int
    is_active: bool
    is_started: bool
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


# Registration Schemas
class RegistrationResponse(BaseModel):
    id: int
    user_id: int
    tournament_id: int
    status: RegistrationStatus
    payment_proof: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime
    user: UserResponse
    
    class Config:
        from_attributes = True


# Match Schemas
class MatchBase(BaseModel):
    player1_score: Optional[int] = None
    player2_score: Optional[int] = None
    notes: Optional[str] = None


class MatchResponse(BaseModel):
    id: int
    tournament_id: int
    round_type: RoundType
    round_number: int
    match_number: int
    player1_id: Optional[int] = None
    player2_id: Optional[int] = None
    player1_score: Optional[int] = None
    player2_score: Optional[int] = None
    winner_id: Optional[int] = None
    status: MatchStatus
    player1: Optional[UserResponse] = None
    player2: Optional[UserResponse] = None
    
    class Config:
        from_attributes = True


# Bracket Schemas
class BracketResponse(BaseModel):
    id: int
    tournament_id: int
    round_type: RoundType
    round_number: int
    position: int
    user_id: Optional[int] = None
    match_id: Optional[int] = None
    user: Optional[UserResponse] = None
    
    class Config:
        from_attributes = True


# Message Schemas
class AdminMessageCreate(BaseModel):
    title: str
    content: str
    is_important: bool = False


class AdminMessageResponse(BaseModel):
    id: int
    title: str
    content: str
    is_important: bool
    is_active: bool
    created_at: datetime
    created_by: int
    
    class Config:
        from_attributes = True


# Token Schema
class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

