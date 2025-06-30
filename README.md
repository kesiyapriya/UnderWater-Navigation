# Underwater Navigation Data Collection API

A production-ready, containerized FastAPI server for collecting and storing sensor data from underwater navigation and mapping systems.

## Features
- Collects DHT sensor, navigation, mapping, and general sensor data
- Stores data in MongoDB with proper indexing
- RESTful API with FastAPI and async MongoDB (Motor)
- Dockerized for easy deployment
- Health checks and logging
- MongoDB Express UI for database management (optional)

## Project Structure
```
.
├── main.py                # FastAPI application
├── database.py            # MongoDB connection logic
├── requirements.txt       # Python dependencies
├── Dockerfile             # API server container build
├── docker-compose.yml     # Multi-service orchestration
├── mongo-init/            # MongoDB init scripts
├── test_api.py            # API endpoint tests
├── test_mongodb.py        # MongoDB connection tests
└── ...
```

## Quick Start (Recommended)

### 1. Clone the repository
```bash
git clone https://github.com/kesiyapriya/UnderWater-Navigation.git
cd UnderWater-Navigation
```

### 2. Build and start all services
```bash
docker-compose up -d
```

### 3. Check service status
```bash
docker-compose ps
```

### 4. Access the services
- **API Server:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs
- **MongoDB Express:** http://localhost:8081 (optional)

### 5. View logs
```bash
docker-compose logs -f api-server
```

## API Endpoints
- `POST /dht-sensor` — DHT sensor data
- `POST /navigation` — Navigation data
- `POST /mapping` — Mapping/sonar data
- `POST /general-sensor` — General sensor data
- `POST /batch-data` — Batch data from multiple sensors
- `GET /data/dht-sensor` — Get DHT sensor data
- `GET /data/navigation` — Get navigation data
- `GET /data/mapping` — Get mapping data
- `GET /data/stats` — Database statistics
- `GET /health` — Health check

## Configuration
- Edit environment variables in `docker-compose.yml` or create a `.env` file (see `.env.example`)
- Default MongoDB credentials are for local development. **Change them for production!**

## Local Development (without Docker)
```bash
# Install dependencies
pip install -r requirements.txt

# Start MongoDB (if not running)
docker-compose up -d mongodb

# Start API server
python main.py
```

## Testing
```bash
python test_api.py
python test_mongodb.py
```

## Production Deployment
- Use `docker-compose up -d` for easy deployment
- For Kubernetes, convert `docker-compose.yml` using Kompose or write manifests
- For Docker Swarm: `docker stack deploy -c docker-compose.yml underwater-nav`

## Security Notes
- Change all default passwords before deploying to production
- Use HTTPS and secure your MongoDB instance
- Restrict network access as needed

## License
[Your License Here]
