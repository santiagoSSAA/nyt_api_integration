# frontend/Dockerfile
FROM node:14

WORKDIR /app

# Copiar archivos de dependencias
COPY package.json yarn.lock ./
RUN yarn install

# Copiar el resto del código
COPY . .

# Construir la aplicación
RUN yarn build

# Exponer el puerto 3000 para React
EXPOSE 3000

# Comando para ejecutar la aplicación
CMD ["yarn", "start"]
