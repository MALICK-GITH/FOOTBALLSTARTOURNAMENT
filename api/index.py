# Vercel serverless entry point
import sys
import os

# Ajouter le répertoire parent au path pour importer app
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from app import app

# Export the Flask app for Vercel
# @vercel/python attend directement l'app Flask
handler = app

