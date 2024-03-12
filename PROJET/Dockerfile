# Utiliser l'image Python officielle
FROM python:3.8-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier le fichier main.py dans le conteneur
COPY main.py main.py

# Installer Flask
RUN pip install --no-cache-dir flask

# Exposer le port sur lequel l'application Flask s'exécute
EXPOSE 5000

# Commande par défaut pour exécuter l'application Flask
CMD ["python", "main.py"]
