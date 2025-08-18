# ---------- Build stage ----------
FROM node:18 AS builder
WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

# Set build-time environment variables
ARG VITE_API_URL
ENV VITE_API_URL=$VITE_API_URL

# Build the application
RUN npm run build -- --logLevel info

# ---------- Production stage ----------
FROM nginx:alpine

# Install curl for healthchecks
RUN apk add --no-cache curl

# Copy the built application
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy startup script
COPY start.sh /start.sh
RUN chmod +x /start.sh

EXPOSE 80
CMD ["/start.sh"]