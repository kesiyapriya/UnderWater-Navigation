// MongoDB initialization script for underwater navigation database
print('Creating underwater navigation database and collections...');

// Switch to the underwater_navigation database
db = db.getSiblingDB('underwater_navigation');

// Create collections for different data types
db.createCollection('dht_sensor_data');
db.createCollection('navigation_data');
db.createCollection('mapping_data');
db.createCollection('general_sensor_data');
db.createCollection('batch_data');

// Create indexes for better query performance
db.dht_sensor_data.createIndex({ "sensor_id": 1, "timestamp": -1 });
db.dht_sensor_data.createIndex({ "timestamp": -1 });
db.dht_sensor_data.createIndex({ "location.lat": 1, "location.lon": 1 });

db.navigation_data.createIndex({ "device_id": 1, "timestamp": -1 });
db.navigation_data.createIndex({ "timestamp": -1 });

db.mapping_data.createIndex({ "sensor_id": 1, "timestamp": -1 });
db.mapping_data.createIndex({ "timestamp": -1 });

db.general_sensor_data.createIndex({ "sensor_type": 1, "sensor_id": 1, "timestamp": -1 });
db.general_sensor_data.createIndex({ "timestamp": -1 });

db.batch_data.createIndex({ "timestamp": -1 });

print('Database and collections created successfully!');
print('Collections: ' + db.getCollectionNames().join(', '));
