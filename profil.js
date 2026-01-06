// Script pour la page de profil

document.addEventListener('DOMContentLoaded', function() {
    loadProfil();
    
    // Bouton de déconnexion
    const logoutBtn = document.getElementById('logoutBtnNav');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', function(e) {
            e.preventDefault();
            if (confirm('Êtes-vous sûr de vouloir vous déconnecter ?')) {
                setCurrentUser(null);
                window.location.href = 'index.html';
            }
        });
    }
});

function loadProfil() {
    const currentUser = getCurrentUser();
    const profilContent = document.getElementById('profilContent');
    const notConnected = document.getElementById('notConnected');
    
    if (!currentUser) {
        profilContent.style.display = 'none';
        notConnected.style.display = 'block';
        return;
    }
    
    // Récupérer les informations complètes de l'utilisateur
    const users = getUsers();
    const user = users.find(u => u.id === currentUser.id);
    
    if (!user) {
        profilContent.innerHTML = '<p style="text-align: center; color: var(--text-light);">Utilisateur non trouvé.</p>';
        return;
    }
    
    // Afficher le profil
    const statusText = {
        'pending': 'En attente de validation',
        'approved': 'Inscription approuvée',
        'rejected': 'Inscription refusée'
    }[user.status] || 'Statut inconnu';
    
    const statusClass = user.status || 'pending';
    
    profilContent.innerHTML = `
        <div class="profil-header">
            ${user.photoProfil ? `
                <div class="profil-avatar">
                    <img src="${user.photoProfil}" alt="Photo de profil">
                </div>
            ` : `
                <div class="profil-avatar">
                    <div class="avatar-placeholder">${user.pseudo.charAt(0).toUpperCase()}</div>
                </div>
            `}
            <div class="profil-info-header">
                <h3>${escapeHtml(user.pseudo)}</h3>
                <span class="status-badge status-${statusClass}">${statusText}</span>
            </div>
        </div>
        
        <div class="profil-details">
            ${user.nomComplet ? `
                <div class="profil-detail-item">
                    <strong>Nom complet</strong>
                    <span>${escapeHtml(user.nomComplet)}</span>
                </div>
            ` : ''}
            
            ${user.contact ? `
                <div class="profil-detail-item">
                    <strong>Contact</strong>
                    <span>${escapeHtml(user.contact)}</span>
                </div>
            ` : ''}
            
            <div class="profil-detail-item">
                <strong>Numéro de paiement</strong>
                <span>${escapeHtml(user.numeroPaiement)}</span>
            </div>
            
            <div class="profil-detail-item">
                <strong>Date d'inscription</strong>
                <span>${new Date(user.dateInscription).toLocaleDateString('fr-FR', {
                    year: 'numeric',
                    month: 'long',
                    day: 'numeric',
                    hour: '2-digit',
                    minute: '2-digit'
                })}</span>
            </div>
            
            ${user.message ? `
                <div class="profil-detail-item">
                    <strong>Message</strong>
                    <p style="margin-top: 0.5rem; color: var(--text-color);">${escapeHtml(user.message)}</p>
                </div>
            ` : ''}
        </div>
        
        ${user.screenshotPaiement ? `
            <div class="profil-screenshot">
                <strong>Screenshot de paiement</strong>
                <div class="profil-image-container">
                    <img src="${user.screenshotPaiement}" alt="Screenshot paiement" onclick="openModal('${user.screenshotPaiement}')">
                </div>
            </div>
        ` : ''}
        
        <div class="profil-actions">
            <a href="bracket.html" class="btn btn-primary">Voir le Bracket</a>
            <button class="btn btn-secondary" id="logoutBtn">Se déconnecter</button>
        </div>
    `;
    
    // Gérer la déconnexion
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', function() {
            if (confirm('Êtes-vous sûr de vouloir vous déconnecter ?')) {
                setCurrentUser(null);
                window.location.href = 'index.html';
            }
        });
    }
    
    // Afficher les liens de navigation (utilise la fonction de script.js)
    if (typeof updateNavigation === 'function') {
        updateNavigation();
    }
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

window.openModal = function(imageSrc) {
    const modal = document.createElement('div');
    modal.className = 'modal active';
    modal.innerHTML = `<img src="${imageSrc}" class="modal-content" alt="Image agrandie">`;
    modal.addEventListener('click', function() {
        document.body.removeChild(modal);
    });
    document.body.appendChild(modal);
};

