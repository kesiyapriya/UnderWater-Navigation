import logging
import os
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Optional, Dict, Any, List

import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from database import db_config, COLLECTIONS

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting up - connecting to MongoDB...")
    await db_config.connect_to_mongo()
    yield
    # Shutdown
    logger.info("Shutting down - closing MongoDB connection...")
    await db_config.close_mongo_connection()

app = FastAPI(
    title="Underwater Navigation Data Collection API",
    description="API server for collecting sensor data from underwater navigation and mapping systems",
    version="1.0.0",
    lifespan=lifespan
)

# Data models
class DHTSensorData(BaseModel):
    sensor_id: str
    temperature: float
    humidity: float
    timestamp: Optional[datetime] = None
    location: Optional[Dict[str, float]] = None

class NavigationData(BaseModel):
    device_id: str
    position: Dict[str, float]
    orientation: Dict[str, float]
    velocity: Optional[Dict[str, float]] = None
    timestamp: Optional[datetime] = None

class MappingData(BaseModel):
    sensor_id: str
    scan_data: List[Dict[str, Any]]
    timestamp: Optional[datetime] = None
    position: Optional[Dict[str, float]] = None

class GeneralSensorData(BaseModel):
    sensor_type: str
    sensor_id: str
    data: Dict[str, Any]
    timestamp: Optional[datetime] = None
    metadata: Optional[Dict[str, Any]] = None

# Helper function to save data
async def save_to_database(collection_name: str, data: dict) -> dict:
    """Save data to MongoDB collection"""
    try:
        collection = db_config.get_collection(collection_name)
        if collection is None:
            return {"status": "partial_success", "message": "Database not available"}
        
        result = await collection.insert_one(data)
        logger.info(f"Data saved to {collection_name} with ID: {result.inserted_id}")
        return {
            "status": "success", 
            "message": "Data saved successfully",
            "database_id": str(result.inserted_id)
        }
    except Exception as e:
        logger.error(f"Database error in {collection_name}: {str(e)}")
        return {"status": "error", "message": "Database error occurred"}

@app.get("/")
async def root():
    return {
        "message": "Underwater Navigation Data Collection API",
        "status": "active",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy", 
        "timestamp": datetime.now(),
        "database_connected": db_config.is_connected
    }

@app.post("/dht-sensor")
async def receive_dht_data(dht_data: DHTSensorData):
    """Receive DHT sensor data (temperature and humidity)"""
    if not dht_data.timestamp:
        dht_data.timestamp = datetime.now()
    
    logger.info(f"DHT data received from sensor: {dht_data.sensor_id}")
    
    # Save to database
    save_result = await save_to_database(COLLECTIONS["dht_sensor"], dht_data.model_dump())
    
    return {
        **save_result,
        "data_type": "dht_sensor",
        "sensor_id": dht_data.sensor_id,
        "timestamp": dht_data.timestamp
    }

@app.post("/navigation")
async def receive_navigation_data(nav_data: NavigationData):
    """Receive navigation data (position, orientation, velocity)"""
    if not nav_data.timestamp:
        nav_data.timestamp = datetime.now()
    
    logger.info(f"Navigation data received from device: {nav_data.device_id}")
    
    # Save to database
    save_result = await save_to_database(COLLECTIONS["navigation"], nav_data.model_dump())
    
    return {
        **save_result,
        "data_type": "navigation",
        "device_id": nav_data.device_id,
        "timestamp": nav_data.timestamp
    }

@app.post("/mapping")
async def receive_mapping_data(mapping_data: MappingData):
    """Receive mapping/sonar data"""
    if not mapping_data.timestamp:
        mapping_data.timestamp = datetime.now()
    
    logger.info(f"Mapping data received from sensor: {mapping_data.sensor_id}, points: {len(mapping_data.scan_data)}")
    
    # Save to database
    save_result = await save_to_database(COLLECTIONS["mapping"], mapping_data.model_dump())
    
    return {
        **save_result,
        "data_type": "mapping",
        "sensor_id": mapping_data.sensor_id,
        "scan_points": len(mapping_data.scan_data),
        "timestamp": mapping_data.timestamp
    }

@app.post("/general-sensor")
async def receive_general_sensor_data(sensor_data: GeneralSensorData):
    """Receive any general sensor data"""
    if not sensor_data.timestamp:
        sensor_data.timestamp = datetime.now()
    
    logger.info(f"General sensor data received: {sensor_data.sensor_type} from {sensor_data.sensor_id}")
    
    # Save to database
    save_result = await save_to_database(COLLECTIONS["general_sensor"], sensor_data.model_dump())
    
    return {
        **save_result,
        "data_type": "general_sensor",
        "sensor_type": sensor_data.sensor_type,
        "sensor_id": sensor_data.sensor_id,
        "timestamp": sensor_data.timestamp
    }

@app.post("/batch-data")
async def receive_batch_data(batch_data: List[Dict[str, Any]]):
    """Receive batch data from multiple sensors"""
    current_time = datetime.now()
    
    logger.info(f"Batch data received with {len(batch_data)} points")
    
    # Save to database
    batch_document = {
        "batch_timestamp": current_time,
        "batch_size": len(batch_data),
        "data_points": batch_data
    }
    
    save_result = await save_to_database(COLLECTIONS["batch_data"], batch_document)
    
    return {
        **save_result,
        "data_type": "batch_data",
        "batch_size": len(batch_data),
        "timestamp": current_time
    }

# Data retrieval endpoints
@app.get("/data/dht-sensor")
async def get_dht_sensor_data(limit: int = 10, sensor_id: Optional[str] = None):
    """Get DHT sensor data from database"""
    try:
        collection = db_config.get_collection(COLLECTIONS["dht_sensor"])
        if collection is None:
            raise HTTPException(status_code=503, detail="Database not available")
        
        query = {"sensor_id": sensor_id} if sensor_id else {}
        cursor = collection.find(query).sort("timestamp", -1).limit(limit)
        documents = await cursor.to_list(length=limit)
        
        # Convert ObjectId to string
        for doc in documents:
            doc["_id"] = str(doc["_id"])
            
        return {"status": "success", "count": len(documents), "data": documents}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Database error")

@app.get("/data/navigation")
async def get_navigation_data(limit: int = 10, device_id: Optional[str] = None):
    """Get navigation data from database"""
    try:
        collection = db_config.get_collection(COLLECTIONS["navigation"])
        if collection is None:
            raise HTTPException(status_code=503, detail="Database not available")
        
        query = {"device_id": device_id} if device_id else {}
        cursor = collection.find(query).sort("timestamp", -1).limit(limit)
        documents = await cursor.to_list(length=limit)
        
        for doc in documents:
            doc["_id"] = str(doc["_id"])
            
        return {"status": "success", "count": len(documents), "data": documents}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Database error")

@app.get("/data/mapping")
async def get_mapping_data(limit: int = 10, sensor_id: Optional[str] = None):
    """Get mapping data from database"""
    try:
        collection = db_config.get_collection(COLLECTIONS["mapping"])
        if collection is None:
            raise HTTPException(status_code=503, detail="Database not available")
        
        query = {"sensor_id": sensor_id} if sensor_id else {}
        cursor = collection.find(query).sort("timestamp", -1).limit(limit)
        documents = await cursor.to_list(length=limit)
        
        for doc in documents:
            doc["_id"] = str(doc["_id"])
            
        return {"status": "success", "count": len(documents), "data": documents}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Database error")

@app.get("/data/stats")
async def get_database_stats():
    """Get database statistics"""
    try:
        if not db_config.is_connected:
            raise HTTPException(status_code=503, detail="Database not available")
            
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
        raise HTTPException(status_code=500, detail="Database error")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    
    logger.info(f"Starting server on {host}:{port}")
    uvicorn.run("main:app", host=host, port=port, reload=False)
