#!/bin/bash

echo "🐳 Docker Commands for MongoDB with Volume Mount"
echo "==============================================="

# Option 1: Using Docker Compose (Recommended)
echo "📋 Option 1: Docker Compose (Recommended)"
echo "------------------------------------------"
echo "Start MongoDB with Docker Compose:"
echo "docker-compose up -d"
echo ""
echo "Stop services:"
echo "docker-compose down"
echo ""
echo "Stop and remove volumes (WARNING: This deletes all data!):"
echo "docker-compose down -v"
echo ""

# Option 2: Using Docker Run with Named Volume
echo "📋 Option 2: Docker Run with Named Volume"
echo "-----------------------------------------"
echo "Create a named volume:"
echo "docker volume create mongodb_underwater_data"
echo ""
echo "Run MongoDB container with volume mount:"
echo 'docker run -d \
  --name underwater_mongodb \
  -p 27017:27017 \
  -e MONGO_INITDB_ROOT_USERNAME=admin \
  -e MONGO_INITDB_ROOT_PASSWORD=adminpassword \
  -e MONGO_INITDB_DATABASE=DHT_ENDPOINT \
  -v mongodb_underwater_data:/data/db \
  --restart=always \
  mongo:7.0'
echo ""

# Option 3: Using Docker Run with Host Directory Mount
echo "📋 Option 3: Docker Run with Host Directory Mount"
echo "------------------------------------------------"
echo "Create local directory:"
echo "mkdir -p ./mongodb_data"
echo ""
echo "Run MongoDB with host directory mount:"
echo 'docker run -d \
  --name underwater_mongodb_host \
  -p 27017:27017 \
  -e MONGO_INITDB_ROOT_USERNAME=admin \
  -e MONGO_INITDB_ROOT_PASSWORD=adminpassword \
  -e MONGO_INITDB_DATABASE=DHT_ENDPOINT \
  -v $(pwd)/mongodb_data:/data/db \
  --restart=always \
  mongo:7.0'
echo ""

# Management Commands
echo "📋 MongoDB Management Commands"
echo "-----------------------------"
echo "Check container status:"
echo "docker ps | grep mongo"
echo ""
echo "View container logs:"
echo "docker logs underwater_mongodb"
echo ""
echo "Connect to MongoDB shell:"
echo "docker exec -it underwater_mongodb mongosh --username admin --password adminpassword"
echo ""
echo "Stop container:"
echo "docker stop underwater_mongodb"
echo ""
echo "Remove container:"
echo "docker rm underwater_mongodb"
echo ""
echo "List volumes:"
echo "docker volume ls"
echo ""
echo "Remove volume (WARNING: This deletes all data!):"
echo "docker volume rm mongodb_underwater_data"
echo ""

# Quick Start Commands
echo "📋 Quick Start Commands"
echo "----------------------"
echo "For fastest setup, run these commands:"
echo ""
echo "1. Start MongoDB with Docker Compose:"
echo "   docker-compose up -d"
echo ""
echo "2. Start your FastAPI server:"
echo "   python main.py"
echo ""
echo "3. Test the API:"
echo "   python test_fix.py"
echo ""

# Connection Information
echo "📋 Connection Information"
echo "------------------------"
echo "MongoDB URL: mongodb://admin:adminpassword@localhost:27017/"
echo "Database: DHT_ENDPOINT"
echo "Port: 27017"
echo ""
echo "If using Docker Compose:"
echo "MongoDB Express: http://localhost:8081"
echo "API Server: http://localhost:8000"
echo "API Docs: http://localhost:8000/docs"
