// Script pour la page d'inscription

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('inscriptionForm');
    const photoProfilInput = document.getElementById('photoProfil');
    const screenshotPaiementInput = document.getElementById('screenshotPaiement');
    const photoProfilPreview = document.getElementById('photoProfilPreview');
    const screenshotPaiementPreview = document.getElementById('screenshotPaiementPreview');

    // Prévisualisation photo de profil
    photoProfilInput.addEventListener('change', function(e) {
        handleImagePreview(e.target.files[0], photoProfilPreview, 'photoProfilError');
    });

    // Prévisualisation screenshot paiement
    screenshotPaiementInput.addEventListener('change', function(e) {
        handleImagePreview(e.target.files[0], screenshotPaiementPreview, 'screenshotPaiementError');
    });

    // Soumission du formulaire
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        clearErrors();

        const pseudo = document.getElementById('pseudo').value.trim();
        const nomComplet = document.getElementById('nomComplet').value.trim();
        const contact = document.getElementById('contact').value.trim();
        const password = document.getElementById('password').value;
        const numeroPaiement = document.getElementById('numeroPaiement').value.trim();
        const message = document.getElementById('message').value.trim();
        const photoProfilFile = photoProfilInput.files[0];
        const screenshotPaiementFile = screenshotPaiementInput.files[0];

        // Validation
        let isValid = true;

        // Validation pseudo
        if (!pseudo) {
            document.getElementById('pseudoError').textContent = 'Le pseudo est obligatoire';
            isValid = false;
        } else if (pseudoExists(pseudo)) {
            document.getElementById('pseudoError').textContent = 'Ce pseudo est déjà utilisé';
            isValid = false;
        }

        // Validation mot de passe
        if (!password) {
            document.getElementById('passwordError').textContent = 'Le mot de passe est obligatoire';
            isValid = false;
        } else if (password.length < 6) {
            document.getElementById('passwordError').textContent = 'Le mot de passe doit contenir au moins 6 caractères';
            isValid = false;
        }

        // Validation numéro de paiement
        if (!numeroPaiement) {
            document.getElementById('numeroPaiementError').textContent = 'Le numéro de paiement est obligatoire';
            isValid = false;
        }

        // Validation images
        let photoProfilBase64 = null;
        let screenshotPaiementBase64 = null;

        if (photoProfilFile) {
            const validation = validateImage(photoProfilFile);
            if (!validation.valid) {
                document.getElementById('photoProfilError').textContent = validation.error;
                isValid = false;
            } else {
                try {
                    photoProfilBase64 = await fileToBase64(photoProfilFile);
                } catch (error) {
                    document.getElementById('photoProfilError').textContent = 'Erreur lors du chargement de l\'image';
                    isValid = false;
                }
            }
        }

        if (screenshotPaiementFile) {
            const validation = validateImage(screenshotPaiementFile);
            if (!validation.valid) {
                document.getElementById('screenshotPaiementError').textContent = validation.error;
                isValid = false;
            } else {
                try {
                    screenshotPaiementBase64 = await fileToBase64(screenshotPaiementFile);
                } catch (error) {
                    document.getElementById('screenshotPaiementError').textContent = 'Erreur lors du chargement de l\'image';
                    isValid = false;
                }
            }
        }

        if (!isValid) {
            showMessage('messageContainer', 'Erreur : vérifiez vos informations', 'error');
            return;
        }

        // Créer l'utilisateur
        const user = {
            id: Date.now().toString(),
            pseudo: pseudo,
            nomComplet: nomComplet || null,
            contact: contact || null,
            password: password, // En production, il faudrait hasher le mot de passe
            photoProfil: photoProfilBase64,
            screenshotPaiement: screenshotPaiementBase64,
            numeroPaiement: numeroPaiement,
            message: message || null,
            status: 'pending', // pending, approved, rejected
            dateInscription: new Date().toISOString()
        };

        // Sauvegarder
        const users = getUsers();
        users.push(user);
        saveUsers(users);

        // Message de succès
        showMessage('messageContainer', 'Inscription réussie ! Votre demande est en attente de validation par l\'administrateur.', 'success');

        // Réinitialiser le formulaire
        form.reset();
        photoProfilPreview.classList.remove('active');
        screenshotPaiementPreview.classList.remove('active');
        photoProfilPreview.innerHTML = '';
        screenshotPaiementPreview.innerHTML = '';

        // Animation de succès
        form.style.transform = 'scale(0.98)';
        setTimeout(() => {
            form.style.transform = 'scale(1)';
        }, 200);
    });
});

// Fonction pour gérer la prévisualisation d'image
function handleImagePreview(file, previewContainer, errorId) {
    const errorElement = document.getElementById(errorId);
    
    if (!file) {
        previewContainer.classList.remove('active');
        previewContainer.innerHTML = '';
        return;
    }

    const validation = validateImage(file);
    if (!validation.valid) {
        errorElement.textContent = validation.error;
        previewContainer.classList.remove('active');
        previewContainer.innerHTML = '';
        return;
    }

    errorElement.textContent = '';

    const reader = new FileReader();
    reader.onload = function(e) {
        previewContainer.innerHTML = `<img src="${e.target.result}" alt="Prévisualisation">`;
        previewContainer.classList.add('active');
    };
    reader.readAsDataURL(file);
}

