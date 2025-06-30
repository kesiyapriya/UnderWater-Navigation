import os
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure
import asyncio

class DatabaseConfig:
    def __init__(self):
        # MongoDB connection settings
        self.MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://admin:underwater_nav_2025@mongodb:27017/")
        self.DATABASE_NAME = os.getenv("DATABASE_NAME", "underwater_navigation")
        self.client = None
        self.database = None
        self.is_connected = False
        
    async def connect_to_mongo(self):
        """Create database connection"""
        try:
            self.client = AsyncIOMotorClient(self.MONGODB_URL, serverSelectionTimeoutMS=10000)
            # Test the connection
            await self.client.admin.command('ping')
            self.database = self.client[self.DATABASE_NAME]
            self.is_connected = True
            print("✅ Successfully connected to MongoDB!")
            return True
        except ConnectionFailure:
            print("⚠️  MongoDB connection failed")
            self.is_connected = False
            return False
        except Exception as e:
            print(f"⚠️  MongoDB connection error: {type(e).__name__}")
            self.is_connected = False
            return False
    
    async def close_mongo_connection(self):
        """Close database connection"""
        if self.client:
            self.client.close()
            print("📤 MongoDB connection closed")
    
    def get_collection(self, collection_name: str):
        """Get a specific collection"""
        if self.database is not None and self.is_connected:
            return self.database[collection_name]
        return None

# Global database instance
db_config = DatabaseConfig()

# Collection names
COLLECTIONS = {
    "dht_sensor": "dht_sensor_data",
    "navigation": "navigation_data", 
    "mapping": "mapping_data",
    "general_sensor": "general_sensor_data",
    "batch_data": "batch_data"
}