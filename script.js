// Script commun pour toutes les pages

// Initialisation du localStorage avec données par défaut
function initStorage() {
    if (!localStorage.getItem('users')) {
        localStorage.setItem('users', JSON.stringify([]));
    }
    if (!localStorage.getItem('admin')) {
        // Admin par défaut : pseudo: "admin", password: "admin123"
        localStorage.setItem('admin', JSON.stringify({
            pseudo: 'admin',
            password: 'admin123'
        }));
    }
    if (!localStorage.getItem('currentUser')) {
        localStorage.setItem('currentUser', JSON.stringify(null));
    }
}

// Initialisation au chargement
document.addEventListener('DOMContentLoaded', function() {
    initStorage();
    initNavigation();
    updateNavigation();
});

// Navigation mobile
function initNavigation() {
    const hamburger = document.querySelector('.hamburger');
    const navMenu = document.querySelector('.nav-menu');
    
    if (hamburger && navMenu) {
        hamburger.addEventListener('click', function() {
            navMenu.classList.toggle('active');
        });

        // Fermer le menu en cliquant sur un lien
        const navLinks = navMenu.querySelectorAll('a');
        navLinks.forEach(link => {
            link.addEventListener('click', function() {
                navMenu.classList.remove('active');
            });
        });
    }
}

// Fonctions utilitaires pour localStorage
function getUsers() {
    return JSON.parse(localStorage.getItem('users') || '[]');
}

function saveUsers(users) {
    localStorage.setItem('users', JSON.stringify(users));
}

function getCurrentUser() {
    const user = localStorage.getItem('currentUser');
    return user ? JSON.parse(user) : null;
}

function setCurrentUser(user) {
    if (user) {
        localStorage.setItem('currentUser', JSON.stringify(user));
    } else {
        localStorage.removeItem('currentUser');
    }
}

function getAdmin() {
    return JSON.parse(localStorage.getItem('admin') || '{}');
}

// Fonction pour convertir une image en base64
function fileToBase64(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => resolve(reader.result);
        reader.onerror = reject;
        reader.readAsDataURL(file);
    });
}

// Fonction pour valider une image
function validateImage(file) {
    const validTypes = ['image/png', 'image/jpg', 'image/jpeg', 'image/gif', 'image/webp'];
    const maxSize = 5 * 1024 * 1024; // 5MB

    if (!validTypes.includes(file.type)) {
        return { valid: false, error: 'Format non supporté. Utilisez PNG, JPG, JPEG, GIF ou WEBP.' };
    }

    if (file.size > maxSize) {
        return { valid: false, error: 'Fichier trop volumineux. Taille maximum : 5MB.' };
    }

    return { valid: true };
}

// Fonction pour afficher un message
function showMessage(containerId, message, type = 'success') {
    const container = document.getElementById(containerId);
    if (!container) return;

    container.className = `message-container show message-${type}`;
    container.textContent = message;

    // Masquer après 5 secondes pour les messages de succès
    if (type === 'success') {
        setTimeout(() => {
            container.classList.remove('show');
        }, 5000);
    }
}

// Fonction pour effacer les messages d'erreur
function clearErrors() {
    const errorMessages = document.querySelectorAll('.error-message');
    errorMessages.forEach(error => {
        error.textContent = '';
    });
}

// Vérifier si un pseudo existe déjà
function pseudoExists(pseudo) {
    const users = getUsers();
    return users.some(user => user.pseudo.toLowerCase() === pseudo.toLowerCase());
}

// Mettre à jour la navigation pour afficher les liens de profil/déconnexion
function updateNavigation() {
    const currentUser = getCurrentUser();
    const profilLink = document.getElementById('profilLink');
    const logoutLink = document.getElementById('logoutLink');
    const logoutBtnNav = document.getElementById('logoutBtnNav');
    
    if (currentUser) {
        if (profilLink) profilLink.style.display = 'block';
        if (logoutLink) logoutLink.style.display = 'block';
        
        if (logoutBtnNav) {
            logoutBtnNav.addEventListener('click', function(e) {
                e.preventDefault();
                if (confirm('Êtes-vous sûr de vouloir vous déconnecter ?')) {
                    setCurrentUser(null);
                    window.location.href = 'index.html';
                }
            });
        }
    } else {
        if (profilLink) profilLink.style.display = 'none';
        if (logoutLink) logoutLink.style.display = 'none';
    }
}

