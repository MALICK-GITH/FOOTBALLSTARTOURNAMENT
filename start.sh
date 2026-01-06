#!/bin/bash
# Script de démarrage pour Render.com
# Utilise gunicorn en production, Flask dev server en local

if [ -z "$PORT" ]; then
    export PORT=5000
fi

# Démarrer avec gunicorn pour la production
exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 2 --timeout 120 app:app


