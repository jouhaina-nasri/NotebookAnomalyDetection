# Utilisez une image de base Node
FROM node:14

# Définissez un répertoire de travail
WORKDIR /app

# Installez les dépendances
COPY package*.json ./
RUN npm cache clean --force
RUN npm install


# Copiez le reste du code
COPY . .

# Exposez le port sur lequel votre application sera accessible
EXPOSE 3000

# Lancez l'application
CMD ["npm", "start"]
