#!/bin/bash
# Start Kanban Board Server
# Usage: ./START_KANBAN.sh

echo "🐝 Starting Gematria Hive Kanban Board..."
echo ""

# Check if FastAPI is installed
python -c "import fastapi" 2>/dev/null || {
    echo "⚠️  FastAPI not installed. Installing..."
    pip install fastapi "uvicorn[standard]" python-multipart -q
}

# Start the server
echo "✅ Starting server on http://localhost:8000"
echo "📋 Open in browser: http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop"
echo ""

python run_kanban.py

