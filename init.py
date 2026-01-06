"""
Script d'initialisation pour créer les dossiers et fichiers nécessaires
"""
import os
import json

# Créer les dossiers
os.makedirs('data', exist_ok=True)
os.makedirs('uploads', exist_ok=True)

# Initialiser les fichiers JSON
if not os.path.exists('data/players.json'):
    with open('data/players.json', 'w', encoding='utf-8') as f:
        json.dump([], f)
    print("✓ Fichier data/players.json créé")

if not os.path.exists('data/bracket.json'):
    with open('data/bracket.json', 'w', encoding='utf-8') as f:
        json.dump({
            'quarterfinals': [],
            'semifinals': [],
            'final': None,
            'winner': None
        }, f, ensure_ascii=False, indent=2)
    print("✓ Fichier data/bracket.json créé")

if not os.path.exists('data/admin.json'):
    from werkzeug.security import generate_password_hash
    with open('data/admin.json', 'w', encoding='utf-8') as f:
        json.dump({
            'username': 'admin',
            'password': generate_password_hash('admin123')
        }, f, ensure_ascii=False, indent=2)
    print("✓ Fichier data/admin.json créé")
    print("⚠️  Identifiants admin par défaut : admin / admin123")
    print("⚠️  CHANGEZ LE MOT DE PASSE EN PRODUCTION !")

print("\n✅ Initialisation terminée !")
print("Vous pouvez maintenant lancer l'application avec : python app.py")

