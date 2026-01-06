// Script pour la page bracket

document.addEventListener('DOMContentLoaded', function() {
    loadBracket();
});

function loadBracket() {
    const users = getUsers();
    const approvedUsers = users.filter(user => user.status === 'approved');

    const bracketContainer = document.getElementById('bracketContainer');
    const bracketContent = document.getElementById('bracketContent');
    const bracketEmpty = bracketContainer.querySelector('.bracket-empty');

    if (approvedUsers.length === 0) {
        bracketEmpty.style.display = 'block';
        bracketContent.style.display = 'none';
        return;
    }

    bracketEmpty.style.display = 'none';
    bracketContent.style.display = 'block';

    // Générer le bracket
    generateBracket(approvedUsers);
}

function generateBracket(players) {
    const bracketTree = document.getElementById('bracketTree');
    bracketTree.innerHTML = '';

    // Trier les joueurs par date d'inscription
    const sortedPlayers = [...players].sort((a, b) => 
        new Date(a.dateInscription) - new Date(b.dateInscription)
    );

    // Calculer le nombre de rounds nécessaires
    const numPlayers = sortedPlayers.length;
    if (numPlayers === 0) return;

    // Calculer le nombre de rounds (puissance de 2 supérieure)
    let numRounds = Math.ceil(Math.log2(numPlayers));
    if (numRounds === 0) numRounds = 1;

    // Créer les rounds
    let currentRoundPlayers = sortedPlayers;
    const rounds = [];

    for (let round = numRounds; round >= 1; round--) {
        const roundMatches = [];
        const nextRoundPlayers = [];

        // Créer les matchs pour ce round
        for (let i = 0; i < currentRoundPlayers.length; i += 2) {
            const player1 = currentRoundPlayers[i];
            const player2 = currentRoundPlayers[i + 1] || null;

            // Simuler un gagnant (pour la démo, on prend le premier joueur)
            const winner = player1;

            roundMatches.push({
                player1: player1,
                player2: player2,
                winner: winner
            });

            if (round > 1) {
                nextRoundPlayers.push(winner);
            }
        }

        rounds.push({
            roundNumber: round,
            roundName: getRoundName(round, numRounds),
            matches: roundMatches
        });

        currentRoundPlayers = nextRoundPlayers;
    }

    // Afficher les rounds (du premier au dernier)
    rounds.reverse().forEach(roundData => {
        const roundDiv = document.createElement('div');
        roundDiv.className = 'bracket-round';

        const roundTitle = document.createElement('div');
        roundTitle.className = 'round-title';
        roundTitle.textContent = roundData.roundName;
        roundDiv.appendChild(roundTitle);

        roundData.matches.forEach(match => {
            const matchDiv = document.createElement('div');
            matchDiv.className = 'bracket-match';

            // Joueur 1
            const player1Div = document.createElement('div');
            player1Div.className = `match-player ${match.winner === match.player1 ? 'winner' : ''}`;
            if (match.player1.photoProfil) {
                const img = document.createElement('img');
                img.src = match.player1.photoProfil;
                img.alt = match.player1.pseudo;
                player1Div.appendChild(img);
            }
            const player1Name = document.createElement('span');
            player1Name.textContent = match.player1.pseudo;
            player1Div.appendChild(player1Name);
            matchDiv.appendChild(player1Div);

            // VS
            if (match.player2) {
                const vsDiv = document.createElement('div');
                vsDiv.className = 'match-vs';
                vsDiv.textContent = 'VS';
                matchDiv.appendChild(vsDiv);

                // Joueur 2
                const player2Div = document.createElement('div');
                player2Div.className = `match-player ${match.winner === match.player2 ? 'winner' : ''}`;
                if (match.player2.photoProfil) {
                    const img = document.createElement('img');
                    img.src = match.player2.photoProfil;
                    img.alt = match.player2.pseudo;
                    player2Div.appendChild(img);
                }
                const player2Name = document.createElement('span');
                player2Name.textContent = match.player2.pseudo;
                player2Div.appendChild(player2Name);
                matchDiv.appendChild(player2Div);
            } else {
                // Bye (pas d'adversaire)
                const byeDiv = document.createElement('div');
                byeDiv.className = 'match-player';
                byeDiv.textContent = 'Bye';
                byeDiv.style.opacity = '0.5';
                matchDiv.appendChild(byeDiv);
            }

            roundDiv.appendChild(matchDiv);
        });

        bracketTree.appendChild(roundDiv);
    });
}

function getRoundName(roundNumber, totalRounds) {
    const roundNames = {
        1: 'Finale',
        2: 'Demi-finales',
        3: 'Quarts de finale',
        4: 'Huitièmes de finale',
        5: 'Seizièmes de finale'
    };

    if (roundNumber === totalRounds && totalRounds === 1) {
        return 'Finale';
    }

    return roundNames[roundNumber] || `Round ${roundNumber}`;
}

// Recharger le bracket toutes les 5 secondes (simulation de mise à jour)
setInterval(() => {
    loadBracket();
}, 5000);

