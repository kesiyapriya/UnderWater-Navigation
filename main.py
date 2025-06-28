from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime
import json
import uvicorn
from motor.motor_asyncio import AsyncIOMotorClient
import os
from database import db_config, COLLECTIONS
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🔄 Connecting to MongoDB...")
    await db_config.connect_to_mongo()
    yield
    # Shutdown
    print("🔄 Closing MongoDB connection...")
    await db_config.close_mongo_connection()

app = FastAPI(
    title="Underwater Navigation Data Collection API",
    description="API server for collecting sensor data from underwater navigation and mapping systems",
    version="1.0.0",
    lifespan=lifespan
)

# Data models for different types of sensor data
class DHTSensorData(BaseModel):
    sensor_id: str
    temperature: float
    humidity: float
    timestamp: Optional[datetime] = None
    location: Optional[Dict[str, float]] = None  # {"lat": x, "lon": y, "depth": z}

class NavigationData(BaseModel):
    device_id: str
    position: Dict[str, float]  # {"x": x, "y": y, "z": z}
    orientation: Dict[str, float]  # {"roll": x, "pitch": y, "yaw": z}
    velocity: Optional[Dict[str, float]] = None
    timestamp: Optional[datetime] = None

class MappingData(BaseModel):
    sensor_id: str
    scan_data: List[Dict[str, Any]]  # Sonar/LiDAR data points
    timestamp: Optional[datetime] = None
    position: Optional[Dict[str, float]] = None

class GeneralSensorData(BaseModel):
    sensor_type: str
    sensor_id: str
    data: Dict[str, Any]
    timestamp: Optional[datetime] = None
    metadata: Optional[Dict[str, Any]] = None

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Underwater Navigation Data Collection API",
        "status": "active",
        "endpoints": [
            "/dht-sensor",
            "/navigation",
            "/mapping",
            "/general-sensor",
            "/health"
        ]
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now()}

# DHT Sensor data endpoint
@app.post("/dht-sensor")
async def receive_dht_data(dht_data: DHTSensorData):
    """
    Endpoint to receive DHT sensor data (temperature and humidity)
    """
    # Set timestamp if not provided
    if not dht_data.timestamp:
        dht_data.timestamp = datetime.now()
    
    print("\n" + "="*60)
    print("🌡️  DHT SENSOR DATA RECEIVED")
    print("="*60)
    print(f"Sensor ID: {dht_data.sensor_id}")
    print(f"Temperature: {dht_data.temperature}°C")
    print(f"Humidity: {dht_data.humidity}%")
    print(f"Timestamp: {dht_data.timestamp}")
    if dht_data.location:
        print(f"Location: {dht_data.location}")
    
    # Save to MongoDB
    try:
        collection = db_config.get_collection(COLLECTIONS["dht_sensor"])
        if collection is not None:
            document = dht_data.dict()
            result = await collection.insert_one(document)
            print(f"💾 Data saved to MongoDB with ID: {result.inserted_id}")
            print("="*60)
            
            return {
                "status": "success",
                "message": "DHT sensor data received and saved to database",
                "data_received": dht_data.dict(),
                "database_id": str(result.inserted_id)
            }
        else:
            print("❌ Database connection not available")
            print("="*60)
            return {
                "status": "partial_success",
                "message": "DHT sensor data received but not saved (database unavailable)",
                "data_received": dht_data.dict()
            }
    except Exception as e:
        print(f"❌ Error saving to database: {e}")
        print("="*60)
        return {
            "status": "error",
            "message": f"DHT sensor data received but database error: {str(e)}",
            "data_received": dht_data.dict()
        }

# Navigation data endpoint
@app.post("/navigation")
async def receive_navigation_data(nav_data: NavigationData):
    """
    Endpoint to receive navigation data (position, orientation, velocity)
    """
    # Set timestamp if not provided
    if not nav_data.timestamp:
        nav_data.timestamp = datetime.now()
    
    print("\n" + "="*60)
    print("🧭 NAVIGATION DATA RECEIVED")
    print("="*60)
    print(f"Device ID: {nav_data.device_id}")
    print(f"Position: {nav_data.position}")
    print(f"Orientation: {nav_data.orientation}")
    if nav_data.velocity:
        print(f"Velocity: {nav_data.velocity}")
    print(f"Timestamp: {nav_data.timestamp}")
    
    # Save to MongoDB
    try:
        collection = db_config.get_collection(COLLECTIONS["navigation"])
        if collection is not None:
            document = nav_data.dict()
            result = await collection.insert_one(document)
            print(f"💾 Data saved to MongoDB with ID: {result.inserted_id}")
            print("="*60)
            
            return {
                "status": "success",
                "message": "Navigation data received and saved to database",
                "data_received": nav_data.dict(),
                "database_id": str(result.inserted_id)
            }
        else:
            print("❌ Database connection not available")
            print("="*60)
            return {
                "status": "partial_success",
                "message": "Navigation data received but not saved (database unavailable)",
                "data_received": nav_data.dict()
            }
    except Exception as e:
        print(f"❌ Error saving to database: {e}")
        print("="*60)
        return {
            "status": "error",
            "message": f"Navigation data received but database error: {str(e)}",
            "data_received": nav_data.dict()
        }

# Mapping data endpoint
@app.post("/mapping")
async def receive_mapping_data(mapping_data: MappingData):
    """
    Endpoint to receive mapping/sonar data
    """
    # Set timestamp if not provided
    if not mapping_data.timestamp:
        mapping_data.timestamp = datetime.now()
    
    print("\n" + "="*60)
    print("🗺️  MAPPING DATA RECEIVED")
    print("="*60)
    print(f"Sensor ID: {mapping_data.sensor_id}")
    print(f"Number of scan points: {len(mapping_data.scan_data)}")
    print(f"Timestamp: {mapping_data.timestamp}")
    if mapping_data.position:
        print(f"Sensor Position: {mapping_data.position}")
    print("Sample scan data (first 3 points):")
    for i, point in enumerate(mapping_data.scan_data[:3]):
        print(f"  Point {i+1}: {point}")
    
    # Save to MongoDB
    try:
        collection = db_config.get_collection(COLLECTIONS["mapping"])
        if collection is not None:
            document = mapping_data.dict()
            result = await collection.insert_one(document)
            print(f"💾 Data saved to MongoDB with ID: {result.inserted_id}")
            print("="*60)
            
            return {
                "status": "success",
                "message": "Mapping data received and saved to database",
                "data_received": {
                    "sensor_id": mapping_data.sensor_id,
                    "scan_points_count": len(mapping_data.scan_data),
                    "timestamp": mapping_data.timestamp
                },
                "database_id": str(result.inserted_id)
            }
        else:
            print("❌ Database connection not available")
            print("="*60)
            return {
                "status": "partial_success",
                "message": "Mapping data received but not saved (database unavailable)",
                "data_received": {
                    "sensor_id": mapping_data.sensor_id,
                    "scan_points_count": len(mapping_data.scan_data),
                    "timestamp": mapping_data.timestamp
                }
            }
    except Exception as e:
        print(f"❌ Error saving to database: {e}")
        print("="*60)
        return {
            "status": "error",
            "message": f"Mapping data received but database error: {str(e)}",
            "data_received": {
                "sensor_id": mapping_data.sensor_id,
                "scan_points_count": len(mapping_data.scan_data),
                "timestamp": mapping_data.timestamp
            }
        }

# General sensor data endpoint
@app.post("/general-sensor")
async def receive_general_sensor_data(sensor_data: GeneralSensorData):
    """
    Endpoint to receive any general sensor data
    """
    # Set timestamp if not provided
    if not sensor_data.timestamp:
        sensor_data.timestamp = datetime.now()
    
    print("\n" + "="*60)
    print("📊 GENERAL SENSOR DATA RECEIVED")
    print("="*60)
    print(f"Sensor Type: {sensor_data.sensor_type}")
    print(f"Sensor ID: {sensor_data.sensor_id}")
    print(f"Data: {json.dumps(sensor_data.data, indent=2)}")
    print(f"Timestamp: {sensor_data.timestamp}")
    if sensor_data.metadata:
        print(f"Metadata: {json.dumps(sensor_data.metadata, indent=2)}")
    
    # Save to MongoDB
    try:
        collection = db_config.get_collection(COLLECTIONS["general_sensor"])
        if collection is not None:
            document = sensor_data.dict()
            result = await collection.insert_one(document)
            print(f"💾 Data saved to MongoDB with ID: {result.inserted_id}")
            print("="*60)
            
            return {
                "status": "success",
                "message": "General sensor data received and saved to database",
                "data_received": sensor_data.dict(),
                "database_id": str(result.inserted_id)
            }
        else:
            print("❌ Database connection not available")
            print("="*60)
            return {
                "status": "partial_success",
                "message": "General sensor data received but not saved (database unavailable)",
                "data_received": sensor_data.dict()
            }
    except Exception as e:
        print(f"❌ Error saving to database: {e}")
        print("="*60)
        return {
            "status": "error",
            "message": f"General sensor data received but database error: {str(e)}",
            "data_received": sensor_data.dict()
        }

# Batch data endpoint for multiple sensors
@app.post("/batch-data")
async def receive_batch_data(batch_data: List[Dict[str, Any]]):
    """
    Endpoint to receive batch data from multiple sensors
    """
    current_time = datetime.now()
    
    print("\n" + "="*60)
    print("📦 BATCH DATA RECEIVED")
    print("="*60)
    print(f"Number of data points: {len(batch_data)}")
    print(f"Timestamp: {current_time}")
    
    for i, data_point in enumerate(batch_data):
        print(f"\nData Point {i+1}:")
        print(json.dumps(data_point, indent=2))
    
    # Save to MongoDB
    try:
        collection = db_config.get_collection(COLLECTIONS["batch_data"])
        if collection is not None:
            # Add timestamp to batch document
            batch_document = {
                "batch_timestamp": current_time,
                "batch_size": len(batch_data),
                "data_points": batch_data
            }
            result = await collection.insert_one(batch_document)
            print(f"💾 Batch data saved to MongoDB with ID: {result.inserted_id}")
            print("="*60)
            
            return {
                "status": "success",
                "message": f"Batch data received and saved to database ({len(batch_data)} points)",
                "data_points_count": len(batch_data),
                "database_id": str(result.inserted_id)
            }
        else:
            print("❌ Database connection not available")
            print("="*60)
            return {
                "status": "partial_success",
                "message": f"Batch data received but not saved (database unavailable) ({len(batch_data)} points)",
                "data_points_count": len(batch_data)
            }
    except Exception as e:
        print(f"❌ Error saving to database: {e}")
        print("="*60)
        return {
            "status": "error",
            "message": f"Batch data received but database error: {str(e)} ({len(batch_data)} points)",
            "data_points_count": len(batch_data)
        }

# Database query endpoints
@app.get("/data/dht-sensor")
async def get_dht_sensor_data(limit: int = 10, sensor_id: Optional[str] = None):
    """Get DHT sensor data from database"""
    try:
        collection = db_config.get_collection(COLLECTIONS["dht_sensor"])
        if collection is None:
            raise HTTPException(status_code=503, detail="Database not available")
        
        query = {}
        if sensor_id:
            query["sensor_id"] = sensor_id
            
        cursor = collection.find(query).sort("timestamp", -1).limit(limit)
        documents = await cursor.to_list(length=limit)
        
        # Convert ObjectId to string
        for doc in documents:
            doc["_id"] = str(doc["_id"])
            
        return {
            "status": "success",
            "count": len(documents),
            "data": documents
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/data/navigation")
async def get_navigation_data(limit: int = 10, device_id: Optional[str] = None):
    """Get navigation data from database"""
    try:
        collection = db_config.get_collection(COLLECTIONS["navigation"])
        if collection is None:
            raise HTTPException(status_code=503, detail="Database not available")
        
        query = {}
        if device_id:
            query["device_id"] = device_id
            
        cursor = collection.find(query).sort("timestamp", -1).limit(limit)
        documents = await cursor.to_list(length=limit)
        
        # Convert ObjectId to string
        for doc in documents:
            doc["_id"] = str(doc["_id"])
            
        return {
            "status": "success",
            "count": len(documents),
            "data": documents
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/data/mapping")
async def get_mapping_data(limit: int = 10, sensor_id: Optional[str] = None):
    """Get mapping data from database"""
    try:
        collection = db_config.get_collection(COLLECTIONS["mapping"])
        if collection is None:
            raise HTTPException(status_code=503, detail="Database not available")
        
        query = {}
        if sensor_id:
            query["sensor_id"] = sensor_id
            
        cursor = collection.find(query).sort("timestamp", -1).limit(limit)
        documents = await cursor.to_list(length=limit)
        
        # Convert ObjectId to string
        for doc in documents:
            doc["_id"] = str(doc["_id"])
            
        return {
            "status": "success",
            "count": len(documents),
            "data": documents
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/data/stats")
async def get_database_stats():
    """Get database statistics"""
    try:
        stats = {}
        for collection_key, collection_name in COLLECTIONS.items():
            collection = db_config.get_collection(collection_name)
            if collection is not None:
                count = await collection.count_documents({})
                stats[collection_key] = count
            else:
                stats[collection_key] = "unavailable"
        
        return {
            "status": "success",
            "database": "underwater_navigation",
            "collections": stats
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

if __name__ == "__main__":
    print("🚀 Starting Underwater Navigation Data Collection API Server...")
    print("📡 Ready to receive sensor data from your underwater navigation system!")
    print("🌐 Server will be available at: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("🔧 Interactive API: http://localhost:8000/redoc")
    print("\nPress Ctrl+C to stop the server\n")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
