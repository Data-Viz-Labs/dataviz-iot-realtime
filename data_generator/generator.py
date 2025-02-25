import time
import random
from datetime import datetime
import psycopg2
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database connection
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_NAME = os.getenv('DB_NAME', 'iotdata')
DB_USER = os.getenv('DB_USER', 'iotuser')
DB_PASS = os.getenv('DB_PASS', 'iotpass')

def wait_for_db(max_retries=30, delay_seconds=2):
    """Wait for database to be ready"""
    for attempt in range(max_retries):
        try:
            conn = psycopg2.connect(
                host=DB_HOST,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASS
            )
            conn.close()
            logger.info("Database is ready!")
            return True
        except Exception as e:
            logger.warning(f"Database not ready (attempt {attempt + 1}/{max_retries}): {e}")
            time.sleep(delay_seconds)
    
    raise Exception("Could not connect to the database")

def ensure_device_exists(conn, device_id):
    """Ensure a specific device exists in the database"""
    location = f"Location for {device_id}"
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO devices (device_id, location_name) VALUES (%s, %s) ON CONFLICT (device_id) DO NOTHING",
            (device_id, location)
        )
        cur.close()
        return True
    except Exception as e:
        logger.error(f"Error ensuring device {device_id} exists: {e}")
        return False

def generate_location():
    """Generate random location within Iberian Peninsula"""
    lat = random.uniform(36.0, 43.8)
    lon = random.uniform(-9.5, 3.3)
    return lat, lon

def generate_sensor_data():
    """Generate random sensor data"""
    device_id = f"DEVICE_{random.randint(1, 100)}"
    temperature = random.uniform(10, 35)
    humidity = random.uniform(30, 80)
    pressure = random.uniform(980, 1020)
    lat, lon = generate_location()
    status = random.choice(['ACTIVE', 'IDLE', 'WARNING', 'ERROR'])
    event_type = random.choice([
        'NORMAL_OPERATION',
        'HIGH_TEMPERATURE',
        'LOW_BATTERY',
        'MAINTENANCE_REQUIRED',
        'SYSTEM_UPDATE'
    ])
    
    return {
        'device_id': device_id,
        'time': datetime.utcnow(),
        'temperature': temperature,
        'humidity': humidity,
        'pressure': pressure,
        'latitude': lat,
        'longitude': lon,
        'status': status,
        'event_type': event_type
    }

def main():
    """Main function to generate and insert data"""
    logger.info("Waiting for database to be ready...")
    wait_for_db()
    
    logger.info("Starting data generation...")
    
    # Establecer una conexión persistente con autocommit
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    conn.autocommit = True
    
    while True:
        try:
            data = generate_sensor_data()
            device_id = data['device_id']
            
            # Ensure device exists before inserting sensor data
            ensure_device_exists(conn, device_id)
            
            # Insert sensor data
            cur = conn.cursor()
            cur.execute(
                """
                INSERT INTO sensor_data (
                    time, device_id, temperature, humidity, 
                    pressure, latitude, longitude, status, event_type
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
                """,
                (
                    data['time'], data['device_id'], data['temperature'],
                    data['humidity'], data['pressure'], data['latitude'],
                    data['longitude'], data['status'], data['event_type']
                )
            )
            cur.close()
            
            logger.info(f"Inserted data for {device_id}: temp={data['temperature']:.1f}°C, status={data['status']}")
            time.sleep(1)  # Generate data every second
            
        except Exception as e:
            logger.error(f"Error: {e}")
            time.sleep(5)  # Wait before retrying
            
            # Intentar reconectar si hay un error de conexión
            try:
                if conn.closed:
                    conn = psycopg2.connect(
                        host=DB_HOST,
                        database=DB_NAME,
                        user=DB_USER,
                        password=DB_PASS
                    )
                    conn.autocommit = True
            except:
                pass

if __name__ == "__main__":
    main()
