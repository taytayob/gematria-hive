#!/bin/bash

# Gematria Hive Webapp Startup Script

echo "🐝 Starting Gematria Hive Webapp..."

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
fi

# Check if port 3000 is in use
if lsof -Pi :3000 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo "⚠️  Port 3000 is already in use!"
    echo "   Trying to kill process on port 3000..."
    kill -9 $(lsof -ti:3000) 2>/dev/null || true
    sleep 1
fi

# Start dev server
echo "🚀 Starting development server on port 3000..."
npm run dev

