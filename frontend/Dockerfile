FROM node:18-alpine

WORKDIR /app

# Копирование package.json и установка зависимостей
COPY package*.json ./
RUN npm install

# Копирование кода
COPY . .

# Сборка для production
RUN npm run build

# Открываем порт
EXPOSE 3000

# Запуск dev сервера
CMD ["npm", "run", "dev", "--", "--host"]