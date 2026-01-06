// Script pour la page de connexion

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('connexionForm');

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        clearErrors();

        const pseudo = document.getElementById('pseudo').value.trim();
        const password = document.getElementById('password').value;

        // Validation
        if (!pseudo) {
            document.getElementById('pseudoError').textContent = 'Le pseudo est obligatoire';
            return;
        }

        if (!password) {
            document.getElementById('passwordError').textContent = 'Le mot de passe est obligatoire';
            return;
        }

        // Vérifier les identifiants
        const users = getUsers();
        const user = users.find(u => 
            u.pseudo.toLowerCase() === pseudo.toLowerCase() && 
            u.password === password
        );

        if (!user) {
            showMessage('messageContainer', 'Pseudo ou mot de passe incorrect', 'error');
            return;
        }

        // Connexion réussie
        setCurrentUser({
            id: user.id,
            pseudo: user.pseudo,
            nomComplet: user.nomComplet
        });

        showMessage('messageContainer', 'Connexion réussie ! Redirection...', 'success');

        // Redirection vers le profil après 1 seconde
        setTimeout(() => {
            window.location.href = 'profil.html';
        }, 1000);
    });
});

