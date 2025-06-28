#!/bin/bash

echo "🐳 MongoDB Docker Commands for Underwater Navigation API"
echo "========================================================"

echo ""
echo "📋 Available Commands:"
echo "---------------------"
echo "1. Start MongoDB with Docker Compose (Recommended)"
echo "2. Start MongoDB with Docker Run"
echo "3. Start specific services"
echo "4. View logs"
echo "5. Stop services"
echo ""

case "$1" in
    "compose-up")
        echo "🚀 Starting MongoDB with Docker Compose..."
        echo "This will start MongoDB with persistent storage"
        echo ""
        docker-compose up -d
        echo ""
        echo "✅ Services started!"
        echo "📊 MongoDB: http://localhost:27017"
        echo "🗄️  MongoDB Express: http://localhost:8081"
        ;;
    
    "docker-run")
        echo "🚀 Starting MongoDB with Docker Run..."
        echo "Creating volume for persistent storage..."
        
        # Create a named volume for MongoDB data
        docker volume create mongodb_data
        
        # Run MongoDB container
        docker run -d \
          --name underwater_navigation_mongodb \
          -p 27017:27017 \
          -e MONGO_INITDB_ROOT_USERNAME=admin \
          -e MONGO_INITDB_ROOT_PASSWORD=underwater_nav_2025 \
          -e MONGO_INITDB_DATABASE=underwater_navigation \
          -v mongodb_data:/data/db \
          -v mongodb_config:/data/configdb \
          --restart=always \
          mongo:7.0
        
        echo ""
        echo "✅ MongoDB container started!"
        echo "📊 MongoDB available at: mongodb://admin:underwater_nav_2025@localhost:27017/"
        ;;
    
    "mongo-only")
        echo "🚀 Starting only MongoDB container..."
        docker-compose up -d mongodb
        ;;
    
    "mongo-express")
        echo "🚀 Starting MongoDB Express..."
        docker-compose up -d mongo-express
        echo "🗄️  MongoDB Express: http://localhost:8081"
        ;;
    
    "logs")
        echo "📄 Showing MongoDB logs..."
        docker logs underwater_navigation_mongodb -f
        ;;
    
    "logs-compose")
        echo "📄 Showing Docker Compose logs..."
        docker-compose logs -f
        ;;
    
    "stop")
        echo "🛑 Stopping all services..."
        docker-compose down
        ;;
    
    "stop-docker")
        echo "🛑 Stopping Docker containers..."
        docker stop underwater_navigation_mongodb
        docker rm underwater_navigation_mongodb
        ;;
    
    "status")
        echo "📋 Container Status:"
        echo "-------------------"
        docker ps | grep -E "(underwater_navigation|mongo)"
        echo ""
        echo "📊 Volume Status:"
        echo "----------------"
        docker volume ls | grep -E "(mongodb|underwater)"
        ;;
    
    "clean")
        echo "🧹 Cleaning up all containers and volumes..."
        echo "⚠️  This will DELETE ALL DATA!"
        read -p "Are you sure? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            docker-compose down -v
            docker volume rm mongodb_data mongodb_config 2>/dev/null || true
            echo "✅ Cleanup completed!"
        else
            echo "❌ Cleanup cancelled"
        fi
        ;;
    
    "connect")
        echo "🔌 Connecting to MongoDB shell..."
        docker exec -it underwater_navigation_mongodb mongosh \
          --username admin \
          --password underwater_nav_2025 \
          --authenticationDatabase admin \
          underwater_navigation
        ;;
    
    *)
        echo "Usage: $0 {command}"
        echo ""
        echo "🐳 Docker Commands:"
        echo "  compose-up    - Start with Docker Compose (recommended)"
        echo "  docker-run    - Start with Docker Run command"
        echo "  mongo-only    - Start only MongoDB"
        echo "  mongo-express - Start only MongoDB Express"
        echo ""
        echo "📋 Management:"
        echo "  status        - Show container status"
        echo "  logs          - Show MongoDB logs"
        echo "  logs-compose  - Show all service logs"
        echo "  stop          - Stop all services"
        echo "  clean         - Clean up everything (deletes data!)"
        echo ""
        echo "🔧 Utilities:"
        echo "  connect       - Connect to MongoDB shell"
        echo ""
        echo "📚 Examples:"
        echo "  $0 compose-up     # Start everything"
        echo "  $0 status         # Check if running"
        echo "  $0 logs           # View MongoDB logs"
        echo "  $0 connect        # Connect to database"
        echo "  $0 stop           # Stop everything"
        echo ""
        echo "🌊 After starting MongoDB, run your FastAPI server:"
        echo "  python main.py"
        ;;
esac
