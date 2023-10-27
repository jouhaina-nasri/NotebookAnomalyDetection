# Utilisez une image de base Python
FROM python:3.9

WORKDIR /app

# Copiez le fichier de dépendances et installez les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Créez le dossier pour les fichiers uploadés et définissez les bonnes permissions
RUN mkdir -p /app/uploads && chmod 777 /app/uploads

# Copiez le reste du code (y compris les modules supplémentaires)
COPY . .

# Exposez le port sur lequel votre application sera accessible
EXPOSE 5000

# Lancez l'application
ENV PYTHONPATH "${PYTHONPATH}:/app"
CMD ["flask", "run", "--host=0.0.0.0"]
