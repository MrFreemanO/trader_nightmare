#!/bin/sh

# Railway deployment startup script for frontend
echo "Starting Railway deployment..."

# If VITE_API_URL is not set, try to detect it from Railway environment
if [ -z "$VITE_API_URL" ]; then
    if [ ! -z "$RAILWAY_STATIC_URL" ]; then
        # Use Railway's backend URL if available
        export VITE_API_URL="https://$RAILWAY_STATIC_URL"
        echo "Using Railway URL: $VITE_API_URL"
    else
        echo "Warning: VITE_API_URL not set, using default"
        export VITE_API_URL="http://localhost:5000"
    fi
fi

echo "API URL configured as: $VITE_API_URL"

# Start nginx
echo "Starting nginx..."
nginx -g 'daemon off;'