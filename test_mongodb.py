import requests
import json
from datetime import datetime
import time
import sys

# Base URL of your API server
BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test health check endpoint"""
    try:
        url = f"{BASE_URL}/health"
        response = requests.get(url, timeout=5)
        print(f"🔍 Health Check Response: {response.status_code} - {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_database_stats():
    """Test database statistics endpoint"""
    try:
        url = f"{BASE_URL}/data/stats"
        response = requests.get(url, timeout=5)
        print(f"📊 Database Stats Response: {response.status_code}")
        if response.status_code == 200:
            stats = response.json()
            print(f"   Collections: {stats.get('collections', {})}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Database stats failed: {e}")
        return False

def test_dht_sensor():
    """Test DHT sensor data endpoint"""
    try:
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
        
        response = requests.post(url, json=data, timeout=10)
        print(f"🌡️  DHT Sensor Response: {response.status_code}")
        result = response.json()
        if 'database_id' in result:
            print(f"   Database ID: {result['database_id']}")
        print(f"   Status: {result.get('status', 'unknown')}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ DHT sensor test failed: {e}")
        return False

def test_navigation_data():
    """Test navigation data endpoint"""
    try:
        url = f"{BASE_URL}/navigation"
        data = {
            "device_id": "auv_navigator_001",
            "position": {"x": 150.7, "y": 230.4, "z": -18.2},
            "orientation": {"roll": 0.15, "pitch": -0.08, "yaw": 127.5},
            "velocity": {"vx": 2.1, "vy": 1.2, "vz": -0.3},
            "timestamp": datetime.now().isoformat()
        }
        
        response = requests.post(url, json=data, timeout=10)
        print(f"🧭 Navigation Response: {response.status_code}")
        result = response.json()
        if 'database_id' in result:
            print(f"   Database ID: {result['database_id']}")
        print(f"   Status: {result.get('status', 'unknown')}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Navigation test failed: {e}")
        return False

def test_mapping_data():
    """Test mapping data endpoint"""
    try:
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
        
        response = requests.post(url, json=data, timeout=10)
        print(f"🗺️  Mapping Response: {response.status_code}")
        result = response.json()
        if 'database_id' in result:
            print(f"   Database ID: {result['database_id']}")
        print(f"   Status: {result.get('status', 'unknown')}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Mapping test failed: {e}")
        return False

def test_general_sensor():
    """Test general sensor data endpoint"""
    try:
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
        
        response = requests.post(url, json=data, timeout=10)
        print(f"📊 General Sensor Response: {response.status_code}")
        result = response.json()
        if 'database_id' in result:
            print(f"   Database ID: {result['database_id']}")
        print(f"   Status: {result.get('status', 'unknown')}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ General sensor test failed: {e}")
        return False

def test_batch_data():
    """Test batch data endpoint"""
    try:
        url = f"{BASE_URL}/batch-data"
        data = [
            {
                "sensor_type": "dht",
                "sensor_id": "dht_002",
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
        
        response = requests.post(url, json=data, timeout=10)
        print(f"📦 Batch Data Response: {response.status_code}")
        result = response.json()
        if 'database_id' in result:
            print(f"   Database ID: {result['database_id']}")
        print(f"   Status: {result.get('status', 'unknown')}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Batch data test failed: {e}")
        return False

def test_data_retrieval():
    """Test data retrieval endpoints"""
    try:
        print("\n🔍 Testing Data Retrieval...")
        
        # Test DHT data retrieval
        url = f"{BASE_URL}/data/dht-sensor?limit=3"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"   DHT Records: {data.get('count', 0)}")
        
        # Test navigation data retrieval
        url = f"{BASE_URL}/data/navigation?limit=3"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"   Navigation Records: {data.get('count', 0)}")
        
        # Test mapping data retrieval
        url = f"{BASE_URL}/data/mapping?limit=3"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"   Mapping Records: {data.get('count', 0)}")
        
        return True
    except Exception as e:
        print(f"❌ Data retrieval test failed: {e}")
        return False

def main():
    print("🧪 Testing Underwater Navigation API with MongoDB...")
    print("=" * 60)
    
    # Check if server is running
    if not test_health_check():
        print("\n❌ Server is not running or not responding!")
        print("Please start the server first:")
        print("   docker-compose up -d")
        print("   python main.py")
        sys.exit(1)
    
    print("\n🔄 Testing Database Connection...")
    test_database_stats()
    
    time.sleep(1)
    
    tests = [
        ("DHT Sensor Data", test_dht_sensor),
        ("Navigation Data", test_navigation_data),
        ("Mapping Data", test_mapping_data),
        ("General Sensor Data", test_general_sensor),
        ("Batch Data", test_batch_data),
    ]
    
    passed = 0
    total = len(tests)
    
    print(f"\n🚀 Running {total} API tests...")
    print("-" * 40)
    
    for test_name, test_func in tests:
        print(f"\n🔄 Testing {test_name}...")
        if test_func():
            print(f"✅ {test_name}: PASSED")
            passed += 1
        else:
            print(f"❌ {test_name}: FAILED")
        time.sleep(1)
    
    # Test data retrieval
    test_data_retrieval()
    
    print("\n" + "=" * 60)
    print(f"🏁 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests completed successfully!")
        print("✅ Your underwater navigation API with MongoDB is working perfectly!")
    else:
        print("⚠️  Some tests failed. Check the server logs for more details.")
    
    print("\n📚 API Documentation: http://localhost:8000/docs")
    print("🗄️  MongoDB Express: http://localhost:8081")

if __name__ == "__main__":
    main()
