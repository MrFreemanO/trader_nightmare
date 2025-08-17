# ---------- Build stage ----------
FROM node:18 AS builder

WORKDIR /app

# Сначала ставим зависимости
COPY package*.json ./
RUN npm install

# Копируем весь код
COPY . .

# Собираем проект
RUN npm run build


# ---------- Production stage ----------
FROM nginx:alpine

# Копируем готовый билд
COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]