import time
import random
from datetime import datetime
from faker import Faker
import numpy as np
from sqlalchemy import create_engine, text
import os
import logging
from sqlalchemy.exc import OperationalError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Faker
fake = Faker()

# Database connection
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_NAME = os.getenv('DB_NAME', 'iotdata')
DB_USER = os.getenv('DB_USER', 'iotuser')
DB_PASS = os.getenv('DB_PASS', 'iotpass')

# Connect to TimescaleDB
db_url = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}'
engine = create_engine(db_url)

def wait_for_db(max_retries=30, delay_seconds=2):
    """Wait for database to be ready"""
    for attempt in range(max_retries):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
                logger.info("Database is ready!")
                return True
        except OperationalError as e:
            logger.warning(f"Database not ready (attempt {attempt + 1}/{max_retries}): {e}")
            time.sleep(delay_seconds)
    
    raise Exception("Could not connect to the database")

def ensure_devices_exist(num_devices=100):
    """Ensure device records exist in the devices table"""
    with engine.connect() as conn:
        for i in range(1, num_devices + 1):
            device_id = f"DEVICE_{i}"
            location = fake.city()
            conn.execute(
                text("""
                INSERT INTO devices (device_id, location_name)
                VALUES (:device_id, :location)
                ON CONFLICT (device_id) DO NOTHING
                """),
                {"device_id": device_id, "location": location}
            )

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
        'time': datetime.utcnow(),
        'device_id': device_id,
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
    
    logger.info("Ensuring devices exist...")
    ensure_devices_exist()
    
    logger.info("Starting data generation...")
    while True:
        try:
            data = generate_sensor_data()
            with engine.connect() as conn:
                conn.execute(
                    text("""
                    INSERT INTO sensor_data (
                        time, device_id, temperature, humidity, 
                        pressure, latitude, longitude, status, event_type
                    ) VALUES (
                        :time, :device_id, :temperature, 
                        :humidity, :pressure, :latitude, 
                        :longitude, :status, :event_type
                    )
                    """),
                    data
                )
            time.sleep(1)  # Generate data every second
            
        except Exception as e:
            logger.error(f"Error: {e}")
            time.sleep(5)  # Wait before retrying

if __name__ == "__main__":
    main()
