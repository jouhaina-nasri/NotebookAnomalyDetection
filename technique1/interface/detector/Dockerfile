FROM node:22-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .

# URL of the Flask API as seen from the user's browser
ARG VITE_API_URL=http://127.0.0.1:5000
ENV VITE_API_URL=$VITE_API_URL
RUN npm run build

EXPOSE 3000
CMD ["npm", "run", "preview"]
