#!/bin/bash

echo "🌊 Underwater Navigation API with MongoDB Setup"
echo "=============================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to check if Docker is running
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        echo -e "${RED}❌ Docker is not running. Please start Docker first.${NC}"
        exit 1
    fi
}

# Function to check if docker-compose is available
check_docker_compose() {
    if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null 2>&1; then
        echo -e "${RED}❌ docker-compose is not available. Please install docker-compose.${NC}"
        exit 1
    fi
}

# Function to start MongoDB
start_mongodb() {
    echo -e "${BLUE}🐳 Starting MongoDB with Docker Compose...${NC}"
    
    # Use docker compose or docker-compose depending on what's available
    if docker compose version &> /dev/null 2>&1; then
        DOCKER_COMPOSE_CMD="docker compose"
    else
        DOCKER_COMPOSE_CMD="docker-compose"
    fi
    
    $DOCKER_COMPOSE_CMD up -d
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ MongoDB container started successfully!${NC}"
        echo -e "${YELLOW}🔄 Waiting for MongoDB to be ready...${NC}"
        sleep 10
        
        # Check if MongoDB is responding
        for i in {1..30}; do
            if docker exec underwater_navigation_mongodb mongosh --eval "db.adminCommand('ping')" > /dev/null 2>&1; then
                echo -e "${GREEN}✅ MongoDB is ready!${NC}"
                break
            fi
            echo -e "${YELLOW}⏳ Waiting for MongoDB... ($i/30)${NC}"
            sleep 2
        done
    else
        echo -e "${RED}❌ Failed to start MongoDB container${NC}"
        exit 1
    fi
}

# Function to install Python dependencies
install_dependencies() {
    echo -e "${BLUE}📦 Installing Python dependencies...${NC}"
    pip install -r requirements.txt
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Dependencies installed successfully!${NC}"
    else
        echo -e "${RED}❌ Failed to install dependencies${NC}"
        exit 1
    fi
}

# Function to start the API server
start_api_server() {
    echo -e "${BLUE}🚀 Starting FastAPI server...${NC}"
    echo -e "${GREEN}Server will be available at: http://localhost:8000${NC}"
    echo -e "${GREEN}API Documentation: http://localhost:8000/docs${NC}"
    echo -e "${GREEN}MongoDB Express: http://localhost:8081${NC}"
    echo ""
    echo -e "${YELLOW}Press Ctrl+C to stop the server${NC}"
    echo ""
    
    python main.py
}

# Function to show status
show_status() {
    echo -e "${BLUE}📋 System Status:${NC}"
    echo "----------------"
    
    # Check MongoDB container
    if docker ps | grep -q underwater_navigation_mongodb; then
        echo -e "${GREEN}✅ MongoDB: Running${NC}"
    else
        echo -e "${RED}❌ MongoDB: Not running${NC}"
    fi
    
    # Check MongoDB Express
    if docker ps | grep -q underwater_navigation_mongo_express; then
        echo -e "${GREEN}✅ MongoDB Express: Running${NC}"
    else
        echo -e "${RED}❌ MongoDB Express: Not running${NC}"
    fi
    
    echo ""
    echo -e "${BLUE}🔗 Available URLs:${NC}"
    echo "   API Server: http://localhost:8000"
    echo "   API Docs: http://localhost:8000/docs"
    echo "   MongoDB Express: http://localhost:8081"
}

# Function to stop services
stop_services() {
    echo -e "${YELLOW}🛑 Stopping services...${NC}"
    
    # Use docker compose or docker-compose depending on what's available
    if docker compose version &> /dev/null 2>&1; then
        docker compose down
    else
        docker-compose down
    fi
    
    echo -e "${GREEN}✅ Services stopped${NC}"
}

# Function to show logs
show_logs() {
    echo -e "${BLUE}📄 Showing MongoDB logs...${NC}"
    docker logs underwater_navigation_mongodb
}

# Main script logic
case "$1" in
    "start")
        check_docker
        check_docker_compose
        start_mongodb
        install_dependencies
        start_api_server
        ;;
    "stop")
        stop_services
        ;;
    "status")
        show_status
        ;;
    "logs")
        show_logs
        ;;
    "test")
        echo -e "${BLUE}🧪 Running API tests...${NC}"
        python test_mongodb.py
        ;;
    *)
        echo "🌊 Underwater Navigation API Manager"
        echo ""
        echo "Usage: $0 {start|stop|status|logs|test}"
        echo ""
        echo "Commands:"
        echo "  start   - Start MongoDB and API server"
        echo "  stop    - Stop all services"
        echo "  status  - Show service status"
        echo "  logs    - Show MongoDB logs"
        echo "  test    - Run API tests"
        echo ""
        echo "Examples:"
        echo "  $0 start    # Start everything"
        echo "  $0 test     # Test the API"
        echo "  $0 stop     # Stop all services"
        ;;
esac
