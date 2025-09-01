#!/bin/sh

# Railway deployment startup script for frontend
echo "Starting Railway deployment..."

# VITE_API_URL must be supplied at build time.
# For runtime overrides, inject settings via nginx or a separate config file.
if [ -n "$VITE_API_URL" ]; then
    echo "Using VITE_API_URL: $VITE_API_URL"
else
    echo "Warning: VITE_API_URL is not set."
fi

# Start nginx
echo "Starting nginx..."
nginx -g 'daemon off;'
