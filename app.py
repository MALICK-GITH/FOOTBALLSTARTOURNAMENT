from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, send_from_directory
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, timedelta
import os
import uuid
import json
from functools import wraps

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production-2026')

# Configuration base de données
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///efootkings.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB max file size
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=30)  # Session persistante 30 jours

# Vercel utilise un système de fichiers read-only, utiliser /tmp pour les fichiers
IS_VERCEL = os.environ.get('VERCEL', '0') == '1'
if IS_VERCEL:
    BASE_DIR = '/tmp'
    app.config['UPLOAD_FOLDER'] = '/tmp/uploads'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/efootkings.db'
else:
    BASE_DIR = '.'
    app.config['UPLOAD_FOLDER'] = 'uploads'

# Initialiser extensions
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'user_login'
login_manager.login_message = 'Veuillez vous connecter pour accéder à cette page.'
login_manager.login_message_category = 'info'

# Créer les dossiers nécessaires
def ensure_dirs():
    try:
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    except (OSError, PermissionError) as e:
        print(f"Warning: Could not create directories: {e}")

ensure_dirs()

# ==================== MODÈLES DE BASE DE DONNÉES ====================

class User(UserMixin, db.Model):
    """Modèle utilisateur avec connexion persistante"""
    __tablename__ = 'users'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    pseudo = db.Column(db.String(100), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(200))
    contact = db.Column(db.String(200))
    profile_picture = db.Column(db.String(255))
    payment_screenshot = db.Column(db.String(255))
    status = db.Column(db.String(20), default='pending')  # pending, validated, rejected
    is_online = db.Column(db.Boolean, default=False)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    registered_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relations
    badges = db.relationship('Badge', backref='user', lazy=True, cascade='all, delete-orphan')
    messages_received = db.relationship('Message', foreign_keys='Message.user_id', backref='recipient', lazy=True)
    match_history = db.relationship('MatchHistory', backref='user', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'pseudo': self.pseudo,
            'full_name': self.full_name,
            'contact': self.contact,
            'profile_picture': self.profile_picture,
            'status': self.status,
            'is_online': self.is_online,
            'last_seen': self.last_seen.isoformat() if self.last_seen else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'badges': [b.to_dict() for b in self.badges]
        }

class Badge(db.Model):
    """Badges et trophées des joueurs"""
    __tablename__ = 'badges'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    badge_type = db.Column(db.String(50), nullable=False)  # winner, finalist, semifinalist, champion
    tournament_date = db.Column(db.Date, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'type': self.badge_type,
            'tournament_date': self.tournament_date.isoformat() if self.tournament_date else None
        }

class Message(db.Model):
    """Messages de l'administrateur aux utilisateurs"""
    __tablename__ = 'messages'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=True)  # None = message global
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'is_read': self.is_read,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'is_global': self.user_id is None
        }

class MatchHistory(db.Model):
    """Historique des matchs pour chaque utilisateur"""
    __tablename__ = 'match_history'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    round_type = db.Column(db.String(50), nullable=False)  # quarterfinal, semifinal, final
    opponent = db.Column(db.String(100), nullable=False)
    user_score = db.Column(db.Integer, default=0)
    opponent_score = db.Column(db.Integer, default=0)
    result = db.Column(db.String(20))  # win, loss
    match_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'round_type': self.round_type,
            'opponent': self.opponent,
            'user_score': self.user_score,
            'opponent_score': self.opponent_score,
            'result': self.result,
            'match_date': self.match_date.isoformat() if self.match_date else None
        }

class Bracket(db.Model):
    """Bracket du tournoi"""
    __tablename__ = 'bracket'
    
    id = db.Column(db.Integer, primary_key=True)
    quarterfinals = db.Column(db.Text)  # JSON string
    semifinals = db.Column(db.Text)  # JSON string
    final = db.Column(db.Text)  # JSON string
    winner = db.Column(db.String(100))
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def get_quarterfinals(self):
        return json.loads(self.quarterfinals) if self.quarterfinals else []
    
    def set_quarterfinals(self, data):
        self.quarterfinals = json.dumps(data) if data else None
    
    def get_semifinals(self):
        return json.loads(self.semifinals) if self.semifinals else []
    
    def set_semifinals(self, data):
        self.semifinals = json.dumps(data) if data else None
    
    def get_final(self):
        return json.loads(self.final) if self.final else None
    
    def set_final(self, data):
        self.final = json.dumps(data) if data else None
    
    def to_dict(self):
        return {
            'quarterfinals': self.get_quarterfinals(),
            'semifinals': self.get_semifinals(),
            'final': self.get_final(),
            'winner': self.winner,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class AdminUser(db.Model):
    """Compte administrateur"""
    __tablename__ = 'admin_users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# ==================== FONCTIONS UTILITAIRES ====================

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def save_uploaded_file(file, folder=''):
    """Sauvegarde un fichier uploadé"""
    if file and file.filename and allowed_file(file.filename):
        try:
            ensure_dirs()
            filename = secure_filename(file.filename)
            unique_filename = f"{uuid.uuid4()}_{filename}"
            if folder:
                folder_path = os.path.join(app.config['UPLOAD_FOLDER'], folder)
                os.makedirs(folder_path, exist_ok=True)
                filepath = os.path.join(folder_path, unique_filename)
            else:
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            
            file.save(filepath)
            # Retourner le chemin relatif avec le dossier si nécessaire
            if folder:
                return f"{folder}/{unique_filename}"
            return unique_filename
        except Exception as e:
            print(f"Error saving file: {e}")
            return None
    return None

def get_bracket_data():
    """Récupère ou crée le bracket"""
    bracket = Bracket.query.first()
    if not bracket:
        bracket = Bracket()
        db.session.add(bracket)
        db.session.commit()
    return bracket

def admin_required(f):
    """Décorateur pour les routes admin"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            flash('Accès refusé. Veuillez vous connecter en tant qu\'administrateur.', 'error')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

def get_max_players():
    return 8

# ==================== FLASK-LOGIN LOADER ====================

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# ==================== ROUTES PUBLIQUES ====================

@app.route('/')
def index():
    validated_count = User.query.filter_by(status='validated').count()
    max_players = get_max_players()
    is_full = validated_count >= max_players
    
    # Mettre à jour le statut en ligne des utilisateurs connectés
    if current_user.is_authenticated:
        current_user.is_online = True
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    
    return render_template('index.html', 
                         registered_count=validated_count, 
                         max_players=max_players,
                         is_full=is_full)

@app.route('/register', methods=['GET', 'POST'])
def register():
    validated_count = User.query.filter_by(status='validated').count()
    max_players = get_max_players()
    
    if validated_count >= max_players:
        flash('Le tournoi est complet ! Les inscriptions sont fermées.', 'warning')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        pseudo = request.form.get('pseudo', '').strip()
        full_name = request.form.get('full_name', '').strip()
        contact = request.form.get('contact', '').strip()
        password = request.form.get('password', '').strip()
        
        if not pseudo:
            flash('Le pseudo eFootball est obligatoire !', 'error')
            return render_template('register.html')
        
        if not password:
            flash('Un mot de passe est obligatoire !', 'error')
            return render_template('register.html')
        
        # Vérifier si le pseudo existe déjà
        existing_user = User.query.filter_by(pseudo=pseudo).first()
        if existing_user:
            flash('Ce pseudo est déjà inscrit !', 'error')
            return render_template('register.html')
        
        # Gérer les uploads
        profile_picture = save_uploaded_file(request.files.get('profile_picture'), 'profiles')
        payment_screenshot = save_uploaded_file(request.files.get('screenshot'), 'payments')
        
        if not payment_screenshot:
            flash('Le screenshot du paiement est obligatoire !', 'error')
            return render_template('register.html')
        
        # Créer l'utilisateur
        new_user = User(
            pseudo=pseudo,
            full_name=full_name or None,
            contact=contact or None,
            profile_picture=profile_picture,
            payment_screenshot=payment_screenshot,
            status='pending'
        )
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Inscription enregistrée ! Votre paiement sera validé par l\'administrateur.', 'success')
        return redirect(url_for('index'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def user_login():
    if current_user.is_authenticated:
        return redirect(url_for('user_dashboard'))
    
    if request.method == 'POST':
        pseudo = request.form.get('pseudo', '').strip()
        password = request.form.get('password', '')
        
        user = User.query.filter_by(pseudo=pseudo).first()
        
        if user and user.check_password(password):
            login_user(user, remember=True)  # Connexion persistante
            session.permanent = True
            user.is_online = True
            user.last_seen = datetime.utcnow()
            db.session.commit()
            flash('Connexion réussie !', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('user_dashboard'))
        else:
            flash('Pseudo ou mot de passe incorrect !', 'error')
    
    return render_template('user_login.html')

@app.route('/logout')
@login_required
def user_logout():
    if current_user.is_authenticated:
        current_user.is_online = False
        db.session.commit()
    logout_user()
    flash('Déconnexion réussie !', 'success')
    return redirect(url_for('index'))

@app.route('/bracket')
def bracket():
    bracket_data = get_bracket_data()
    validated_players = User.query.filter_by(status='validated').all()
    
    # Si on a 8 joueurs validés, générer le bracket automatiquement
    if len(validated_players) == 8 and not bracket_data.get_quarterfinals():
        quarterfinals = []
        for i in range(0, 8, 2):
            quarterfinals.append({
                'player1': validated_players[i].pseudo,
                'player2': validated_players[i+1].pseudo,
                'score1': 0,
                'score2': 0,
                'winner': None
            })
        bracket_data.set_quarterfinals(quarterfinals)
        db.session.commit()
    
    return render_template('bracket.html', 
                         bracket=bracket_data.to_dict(), 
                         players=[p.pseudo for p in validated_players])

# ==================== ROUTES UTILISATEUR ====================

@app.route('/dashboard')
@login_required
def user_dashboard():
    user = current_user
    user.is_online = True
    user.last_seen = datetime.utcnow()
    db.session.commit()
    
    # Récupérer les messages non lus
    unread_messages = Message.query.filter(
        ((Message.user_id == user.id) | (Message.user_id.is_(None))) & 
        (Message.is_read == False)
    ).order_by(Message.created_at.desc()).all()
    
    # Récupérer l'historique des matchs
    match_history = MatchHistory.query.filter_by(user_id=user.id).order_by(MatchHistory.match_date.desc()).all()
    
    # Récupérer le bracket pour voir la position
    bracket_data = get_bracket_data().to_dict()
    
    return render_template('user_dashboard.html',
                         user=user,
                         unread_messages=unread_messages,
                         match_history=match_history,
                         bracket=bracket_data)

@app.route('/api/messages/read/<int:message_id>', methods=['POST'])
@login_required
def mark_message_read(message_id):
    message = Message.query.get_or_404(message_id)
    if message.user_id == current_user.id or message.user_id is None:
        message.is_read = True
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'error': 'Unauthorized'}), 403

@app.route('/api/messages/unread-count')
@login_required
def unread_messages_count():
    count = Message.query.filter(
        ((Message.user_id == current_user.id) | (Message.user_id.is_(None))) & 
        (Message.is_read == False)
    ).count()
    return jsonify({'count': count})

# ==================== ROUTES ADMIN ====================

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if session.get('admin_logged_in'):
        return redirect(url_for('admin_dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        admin = AdminUser.query.filter_by(username=username).first()
        
        if not admin:
            # Créer l'admin par défaut si aucun n'existe
            admin = AdminUser(username='admin')
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
        
        if admin.check_password(password):
            session['admin_logged_in'] = True
            session.permanent = True
            flash('Connexion réussie !', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Identifiants incorrects !', 'error')
    
    return render_template('admin_login.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    flash('Déconnexion réussie !', 'success')
    return redirect(url_for('admin_login'))

@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    users = User.query.order_by(User.created_at.desc()).all()
    validated_players = User.query.filter_by(status='validated').all()
    pending_count = User.query.filter_by(status='pending').count()
    bracket_data = get_bracket_data()
    
    return render_template('admin_dashboard.html', 
                         users=users, 
                         bracket=bracket_data.to_dict(),
                         validated_players=validated_players,
                         pending_count=pending_count)

@app.route('/admin/users')
@admin_required
def admin_users():
    users = User.query.order_by(User.created_at.desc()).all()
    return jsonify({'users': [u.to_dict() for u in users]})

@app.route('/admin/validate/<user_id>', methods=['POST'])
@admin_required
def validate_user(user_id):
    user = User.query.get_or_404(user_id)
    action = request.json.get('action')  # 'validate' or 'reject'
    
    if action == 'validate':
        validated_count = User.query.filter_by(status='validated').count()
        if validated_count >= get_max_players():
            return jsonify({'error': 'Le tournoi est complet (8 joueurs)'}), 400
        
        user.status = 'validated'
        flash(f'Joueur {user.pseudo} validé !', 'success')
        
        # Si on atteint 8 joueurs validés, générer le bracket
        validated_players = User.query.filter_by(status='validated').all()
        if len(validated_players) == 8:
            bracket_data = get_bracket_data()
            if not bracket_data.get_quarterfinals():
                quarterfinals = []
                for i in range(0, 8, 2):
                    quarterfinals.append({
                        'player1': validated_players[i].pseudo,
                        'player2': validated_players[i+1].pseudo,
                        'score1': 0,
                        'score2': 0,
                        'winner': None
                    })
                bracket_data.set_quarterfinals(quarterfinals)
    elif action == 'reject':
        user.status = 'rejected'
        flash(f'Joueur {user.pseudo} refusé.', 'info')
    
    db.session.commit()
    return jsonify({'success': True, 'status': user.status})

@app.route('/admin/delete-user/<user_id>', methods=['POST'])
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash(f'Utilisateur {user.pseudo} supprimé.', 'info')
    return jsonify({'success': True})

@app.route('/admin/update-bracket', methods=['POST'])
@admin_required
def update_bracket():
    bracket_data = get_bracket_data()
    data = request.json
    
    # Mettre à jour les quarts de finale
    if 'quarterfinals' in data:
        quarterfinals = data['quarterfinals']
        for i, match_data in enumerate(quarterfinals):
            if i < len(bracket_data.get_quarterfinals()):
                existing = bracket_data.get_quarterfinals()[i]
                existing['score1'] = match_data.get('score1', 0)
                existing['score2'] = match_data.get('score2', 0)
                
                # Déterminer le gagnant
                if existing['score1'] > existing['score2']:
                    existing['winner'] = existing['player1']
                elif existing['score2'] > existing['score1']:
                    existing['winner'] = existing['player2']
                else:
                    existing['winner'] = None
        
        bracket_data.set_quarterfinals(quarterfinals)
        
        # Générer les demi-finales si tous les quarts sont terminés
        winners = [m['winner'] for m in quarterfinals if m.get('winner')]
        if len(winners) == 4 and not bracket_data.get_semifinals():
            semifinals = [
                {'player1': winners[0], 'player2': winners[1], 'score1': 0, 'score2': 0, 'winner': None},
                {'player1': winners[2], 'player2': winners[3], 'score1': 0, 'score2': 0, 'winner': None}
            ]
            bracket_data.set_semifinals(semifinals)
            
            # Créer l'historique des matchs pour les quarts de finale
            for match in quarterfinals:
                if match.get('winner'):
                    # Trouver les utilisateurs
                    user1 = User.query.filter_by(pseudo=match['player1']).first()
                    user2 = User.query.filter_by(pseudo=match['player2']).first()
                    
                    if user1:
                        history1 = MatchHistory(
                            user_id=user1.id,
                            round_type='quarterfinal',
                            opponent=match['player2'],
                            user_score=match['score1'],
                            opponent_score=match['score2'],
                            result='win' if match['winner'] == match['player1'] else 'loss'
                        )
                        db.session.add(history1)
                    
                    if user2:
                        history2 = MatchHistory(
                            user_id=user2.id,
                            round_type='quarterfinal',
                            opponent=match['player1'],
                            user_score=match['score2'],
                            opponent_score=match['score1'],
                            result='win' if match['winner'] == match['player2'] else 'loss'
                        )
                        db.session.add(history2)
    
    # Mettre à jour les demi-finales
    if 'semifinals' in data:
        semifinals = data['semifinals']
        for i, match_data in enumerate(semifinals):
            if i < len(bracket_data.get_semifinals()):
                existing = bracket_data.get_semifinals()[i]
                existing['score1'] = match_data.get('score1', 0)
                existing['score2'] = match_data.get('score2', 0)
                
                if existing['score1'] > existing['score2']:
                    existing['winner'] = existing['player1']
                elif existing['score2'] > existing['score1']:
                    existing['winner'] = existing['player2']
                else:
                    existing['winner'] = None
        
        bracket_data.set_semifinals(semifinals)
        
        # Générer la finale si les deux demi-finales sont terminées
        winners = [m['winner'] for m in semifinals if m.get('winner')]
        if len(winners) == 2 and not bracket_data.get_final():
            final = {
                'player1': winners[0],
                'player2': winners[1],
                'score1': 0,
                'score2': 0,
                'winner': None
            }
            bracket_data.set_final(final)
            
            # Attribuer badge demi-finaliste aux perdants
            for match in semifinals:
                if match.get('winner'):
                    loser = match['player1'] if match['winner'] == match['player2'] else match['player2']
                    user = User.query.filter_by(pseudo=loser).first()
                    if user:
                        # Vérifier si le badge n'existe pas déjà
                        existing_badge = Badge.query.filter_by(
                            user_id=user.id,
                            badge_type='semifinalist'
                        ).first()
                        if not existing_badge:
                            badge = Badge(user_id=user.id, badge_type='semifinalist')
                            db.session.add(badge)
            
            # Créer l'historique des matchs pour les demi-finales
            for match in semifinals:
                if match.get('winner'):
                    user1 = User.query.filter_by(pseudo=match['player1']).first()
                    user2 = User.query.filter_by(pseudo=match['player2']).first()
                    
                    if user1:
                        history1 = MatchHistory(
                            user_id=user1.id,
                            round_type='semifinal',
                            opponent=match['player2'],
                            user_score=match['score1'],
                            opponent_score=match['score2'],
                            result='win' if match['winner'] == match['player1'] else 'loss'
                        )
                        db.session.add(history1)
                    
                    if user2:
                        history2 = MatchHistory(
                            user_id=user2.id,
                            round_type='semifinal',
                            opponent=match['player1'],
                            user_score=match['score2'],
                            opponent_score=match['score1'],
                            result='win' if match['winner'] == match['player2'] else 'loss'
                        )
                        db.session.add(history2)
    
    # Mettre à jour la finale
    if 'final' in data:
        final = data['final']
        existing_final = bracket_data.get_final()
        if existing_final:
            existing_final['score1'] = final.get('score1', 0)
            existing_final['score2'] = final.get('score2', 0)
            
            if existing_final['score1'] > existing_final['score2']:
                existing_final['winner'] = existing_final['player1']
                bracket_data.winner = existing_final['player1']
            elif existing_final['score2'] > existing_final['score1']:
                existing_final['winner'] = existing_final['player2']
                bracket_data.winner = existing_final['player2']
            else:
                existing_final['winner'] = None
                bracket_data.winner = None
            
            bracket_data.set_final(existing_final)
            
            # Attribuer badges
            if existing_final.get('winner'):
                winner_user = User.query.filter_by(pseudo=existing_final['winner']).first()
                loser_user = User.query.filter_by(
                    pseudo=existing_final['player1'] if existing_final['winner'] == existing_final['player2'] 
                    else existing_final['player2']
                ).first()
                
                # Badge champion pour le vainqueur
                if winner_user:
                    existing_badge = Badge.query.filter_by(
                        user_id=winner_user.id,
                        badge_type='champion'
                    ).first()
                    if not existing_badge:
                        badge = Badge(user_id=winner_user.id, badge_type='champion')
                        db.session.add(badge)
                
                # Badge finaliste pour le perdant
                if loser_user:
                    existing_badge = Badge.query.filter_by(
                        user_id=loser_user.id,
                        badge_type='finalist'
                    ).first()
                    if not existing_badge:
                        badge = Badge(user_id=loser_user.id, badge_type='finalist')
                        db.session.add(badge)
                
                # Créer l'historique de la finale
                if winner_user:
                    history1 = MatchHistory(
                        user_id=winner_user.id,
                        round_type='final',
                        opponent=existing_final['player1'] if existing_final['winner'] == existing_final['player2'] else existing_final['player2'],
                        user_score=existing_final['score1'] if existing_final['winner'] == existing_final['player1'] else existing_final['score2'],
                        opponent_score=existing_final['score2'] if existing_final['winner'] == existing_final['player1'] else existing_final['score1'],
                        result='win'
                    )
                    db.session.add(history1)
                
                if loser_user:
                    history2 = MatchHistory(
                        user_id=loser_user.id,
                        round_type='final',
                        opponent=existing_final['winner'],
                        user_score=existing_final['score2'] if existing_final['winner'] == existing_final['player1'] else existing_final['score1'],
                        opponent_score=existing_final['score1'] if existing_final['winner'] == existing_final['player1'] else existing_final['score2'],
                        result='loss'
                    )
                    db.session.add(history2)
    
    db.session.commit()
    return jsonify({'success': True, 'bracket': bracket_data.to_dict()})

@app.route('/admin/messages', methods=['GET', 'POST'])
@admin_required
def admin_messages():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        target = request.form.get('target', 'all')  # 'all' or user_id
        
        if not title or not content:
            flash('Le titre et le contenu sont obligatoires !', 'error')
            return redirect(url_for('admin_messages'))
        
        if target == 'all':
            # Message global
            message = Message(user_id=None, title=title, content=content)
            db.session.add(message)
        else:
            # Message ciblé
            message = Message(user_id=target, title=title, content=content)
            db.session.add(message)
        
        db.session.commit()
        flash('Message envoyé avec succès !', 'success')
        return redirect(url_for('admin_messages'))
    
    # GET: Afficher le formulaire et l'historique
    users = User.query.all()
    messages = Message.query.order_by(Message.created_at.desc()).limit(50).all()
    return render_template('admin_messages.html', users=users, messages=messages)

@app.route('/api/bracket/updates')
def bracket_updates():
    """Endpoint pour les mises à jour en temps réel du bracket"""
    bracket_data = get_bracket_data()
    return jsonify(bracket_data.to_dict())

# ==================== ROUTES FICHIERS ====================

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    try:
        # Gérer les fichiers dans des sous-dossiers (profiles/, payments/)
        if '/' in filename:
            folder, file = filename.split('/', 1)
            folder_path = os.path.join(app.config['UPLOAD_FOLDER'], folder)
            return send_from_directory(folder_path, file)
        else:
            return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    except Exception as e:
        print(f"Error serving file: {e}")
        return "File not found", 404

# ==================== INITIALISATION ====================

# Initialiser la base de données et créer l'admin par défaut
with app.app_context():
    db.create_all()
    if not AdminUser.query.first():
        admin = AdminUser(username='admin')
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print("Admin créé: username='admin', password='admin123'")

if __name__ == '__main__':
    app.run(debug=True)
