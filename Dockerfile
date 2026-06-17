# TP6 — Conteneurisation de l'application Dash
FROM python:3.12-slim

WORKDIR /app

# Installer les dépendances d'abord (cache Docker plus efficace)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code de l'application
COPY . .

# Port exposé
EXPOSE 8050

# Lancement via Gunicorn (serveur de production)
# "app:server" = fichier app.py, objet Flask `server`
CMD ["gunicorn", "app:server", "--bind", "0.0.0.0:8050", "--workers", "4"]
