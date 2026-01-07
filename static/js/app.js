// Configuration
const API_BASE_URL = '/api';

// Gestion de l'authentification
let currentUser = null;

// Vérifier si l'utilisateur est connecté au chargement
document.addEventListener('DOMContentLoaded', async () => {
    await checkAuth();
    loadMessages();
    if (window.location.pathname === '/' || window.location.pathname === '/index.html') {
        loadTournaments();
    }
});

// Fonctions d'authentification
async function checkAuth() {
    const token = localStorage.getItem('token') || getCookie('session_token');
    if (!token) {
        updateNavForGuest();
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/users/me`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (response.ok) {
            currentUser = await response.json();
            updateNavForUser(currentUser);
        } else {
            clearAuth();
            updateNavForGuest();
        }
    } catch (error) {
        console.error('Erreur de vérification auth:', error);
        clearAuth();
        updateNavForGuest();
    }
}

function updateNavForUser(user) {
    const navLinks = document.querySelector('.nav-links');
    if (!navLinks) return;
    
    navLinks.innerHTML = `
        <li><a href="/">Accueil</a></li>
        <li><a href="/#tournaments">Tournois</a></li>
        ${user.role === 'admin' ? '<li><a href="/admin">Administration</a></li>' : ''}
        <li class="user-menu">
            <span>${user.username}</span>
            <a href="#" onclick="showProfileModal(); return false;">Profil</a>
            <a href="#" onclick="logout(); return false;" class="btn btn-secondary">Déconnexion</a>
        </li>
    `;
}

function updateNavForGuest() {
    const navLinks = document.querySelector('.nav-links');
    if (!navLinks) return;
    
    navLinks.innerHTML = `
        <li><a href="/">Accueil</a></li>
        <li><a href="#" onclick="showLoginModal(); return false;">Connexion</a></li>
        <li><a href="#" onclick="showRegisterModal(); return false;" class="btn btn-primary">Inscription</a></li>
    `;
}

function clearAuth() {
    localStorage.removeItem('token');
    currentUser = null;
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

// Fonctions de connexion/inscription
async function login(email, password, rememberMe) {
    try {
        const response = await fetch(`${API_BASE_URL}/users/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password, remember_me: rememberMe })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            localStorage.setItem('token', data.access_token);
            currentUser = data.user;
            updateNavForUser(currentUser);
            closeModal('loginModal');
            showAlert('Connexion réussie!', 'success');
            window.location.reload();
        } else {
            showAlert(data.detail || 'Erreur de connexion', 'error');
        }
    } catch (error) {
        showAlert('Erreur de connexion', 'error');
    }
}

async function register(userData) {
    try {
        const response = await fetch(`${API_BASE_URL}/users/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(userData)
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showAlert('Inscription réussie! Vous pouvez maintenant vous connecter.', 'success');
            closeModal('registerModal');
            showLoginModal();
        } else {
            showAlert(data.detail || 'Erreur d\'inscription', 'error');
        }
    } catch (error) {
        showAlert('Erreur d\'inscription', 'error');
    }
}

async function logout() {
    try {
        await fetch(`${API_BASE_URL}/users/logout`, {
            method: 'POST'
        });
    } catch (error) {
        console.error('Erreur de déconnexion:', error);
    }
    
    clearAuth();
    updateNavForGuest();
    showAlert('Déconnexion réussie', 'success');
    window.location.href = '/';
}

// Fonctions de modals
function showLoginModal() {
    const modal = document.getElementById('loginModal');
    if (modal) {
        modal.style.display = 'block';
    }
}

function showRegisterModal() {
    const modal = document.getElementById('registerModal');
    if (modal) {
        modal.style.display = 'block';
    }
}


function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = 'none';
    }
}

// Fermer modals en cliquant en dehors
window.onclick = function(event) {
    const modals = document.querySelectorAll('.modal');
    modals.forEach(modal => {
        if (event.target == modal) {
            modal.style.display = 'none';
        }
    });
}

// Handlers de formulaires
function handleLogin(event) {
    event.preventDefault();
    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;
    const rememberMe = document.getElementById('rememberMe').checked;
    login(email, password, rememberMe);
}

function handleRegister(event) {
    event.preventDefault();
    const userData = {
        email: document.getElementById('registerEmail').value,
        username: document.getElementById('registerUsername').value,
        full_name: document.getElementById('registerFullName').value,
        phone: document.getElementById('registerPhone').value,
        password: document.getElementById('registerPassword').value
    };
    register(userData);
}

// Charger les tournois
async function loadTournaments() {
    try {
        const response = await fetch(`${API_BASE_URL}/tournaments/`);
        const tournaments = await response.json();
        
        const container = document.getElementById('tournamentsContainer');
        if (!container) return;
        
        if (tournaments.length === 0) {
            container.innerHTML = '<p>Aucun tournoi disponible pour le moment.</p>';
            return;
        }
        
        container.innerHTML = tournaments.map(tournament => `
            <div class="tournament-card">
                <h3 class="tournament-title">${tournament.name}</h3>
                <p class="tournament-info">${tournament.description || ''}</p>
                <p class="tournament-info">Frais d'inscription: ${tournament.registration_fee}€</p>
                <p class="tournament-info">Participants: ${tournament.current_participants}/${tournament.max_participants}</p>
                ${currentUser && currentUser.registration_status === 'approved' ? 
                    `<button class="btn btn-primary" onclick="registerToTournament(${tournament.id})">S'inscrire</button>` : 
                    '<p class="tournament-info">Votre inscription doit être approuvée pour participer</p>'
                }
                ${tournament.is_started ? 
                    `<a href="/brackets/${tournament.id}" class="btn btn-secondary">Voir les brackets</a>` : 
                    ''
                }
            </div>
        `).join('');
    } catch (error) {
        console.error('Erreur de chargement des tournois:', error);
    }
}

async function registerToTournament(tournamentId) {
    if (!currentUser) {
        showLoginModal();
        return;
    }
    
    try {
        const token = localStorage.getItem('token');
        const response = await fetch(`${API_BASE_URL}/tournaments/${tournamentId}/register`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showAlert('Inscription au tournoi réussie!', 'success');
            loadTournaments();
        } else {
            showAlert(data.detail || 'Erreur d\'inscription', 'error');
        }
    } catch (error) {
        showAlert('Erreur d\'inscription', 'error');
    }
}

// Charger les messages
async function loadMessages() {
    try {
        const response = await fetch(`${API_BASE_URL}/messages/`);
        const messages = await response.json();
        
        const container = document.getElementById('messagesContainer');
        if (!container) return;
        
        if (messages.length === 0) return;
        
        container.innerHTML = messages.map(msg => `
            <div class="message-card ${msg.is_important ? 'important' : ''}">
                <div class="message-title">${msg.title}</div>
                <div class="message-content">${msg.content}</div>
                <div class="message-date">${new Date(msg.created_at).toLocaleDateString('fr-FR')}</div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Erreur de chargement des messages:', error);
    }
}

// Alertes
function showAlert(message, type = 'success') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.textContent = message;
    
    const container = document.querySelector('.container') || document.body;
    container.insertBefore(alertDiv, container.firstChild);
    
    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}

// Mettre à jour le profil
async function updateProfile(event) {
    event.preventDefault();
    
    if (!currentUser) return;
    
    const userData = {
        username: document.getElementById('profileUsername').value,
        full_name: document.getElementById('profileFullName').value,
        phone: document.getElementById('profilePhone').value
    };
    
    try {
        const token = localStorage.getItem('token');
        const response = await fetch(`${API_BASE_URL}/users/me`, {
            method: 'PUT',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(userData)
        });
        
        if (response.ok) {
            currentUser = await response.json();
            showAlert('Profil mis à jour avec succès!', 'success');
            closeModal('profileModal');
        } else {
            const data = await response.json();
            showAlert(data.detail || 'Erreur de mise à jour', 'error');
        }
    } catch (error) {
        showAlert('Erreur de mise à jour', 'error');
    }
}

// Charger le statut du profil dans le modal
function showProfileModal() {
    if (!currentUser) return;
    
    const modal = document.getElementById('profileModal');
    if (modal) {
        document.getElementById('profileUsername').value = currentUser.username;
        document.getElementById('profileFullName').value = currentUser.full_name;
        document.getElementById('profilePhone').value = currentUser.phone || '';
        
        const statusDiv = document.getElementById('profileStatus');
        let statusClass = 'status-pending';
        if (currentUser.registration_status === 'approved') statusClass = 'status-approved';
        if (currentUser.registration_status === 'rejected') statusClass = 'status-rejected';
        statusDiv.innerHTML = `<span class="status-badge ${statusClass}">${currentUser.registration_status}</span>`;
        
        const img = document.getElementById('currentProfilePicture');
        if (currentUser.profile_picture) {
            img.src = `/static/uploads/${currentUser.profile_picture}`;
        } else {
            img.src = '/static/default-avatar.png';
        }
        
        modal.style.display = 'block';
    }
}

// Upload de fichiers
async function uploadProfilePicture(file) {
    if (!file) return;
    
    const formData = new FormData();
    formData.append('file', file);
    
    try {
        const token = localStorage.getItem('token');
        const response = await fetch(`${API_BASE_URL}/users/upload-profile-picture`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`
            },
            body: formData
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showAlert('Photo de profil uploadée avec succès!', 'success');
            if (currentUser) {
                currentUser.profile_picture = data.filename;
            }
            window.location.reload();
        } else {
            showAlert(data.detail || 'Erreur d\'upload', 'error');
        }
    } catch (error) {
        showAlert('Erreur d\'upload', 'error');
    }
}

async function uploadPaymentProof(file) {
    if (!file) return;
    
    const formData = new FormData();
    formData.append('file', file);
    
    try {
        const token = localStorage.getItem('token');
        const response = await fetch(`${API_BASE_URL}/users/upload-payment-proof`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`
            },
            body: formData
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showAlert('Preuve de paiement uploadée avec succès!', 'success');
        } else {
            showAlert(data.detail || 'Erreur d\'upload', 'error');
        }
    } catch (error) {
        showAlert('Erreur d\'upload', 'error');
    }
}

