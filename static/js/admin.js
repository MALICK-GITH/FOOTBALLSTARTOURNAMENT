// Scripts spécifiques à l'administration

let currentSection = null;

// Vérifier que l'utilisateur est admin
document.addEventListener('DOMContentLoaded', async () => {
    await checkAuth();
    if (!currentUser || currentUser.role !== 'admin') {
        window.location.href = '/';
        return;
    }
});

// Gestion des sections
function loadSection(section) {
    // Cacher toutes les sections
    document.querySelectorAll('.section').forEach(s => s.classList.add('hidden'));
    
    // Afficher la section demandée
    const sectionDiv = document.getElementById(section + 'Section');
    if (sectionDiv) {
        sectionDiv.classList.remove('hidden');
        currentSection = section;
        
        // Charger les données de la section
        switch(section) {
            case 'users':
                loadUsers();
                break;
            case 'registrations':
                loadRegistrations();
                break;
            case 'tournaments':
                loadTournamentsAdmin();
                break;
            case 'messages':
                loadMessagesAdmin();
                break;
            case 'logs':
                loadLogs();
                break;
        }
    }
}

// Charger les utilisateurs
async function loadUsers() {
    try {
        const filter = document.getElementById('userFilter')?.value || '';
        const token = localStorage.getItem('token');
        
        let url = '/api/admin/users';
        if (filter) {
            url += `?status_filter=${filter}`;
        }
        
        const response = await fetch(url, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        const users = await response.json();
        const tbody = document.getElementById('usersTableBody');
        
        tbody.innerHTML = users.map(user => `
            <tr>
                <td>${user.id}</td>
                <td>${user.email}</td>
                <td>${user.username}</td>
                <td>${user.full_name}</td>
                <td>
                    <span class="status-badge status-${user.registration_status}">
                        ${user.registration_status}
                    </span>
                </td>
                <td>
                    ${user.registration_status === 'pending' ? `
                        <button class="btn btn-success" onclick="approveUser(${user.id})">Approuver</button>
                        <button class="btn btn-danger" onclick="rejectUser(${user.id})">Refuser</button>
                    ` : ''}
                    ${user.is_active ? `
                        <button class="btn btn-danger" onclick="blockUser(${user.id})">Bloquer</button>
                    ` : `
                        <button class="btn btn-success" onclick="unblockUser(${user.id})">Débloquer</button>
                    `}
                    ${user.role !== 'admin' ? `
                        <button class="btn btn-danger" onclick="deleteUser(${user.id})">Supprimer</button>
                    ` : ''}
                </td>
            </tr>
        `).join('');
    } catch (error) {
        console.error('Erreur de chargement des utilisateurs:', error);
    }
}

// Actions sur les utilisateurs
async function approveUser(userId) {
    if (!confirm('Approuver cet utilisateur?')) return;
    
    try {
        const token = localStorage.getItem('token');
        const response = await fetch(`/api/admin/users/${userId}/approve`, {
            method: 'PUT',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (response.ok) {
            showAlert('Utilisateur approuvé', 'success');
            loadUsers();
        }
    } catch (error) {
        showAlert('Erreur', 'error');
    }
}

async function rejectUser(userId) {
    if (!confirm('Refuser cet utilisateur?')) return;
    
    try {
        const token = localStorage.getItem('token');
        const response = await fetch(`/api/admin/users/${userId}/reject`, {
            method: 'PUT',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (response.ok) {
            showAlert('Utilisateur refusé', 'success');
            loadUsers();
        }
    } catch (error) {
        showAlert('Erreur', 'error');
    }
}

async function blockUser(userId) {
    if (!confirm('Bloquer cet utilisateur?')) return;
    
    try {
        const token = localStorage.getItem('token');
        const response = await fetch(`/api/admin/users/${userId}/block`, {
            method: 'PUT',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (response.ok) {
            showAlert('Utilisateur bloqué', 'success');
            loadUsers();
        }
    } catch (error) {
        showAlert('Erreur', 'error');
    }
}

async function unblockUser(userId) {
    try {
        const token = localStorage.getItem('token');
        const response = await fetch(`/api/admin/users/${userId}/unblock`, {
            method: 'PUT',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (response.ok) {
            showAlert('Utilisateur débloqué', 'success');
            loadUsers();
        }
    } catch (error) {
        showAlert('Erreur', 'error');
    }
}

async function deleteUser(userId) {
    if (!confirm('Supprimer définitivement cet utilisateur?')) return;
    
    try {
        const token = localStorage.getItem('token');
        const response = await fetch(`/api/admin/users/${userId}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (response.ok) {
            showAlert('Utilisateur supprimé', 'success');
            loadUsers();
        }
    } catch (error) {
        showAlert('Erreur', 'error');
    }
}

// Charger les inscriptions
async function loadRegistrations() {
    try {
        const filter = document.getElementById('registrationFilter')?.value || '';
        const token = localStorage.getItem('token');
        
        let url = '/api/admin/registrations';
        if (filter) {
            url += `?status_filter=${filter}`;
        }
        
        const response = await fetch(url, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        const registrations = await response.json();
        const tbody = document.getElementById('registrationsTableBody');
        
        tbody.innerHTML = registrations.map(reg => `
            <tr>
                <td>${reg.id}</td>
                <td>${reg.user.username} (${reg.user.email})</td>
                <td>Tournoi #${reg.tournament_id}</td>
                <td>
                    <span class="status-badge status-${reg.status}">${reg.status}</span>
                </td>
                <td>${new Date(reg.created_at).toLocaleDateString('fr-FR')}</td>
                <td>
                    ${reg.payment_proof ? `<a href="/static/uploads/${reg.payment_proof}" target="_blank">Voir preuve</a>` : 'Aucune preuve'}
                </td>
            </tr>
        `).join('');
    } catch (error) {
        console.error('Erreur de chargement des inscriptions:', error);
    }
}

// Charger les tournois (admin)
async function loadTournamentsAdmin() {
    try {
        const response = await fetch('/api/tournaments/');
        const tournaments = await response.json();
        const container = document.getElementById('tournamentsList');
        
        container.innerHTML = tournaments.map(tournament => `
            <div class="tournament-card">
                <h3>${tournament.name}</h3>
                <p>Participants: ${tournament.current_participants}/${tournament.max_participants}</p>
                <p>Frais: ${tournament.registration_fee}€</p>
                ${!tournament.is_started ? `
                    <button class="btn btn-primary" onclick="startTournament(${tournament.id})">Démarrer le tournoi</button>
                ` : '<p>Tournoi démarré</p>'}
            </div>
        `).join('');
    } catch (error) {
        console.error('Erreur:', error);
    }
}

async function startTournament(tournamentId) {
    if (!confirm('Démarrer ce tournoi? Les brackets seront générés automatiquement.')) return;
    
    try {
        const token = localStorage.getItem('token');
        const response = await fetch(`/api/tournaments/${tournamentId}/start`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (response.ok) {
            showAlert('Tournoi démarré avec succès!', 'success');
            loadTournamentsAdmin();
        }
    } catch (error) {
        showAlert('Erreur', 'error');
    }
}

// Gestion des messages
async function loadMessagesAdmin() {
    try {
        const response = await fetch('/api/messages/');
        const messages = await response.json();
        const container = document.getElementById('messagesList');
        
        container.innerHTML = messages.map(msg => `
            <div class="message-card ${msg.is_important ? 'important' : ''}">
                <div class="message-title">${msg.title}</div>
                <div class="message-content">${msg.content}</div>
                <div class="message-date">${new Date(msg.created_at).toLocaleDateString('fr-FR')}</div>
                <button class="btn btn-danger" onclick="deleteMessage(${msg.id})">Supprimer</button>
            </div>
        `).join('');
    } catch (error) {
        console.error('Erreur:', error);
    }
}

function showCreateMessageModal() {
    document.getElementById('createMessageModal').style.display = 'block';
}

async function createMessage(event) {
    event.preventDefault();
    
    const title = document.getElementById('messageTitle').value;
    const content = document.getElementById('messageContent').value;
    const isImportant = document.getElementById('messageImportant').checked;
    
    try {
        const token = localStorage.getItem('token');
        const response = await fetch('/api/messages/', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ title, content, is_important: isImportant })
        });
        
        if (response.ok) {
            showAlert('Message créé', 'success');
            closeModal('createMessageModal');
            loadMessagesAdmin();
        }
    } catch (error) {
        showAlert('Erreur', 'error');
    }
}

async function deleteMessage(messageId) {
    if (!confirm('Supprimer ce message?')) return;
    
    try {
        const token = localStorage.getItem('token');
        const response = await fetch(`/api/messages/${messageId}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (response.ok) {
            showAlert('Message supprimé', 'success');
            loadMessagesAdmin();
        }
    } catch (error) {
        showAlert('Erreur', 'error');
    }
}

// Charger les logs
async function loadLogs() {
    try {
        const token = localStorage.getItem('token');
        const response = await fetch('/api/admin/activity-logs', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        const logs = await response.json();
        const tbody = document.getElementById('logsTableBody');
        
        tbody.innerHTML = logs.map(log => `
            <tr>
                <td>${new Date(log.created_at).toLocaleString('fr-FR')}</td>
                <td>${log.action}</td>
                <td>${log.details || ''}</td>
                <td>${log.user_id || 'Système'}</td>
            </tr>
        `).join('');
    } catch (error) {
        console.error('Erreur:', error);
    }
}

