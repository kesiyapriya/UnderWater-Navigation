import requests
import json
from datetime import datetime
import time

# Base URL of your API server
BASE_URL = "http://localhost:8000"

def test_dht_sensor():
    """Test DHT sensor data endpoint"""
    url = f"{BASE_URL}/dht-sensor"
    data = {
        "sensor_id": "dht_underwater_001",
        "temperature": 18.5,
        "humidity": 85.3,
        "timestamp": datetime.now().isoformat(),
        "location": {
            "lat": 40.7128,
            "lon": -74.0060,
            "depth": -12.5
        }
    }
    
    response = requests.post(url, json=data)
    print(f"DHT Sensor Response: {response.status_code} - {response.json()}")

def test_navigation_data():
    """Test navigation data endpoint"""
    url = f"{BASE_URL}/navigation"
    data = {
        "device_id": "auv_navigator_001",
        "position": {"x": 150.7, "y": 230.4, "z": -18.2},
        "orientation": {"roll": 0.15, "pitch": -0.08, "yaw": 127.5},
        "velocity": {"vx": 2.1, "vy": 1.2, "vz": -0.3},
        "timestamp": datetime.now().isoformat()
    }
    
    response = requests.post(url, json=data)
    print(f"Navigation Response: {response.status_code} - {response.json()}")

def test_mapping_data():
    """Test mapping data endpoint"""
    url = f"{BASE_URL}/mapping"
    data = {
        "sensor_id": "sonar_multibeam_001",
        "scan_data": [
            {"distance": 25.8, "angle": 0, "intensity": 0.92, "quality": "high"},
            {"distance": 18.3, "angle": 15, "intensity": 0.87, "quality": "high"},
            {"distance": 32.1, "angle": 30, "intensity": 0.65, "quality": "medium"},
            {"distance": 45.2, "angle": 45, "intensity": 0.43, "quality": "low"}
        ],
        "timestamp": datetime.now().isoformat(),
        "position": {"x": 150.7, "y": 230.4, "z": -18.2}
    }
    
    response = requests.post(url, json=data)
    print(f"Mapping Response: {response.status_code} - {response.json()}")

def test_general_sensor():
    """Test general sensor data endpoint"""
    url = f"{BASE_URL}/general-sensor"
    data = {
        "sensor_type": "pressure_depth",
        "sensor_id": "pressure_001",
        "data": {
            "pressure": 2.85,  # bar
            "depth": 18.5,     # meters
            "temperature": 16.2 # celsius
        },
        "timestamp": datetime.now().isoformat(),
        "metadata": {
            "calibration_date": "2025-06-01",
            "accuracy": "±0.1%",
            "sensor_model": "SeaBird SBE-39"
        }
    }
    
    response = requests.post(url, json=data)
    print(f"General Sensor Response: {response.status_code} - {response.json()}")

def test_batch_data():
    """Test batch data endpoint"""
    url = f"{BASE_URL}/batch-data"
    data = [
        {
            "sensor_type": "dht",
            "sensor_id": "dht_001",
            "temperature": 19.2,
            "humidity": 82.1,
            "timestamp": datetime.now().isoformat()
        },
        {
            "sensor_type": "pressure",
            "sensor_id": "pressure_002",
            "pressure": 3.12,
            "depth": 21.2,
            "timestamp": datetime.now().isoformat()
        },
        {
            "sensor_type": "imu",
            "sensor_id": "imu_001",
            "acceleration": {"x": 0.12, "y": -0.05, "z": 9.81},
            "gyroscope": {"x": 0.001, "y": 0.002, "z": -0.001},
            "timestamp": datetime.now().isoformat()
        }
    ]
    
    response = requests.post(url, json=data)
    print(f"Batch Data Response: {response.status_code} - {response.json()}")

def test_health_check():
    """Test health check endpoint"""
    url = f"{BASE_URL}/health"
    response = requests.get(url)
    print(f"Health Check Response: {response.status_code} - {response.json()}")

if __name__ == "__main__":
    print("🧪 Testing Underwater Navigation API Endpoints...")
    print("=" * 60)
    
    try:
        # Test health check first
        test_health_check()
        time.sleep(1)
        
        # Test DHT sensor data
        test_dht_sensor()
        time.sleep(1)
        
        # Test navigation data
        test_navigation_data()
        time.sleep(1)
        
        # Test mapping data
        test_mapping_data()
        time.sleep(1)
        
        # Test general sensor data
        test_general_sensor()
        time.sleep(1)
        
        # Test batch data
        test_batch_data()
        
        print("\n✅ All tests completed! Check your server terminal for the logged data.")
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to the API server.")
        print("Make sure the server is running on http://localhost:8000")
        print("Run: python main.py")
    except Exception as e:
        print(f"❌ Error occurred: {e}")
