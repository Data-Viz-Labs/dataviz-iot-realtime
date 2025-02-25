import time
import random
from datetime import datetime
from faker import Faker
import numpy as np
from sqlalchemy import create_engine
import os

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

def create_tables():
    """Create necessary database tables"""
    with engine.connect() as conn:
        # Create extension if it doesn't exist
        conn.execute("CREATE EXTENSION IF NOT EXISTS timescaledb;")
        
        # Create sensor_data table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS sensor_data (
                time TIMESTAMPTZ NOT NULL,
                device_id VARCHAR(50),
                temperature FLOAT,
                humidity FLOAT,
                pressure FLOAT,
                latitude FLOAT,
                longitude FLOAT,
                status VARCHAR(20),
                event_type VARCHAR(50)
            );
        """)
        
        # Convert to hypertable
        conn.execute("""
            SELECT create_hypertable('sensor_data', 'time', 
                                   if_not_exists => TRUE);
        """)

def generate_location():
    """Generate random location within Iberian Peninsula"""
    # Approximate boundaries of Iberian Peninsula
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
    print("Creating tables...")
    create_tables()
    
    print("Starting data generation...")
    while True:
        try:
            data = generate_sensor_data()
            with engine.connect() as conn:
                conn.execute(
                    """
                    INSERT INTO sensor_data (
                        time, device_id, temperature, humidity, 
                        pressure, latitude, longitude, status, event_type
                    ) VALUES (
                        %(time)s, %(device_id)s, %(temperature)s, 
                        %(humidity)s, %(pressure)s, %(latitude)s, 
                        %(longitude)s, %(status)s, %(event_type)s
                    )
                    """,
                    data
                )
            time.sleep(1)  # Generate data every second
            
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(5)  # Wait before retrying

if __name__ == "__main__":
    main()
