FROM python:3.13-slim

WORKDIR /app

# Copier le projet (code + pyproject + README, etc.)
COPY . .

# Installer les dépendances décrites dans pyproject.toml
# (comme tu l'as fait en local avec `pip install -e .`)
RUN pip install --no-cache-dir -e .

# Très important : dire à Python de chercher aussi dans /app/src
ENV PYTHONPATH=/app/src

# Lancer la même commande que sur ta machine
CMD ["streamlit", "run", "src/maison_estimateur/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
