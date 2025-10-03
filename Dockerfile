# Utiliser une image Python officielle comme base
FROM python:3.11-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier le fichier requirements.txt
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier tous les fichiers de l'application
COPY . .

# Exposer le port 8501 pour Streamlit
EXPOSE 8501

# Créer un utilisateur non-root pour la sécurité
RUN useradd -m -u 1000 streamlit && chown -R streamlit:streamlit /app
USER streamlit

# Configurer Streamlit
RUN mkdir -p /home/streamlit/.streamlit
RUN echo "[server]\nheadless = true\nport = 8501\naddress = 0.0.0.0\n" > /home/streamlit/.streamlit/config.toml

# Commande pour démarrer l'application
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501"]