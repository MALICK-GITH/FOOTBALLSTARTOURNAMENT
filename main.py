from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os

from database import engine, Base
from config import settings
from routes import users, admin, tournaments, messages, matches
from auth import get_password_hash
from models import User, UserRole

# Créer les tables au démarrage
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    Base.metadata.create_all(bind=engine)
    
    # Créer l'admin par défaut s'il n'existe pas
    from database import SessionLocal
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
    finally:
        db.close()
    
    yield
    
    # Shutdown
    pass

app = FastAPI(
    title="eFootball Mobile 2026 Tournament Platform",
    description="Plateforme professionnelle de tournois eFootball Mobile",
    version="1.0.0",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Router les routes API
app.include_router(users.router)
app.include_router(admin.router)
app.include_router(tournaments.router)
app.include_router(messages.router)
app.include_router(matches.router)

# Servir les fichiers statiques
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Page d'accueil"""
    if os.path.exists("templates/index.html"):
        with open("templates/index.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse(content="<h1>eFootball Tournament Platform</h1><p>Frontend en cours de chargement...</p>")


@app.get("/admin", response_class=HTMLResponse)
async def admin_page():
    """Page admin"""
    if os.path.exists("templates/admin.html"):
        with open("templates/admin.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse(content="<h1>Administration</h1><p>Interface admin en cours de chargement...</p>")


@app.get("/brackets/{tournament_id}", response_class=HTMLResponse)
async def brackets_page(tournament_id: int):
    """Page brackets"""
    if os.path.exists("templates/brackets.html"):
        with open("templates/brackets.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse(content=f"<h1>Brackets - Tournoi {tournament_id}</h1>")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

