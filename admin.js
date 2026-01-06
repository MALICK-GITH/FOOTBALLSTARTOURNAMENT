// Script pour la page admin

document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('adminLoginForm');
    const loginSection = document.getElementById('adminLoginSection');
    const adminPanel = document.getElementById('adminPanel');
    const logoutBtn = document.getElementById('logoutBtn');
    const statusFilter = document.getElementById('statusFilter');
    const tabButtons = document.querySelectorAll('.tab-btn');

    // Vérifier si déjà connecté
    checkAdminSession();

    // Connexion admin
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            e.preventDefault();

            const pseudo = document.getElementById('adminPseudo').value.trim();
            const password = document.getElementById('adminPassword').value;

            const admin = getAdmin();

            if (pseudo === admin.pseudo && password === admin.password) {
                // Connexion réussie
                localStorage.setItem('adminSession', 'true');
                showMessage('adminMessageContainer', 'Connexion réussie', 'success');
                
                setTimeout(() => {
                    showAdminPanel();
                }, 500);
            } else {
                showMessage('adminMessageContainer', 'Identifiants incorrects', 'error');
            }
        });
    }

    // Déconnexion
    if (logoutBtn) {
        logoutBtn.addEventListener('click', function() {
            localStorage.removeItem('adminSession');
            hideAdminPanel();
        });
    }

    // Filtre par statut
    if (statusFilter) {
        statusFilter.addEventListener('change', function() {
            loadInscriptions();
        });
    }

    // Onglets
    tabButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            const tabName = this.getAttribute('data-tab');
            switchTab(tabName);
        });
    });

    function checkAdminSession() {
        if (localStorage.getItem('adminSession') === 'true') {
            showAdminPanel();
        }
    }

    function showAdminPanel() {
        loginSection.style.display = 'none';
        adminPanel.style.display = 'block';
        loadInscriptions();
        loadMessages();
    }

    function hideAdminPanel() {
        loginSection.style.display = 'block';
        adminPanel.style.display = 'none';
        if (loginForm) loginForm.reset();
    }

    function switchTab(tabName) {
        // Mettre à jour les boutons
        tabButtons.forEach(btn => {
            btn.classList.remove('active');
            if (btn.getAttribute('data-tab') === tabName) {
                btn.classList.add('active');
            }
        });

        // Mettre à jour le contenu
        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.remove('active');
        });

        if (tabName === 'inscriptions') {
            document.getElementById('inscriptionsTab').classList.add('active');
        } else if (tabName === 'messages') {
            document.getElementById('messagesTab').classList.add('active');
            loadMessages();
        }
    }

    function loadInscriptions() {
        const users = getUsers();
        const statusFilterValue = statusFilter ? statusFilter.value : 'all';
        
        let filteredUsers = users;
        if (statusFilterValue !== 'all') {
            filteredUsers = users.filter(user => user.status === statusFilterValue);
        }

        const container = document.getElementById('inscriptionsList');
        if (!container) return;

        if (filteredUsers.length === 0) {
            container.innerHTML = '<p style="text-align: center; color: var(--text-light); padding: 2rem;">Aucune inscription trouvée.</p>';
            return;
        }

        container.innerHTML = filteredUsers.map(user => {
            const statusClass = user.status || 'pending';
            const statusText = {
                'pending': 'En attente',
                'approved': 'Approuvé',
                'rejected': 'Refusé'
            }[statusClass] || 'En attente';

            return `
                <div class="inscription-card ${statusClass}">
                    <div class="inscription-header">
                        <div class="inscription-info">
                            <h4>${escapeHtml(user.pseudo)}</h4>
                            <span class="status-badge status-${statusClass}">${statusText}</span>
                        </div>
                    </div>
                    <div class="inscription-details">
                        ${user.nomComplet ? `
                            <div class="inscription-detail">
                                <strong>Nom complet</strong>
                                <span>${escapeHtml(user.nomComplet)}</span>
                            </div>
                        ` : ''}
                        ${user.contact ? `
                            <div class="inscription-detail">
                                <strong>Contact</strong>
                                <span>${escapeHtml(user.contact)}</span>
                            </div>
                        ` : ''}
                        <div class="inscription-detail">
                            <strong>Numéro de paiement</strong>
                            <span>${escapeHtml(user.numeroPaiement)}</span>
                        </div>
                        <div class="inscription-detail">
                            <strong>Date d'inscription</strong>
                            <span>${new Date(user.dateInscription).toLocaleDateString('fr-FR')}</span>
                        </div>
                    </div>
                    ${user.photoProfil || user.screenshotPaiement ? `
                        <div class="inscription-images">
                            ${user.photoProfil ? `
                                <div class="inscription-image">
                                    <img src="${user.photoProfil}" alt="Photo de profil" onclick="openModal('${user.photoProfil}')">
                                    <div class="image-label">Photo de profil</div>
                                </div>
                            ` : ''}
                            ${user.screenshotPaiement ? `
                                <div class="inscription-image">
                                    <img src="${user.screenshotPaiement}" alt="Screenshot paiement" onclick="openModal('${user.screenshotPaiement}')">
                                    <div class="image-label">Screenshot paiement</div>
                                </div>
                            ` : ''}
                        </div>
                    ` : ''}
                    ${user.message ? `
                        <div class="inscription-detail" style="margin-top: 1rem;">
                            <strong>Message</strong>
                            <p style="margin-top: 0.5rem; color: var(--text-color);">${escapeHtml(user.message)}</p>
                        </div>
                    ` : ''}
                    <div class="inscription-actions">
                        ${user.status !== 'approved' ? `
                            <button class="btn btn-success" onclick="approveUser('${user.id}')">Approuver</button>
                        ` : ''}
                        ${user.status !== 'rejected' ? `
                            <button class="btn btn-danger" onclick="rejectUser('${user.id}')">Refuser</button>
                        ` : ''}
                        <button class="btn btn-secondary" onclick="deleteUser('${user.id}')">Supprimer</button>
                    </div>
                </div>
            `;
        }).join('');
    }

    function loadMessages() {
        const users = getUsers();
        const usersWithMessages = users.filter(user => user.message);

        const container = document.getElementById('messagesList');
        if (!container) return;

        if (usersWithMessages.length === 0) {
            container.innerHTML = '<p style="text-align: center; color: var(--text-light); padding: 2rem;">Aucun message trouvé.</p>';
            return;
        }

        container.innerHTML = usersWithMessages.map(user => {
            return `
                <div class="message-card">
                    <div class="inscription-header">
                        <h4>${escapeHtml(user.pseudo)}</h4>
                        <span class="status-badge">${new Date(user.dateInscription).toLocaleDateString('fr-FR')}</span>
                    </div>
                    <p style="margin-top: 1rem; color: var(--text-color); line-height: 1.6;">${escapeHtml(user.message)}</p>
                </div>
            `;
        }).join('');
    }

    // Fonctions globales pour les actions
    window.approveUser = function(userId) {
        const users = getUsers();
        const userIndex = users.findIndex(u => u.id === userId);
        if (userIndex !== -1) {
            users[userIndex].status = 'approved';
            saveUsers(users);
            loadInscriptions();
            showMessage('adminPanelMessageContainer', 'Utilisateur approuvé avec succès', 'success');
        }
    };

    window.rejectUser = function(userId) {
        const users = getUsers();
        const userIndex = users.findIndex(u => u.id === userId);
        if (userIndex !== -1) {
            users[userIndex].status = 'rejected';
            saveUsers(users);
            loadInscriptions();
            showMessage('adminPanelMessageContainer', 'Utilisateur refusé', 'success');
        }
    };

    window.deleteUser = function(userId) {
        if (confirm('Êtes-vous sûr de vouloir supprimer cet utilisateur ?')) {
            const users = getUsers();
            const filteredUsers = users.filter(u => u.id !== userId);
            saveUsers(filteredUsers);
            loadInscriptions();
            loadMessages();
            showMessage('adminPanelMessageContainer', 'Utilisateur supprimé', 'success');
        }
    };

    window.openModal = function(imageSrc) {
        const modal = document.createElement('div');
        modal.className = 'modal active';
        modal.innerHTML = `<img src="${imageSrc}" class="modal-content" alt="Image agrandie">`;
        modal.addEventListener('click', function() {
            document.body.removeChild(modal);
        });
        document.body.appendChild(modal);
    };

    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
});

