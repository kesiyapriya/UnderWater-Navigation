// MongoDB initialization script for underwater navigation database
db = db.getSiblingDB('underwater_navigation');

// Create collections for different data types
db.createCollection('dht_sensor_data');
db.createCollection('navigation_data');
db.createCollection('mapping_data');
db.createCollection('general_sensor_data');
db.createCollection('batch_data');

// Create indexes for better performance
db.dht_sensor_data.createIndex({ "sensor_id": 1, "timestamp": -1 });
db.navigation_data.createIndex({ "device_id": 1, "timestamp": -1 });
db.mapping_data.createIndex({ "sensor_id": 1, "timestamp": -1 });
db.general_sensor_data.createIndex({ "sensor_type": 1, "sensor_id": 1, "timestamp": -1 });
db.batch_data.createIndex({ "timestamp": -1 });

// Create a user for the application
db.createUser({
  user: "underwater_nav_user",
  pwd: "nav_user_2025",
  roles: [
    {
      role: "readWrite",
      db: "underwater_navigation"
    }
  ]
});

print("Database initialization completed for underwater navigation system!");
