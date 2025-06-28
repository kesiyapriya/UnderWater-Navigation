#!/bin/bash

echo "🐳 Setting up MongoDB with Docker Compose for Underwater Navigation API"
echo "================================================================"

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "✅ Docker and Docker Compose are available"

# Create data directories for volume mounting (optional, Docker will create them)
echo "📁 Creating local data directories..."
mkdir -p ./mongodb_data
mkdir -p ./mongodb_config

echo "🚀 Starting MongoDB container with persistent storage..."

# Stop and remove existing containers if they exist
echo "🔄 Stopping existing containers..."
docker-compose down

# Start MongoDB and Mongo Express
echo "🐳 Starting MongoDB services..."
docker-compose up -d

# Wait a bit for containers to start
echo "⏳ Waiting for services to start..."
sleep 10

# Check if containers are running
echo "📊 Checking container status..."
docker-compose ps

echo ""
echo "🎉 Setup complete!"
echo "================================================================"
echo "📊 MongoDB is running on: http://localhost:27017"
echo "🌐 Mongo Express (Web UI) is running on: http://localhost:8081"
echo ""
echo "Database credentials:"
echo "  Username: admin"
echo "  Password: underwater_nav_2025"
echo "  Database: underwater_navigation"
echo ""
echo "📂 Data persistence:"
echo "  MongoDB data is stored in Docker volume 'mongodb_data'"
echo "  This ensures your data will persist even if containers are stopped/removed"
echo ""
echo "🔧 Useful commands:"
echo "  Stop services: docker-compose down"
echo "  View logs: docker-compose logs -f"
echo "  Restart services: docker-compose restart"
echo "  Remove all (including volumes): docker-compose down -v"
echo ""
echo "🚀 Now you can start your FastAPI server with: python main.py"
