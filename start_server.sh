#!/bin/bash

# Start Underwater Navigation API Server
echo "🚀 Starting Underwater Navigation Data Collection API Server..."
echo "📡 Installing dependencies..."

# Install Python dependencies
pip install -r requirements.txt

echo ""
echo "🌊 Starting FastAPI server for underwater navigation data collection..."
echo "Server will be available at: http://localhost:8000"
echo "API Documentation: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the FastAPI server using uvicorn directly (recommended)
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
