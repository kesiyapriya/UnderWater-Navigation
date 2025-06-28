#!/bin/bash

echo "🐳 Starting MongoDB for Underwater Navigation API"
echo "================================================="

# Check if Docker is running
if ! sudo  docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Create a named volume for persistent data
echo "📁 Creating named volume for persistent data..."
sudo docker volume create mongodb_underwater_data

# Stop and remove existing container if it exists
echo "🔄 Stopping existing MongoDB container..."
sudo docker stop underwater_mongodb 2>/dev/null || true
sudo docker rm underwater_mongodb 2>/dev/null || true

# Start MongoDB container
echo "🚀 Starting MongoDB container..."
sudo docker run -d \
  --name underwater_mongodb \
  -p 27017:27017 \
  -e MONGO_INITDB_ROOT_USERNAME=admin \
  -e MONGO_INITDB_ROOT_PASSWORD=adminpassword \
  -e MONGO_INITDB_DATABASE=DHT_ENDPOINT \
  -v mongodb_underwater_data:/data/db \
  --restart=always \
  mongo:7.0

# Wait for MongoDB to start
echo "⏳ Waiting for MongoDB to start..."
sleep 10

# Check if container is running
if sudo docker ps | grep -q underwater_mongodb; then
    echo "✅ MongoDB container started successfully!"
    echo ""
    echo "📊 Connection Details:"
    echo "   Host: localhost"
    echo "   Port: 27017"
    echo "   Username: admin"
    echo "   Password: adminpassword"
    echo "   Database: DHT_ENDPOINT"
    echo ""
    echo "🔗 Connection URL:"
    echo "   mongodb://admin:adminpassword@localhost:27017/"
    echo ""
    echo "🔧 Useful Commands:"
    echo "   View logs: docker logs underwater_mongodb"
    echo "   Stop: docker stop underwater_mongodb"
    echo "   Connect: docker exec -it underwater_mongodb mongosh --username admin --password adminpassword"
    echo ""
    echo "🚀 Now you can start your FastAPI server:"
    echo "   python main.py"
else
    echo "❌ Failed to start MongoDB container"
    echo "Check logs with: docker logs underwater_mongodb"
    exit 1
fi
