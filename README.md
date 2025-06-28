# Underwater Navigation Data Collection API with MongoDB

This FastAPI server with MongoDB integration is designed to collect and store sensor data from underwater navigation and mapping systems for the project "Advanced Autonomous Navigation and Mapping in Challenging Underwater Environments with Kubernetes Cluster and IoT Integration".

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Python 3.8+
- pip

### 1. Start the Complete System
```bash
./manage.sh start
```

This will:
- Start MongoDB container with persistent storage
- Start MongoDB Express (web interface)
- Install Python dependencies
- Start the FastAPI server

### 2. Test the API
```bash
./manage.sh test
```

### 3. Check System Status
```bash
./manage.sh status
```

### 4. Stop All Services
```bash
./manage.sh stop
```

## 🗄️ Database Integration

### MongoDB Setup
- **Database**: `underwater_navigation`
- **Collections**:
  - `dht_sensor_data` - Temperature and humidity data
  - `navigation_data` - Position, orientation, velocity
  - `mapping_data` - Sonar/LiDAR scan data
  - `general_sensor_data` - Any sensor type
  - `batch_data` - Multiple sensor readings

### Data Persistence
- MongoDB data is stored in Docker volumes (`mongodb_data`)
- Data survives container restarts and recreations
- Automatic database initialization with indexes

## 📡 API Endpoints

### Data Collection Endpoints

#### DHT Sensor Data
- **POST** `/dht-sensor`
```json
{
  "sensor_id": "dht_underwater_001",
  "temperature": 18.5,
  "humidity": 85.3,
  "timestamp": "2025-06-19T10:30:00",
  "location": {
    "lat": 40.7128,
    "lon": -74.0060,
    "depth": -12.5
  }
}
```

#### Navigation Data
- **POST** `/navigation`
```json
{
  "device_id": "auv_navigator_001",
  "position": {"x": 150.7, "y": 230.4, "z": -18.2},
  "orientation": {"roll": 0.15, "pitch": -0.08, "yaw": 127.5},
  "velocity": {"vx": 2.1, "vy": 1.2, "vz": -0.3}
}
```

#### Mapping Data
- **POST** `/mapping`
```json
{
  "sensor_id": "sonar_multibeam_001",
  "scan_data": [
    {"distance": 25.8, "angle": 0, "intensity": 0.92, "quality": "high"},
    {"distance": 18.3, "angle": 15, "intensity": 0.87, "quality": "high"}
  ],
  "position": {"x": 150.7, "y": 230.4, "z": -18.2}
}
```

#### General Sensor Data
- **POST** `/general-sensor`
```json
{
  "sensor_type": "pressure_depth",
  "sensor_id": "pressure_001",
  "data": {
    "pressure": 2.85,
    "depth": 18.5,
    "temperature": 16.2
  },
  "metadata": {
    "calibration_date": "2025-06-01",
    "accuracy": "±0.1%"
  }
}
```

#### Batch Data
- **POST** `/batch-data`
```json
[
  {
    "sensor_type": "dht",
    "sensor_id": "dht_001",
    "temperature": 19.2,
    "humidity": 82.1
  },
  {
    "sensor_type": "pressure",
    "sensor_id": "pressure_002",
    "pressure": 3.12,
    "depth": 21.2
  }
]
```

### Data Retrieval Endpoints

#### Get DHT Sensor Data
- **GET** `/data/dht-sensor?limit=10&sensor_id=dht_001`

#### Get Navigation Data
- **GET** `/data/navigation?limit=10&device_id=nav_001`

#### Get Mapping Data
- **GET** `/data/mapping?limit=10&sensor_id=sonar_001`

#### Get Database Statistics
- **GET** `/data/stats`

## 🔧 System URLs

When running:
- **API Server**: `http://localhost:8000`
- **API Documentation**: `http://localhost:8000/docs`
- **Alternative Docs**: `http://localhost:8000/redoc`
- **MongoDB Express**: `http://localhost:8081`

## 🐳 Docker Services

### MongoDB
- **Port**: 27017
- **Username**: admin
- **Password**: underwater_nav_2025
- **Database**: underwater_navigation
- **Volume**: `mongodb_data` (persistent storage)

### MongoDB Express
- **Port**: 8081
- **No authentication required**
- **Direct access to database**

## 📊 Data Flow

1. **Data Collection**: Sensors send data to API endpoints
2. **Validation**: Pydantic models validate incoming data
3. **Processing**: Data is processed and timestamped
4. **Storage**: Data is stored in appropriate MongoDB collection
5. **Confirmation**: API returns success response with database ID
6. **Retrieval**: Data can be queried through GET endpoints

## 🧪 Testing

### Automated Testing
```bash
# Run comprehensive tests
./manage.sh test

# Or manually
python test_mongodb.py
```

### Manual Testing
```bash
# Test DHT sensor endpoint
curl -X POST "http://localhost:8000/dht-sensor" \
  -H "Content-Type: application/json" \
  -d '{
    "sensor_id": "dht_test_001",
    "temperature": 20.5,
    "humidity": 75.0
  }'

# Get stored data
curl "http://localhost:8000/data/dht-sensor?limit=5"
```

## 🔍 Monitoring

### Terminal Output
All received data is displayed in the server terminal with:
- Colored output for different data types
- Timestamps and sensor IDs
- Database storage confirmation
- Error handling and reporting

### Database Statistics
Check collection counts and database status:
```bash
curl "http://localhost:8000/data/stats"
```

## 🛠️ Development

### Project Structure
```
API_sever/
├── main.py              # FastAPI application
├── database.py          # MongoDB configuration
├── docker-compose.yml   # MongoDB services
├── requirements.txt     # Python dependencies
├── manage.sh           # Management script
├── test_mongodb.py     # Comprehensive tests
├── mongo-init/         # Database initialization
│   └── init-mongo.js   # MongoDB setup script
└── README.md           # This file
```

### Adding New Endpoints
1. Define Pydantic model in `main.py`
2. Create endpoint function with MongoDB integration
3. Add collection to `COLLECTIONS` in `database.py`
4. Update tests in `test_mongodb.py`

## 🔒 Security Notes

### Production Deployment
- Change default MongoDB passwords
- Enable MongoDB authentication
- Use environment variables for secrets
- Configure CORS properly
- Add rate limiting
- Enable HTTPS/TLS
- Implement API authentication

### Current Security
- MongoDB uses authentication
- Database initialization creates application user
- Docker network isolation
- Input validation via Pydantic

## 📈 Performance

### MongoDB Optimizations
- Indexes on commonly queried fields
- Compound indexes for complex queries
- Efficient document structure
- Connection pooling via Motor

### API Optimizations
- Async/await for database operations
- Non-blocking I/O operations
- Efficient JSON serialization
- Proper error handling

## 🔄 Backup and Recovery

### Manual Backup
```bash
# Backup database
docker exec underwater_navigation_mongodb mongodump --out /backup

# Restore database
docker exec underwater_navigation_mongodb mongorestore /backup
```

### Automated Backup
Consider implementing:
- Scheduled database dumps
- Off-site backup storage
- Point-in-time recovery
- Replica sets for high availability

## 🌊 Underwater Navigation Features

This system is specifically designed for underwater navigation with:
- **Multi-sensor support**: DHT, sonar, navigation, pressure sensors
- **Location tracking**: GPS coordinates with depth information
- **Real-time processing**: Immediate storage and confirmation
- **Batch processing**: Handle multiple sensor readings efficiently
- **Data persistence**: Never lose sensor data with MongoDB volumes
- **Scalability**: Ready for Kubernetes deployment
- **Monitoring**: Real-time terminal output and web interface
