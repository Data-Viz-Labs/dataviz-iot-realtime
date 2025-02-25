-- Create the database
CREATE DATABASE iotdata;

-- Create the user
CREATE USER iotuser WITH PASSWORD 'iotpass';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE iotdata TO iotuser;

-- Connect to the iotdata database
\c iotdata

-- Grant privileges on all tables in schema public to iotuser
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO iotuser;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO iotuser;
GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public TO iotuser;

-- Allow iotuser to create new tables (needed for TimescaleDB hypertables)
GRANT CREATE ON SCHEMA public TO iotuser;

-- Create enum types for status and event types
CREATE TYPE device_status AS ENUM ('ACTIVE', 'IDLE', 'WARNING', 'ERROR');
CREATE TYPE event_type AS ENUM (
    'NORMAL_OPERATION',
    'HIGH_TEMPERATURE',
    'LOW_BATTERY',
    'MAINTENANCE_REQUIRED',
    'SYSTEM_UPDATE'
);

-- Create devices table
CREATE TABLE IF NOT EXISTS devices (
    device_id VARCHAR(50) PRIMARY KEY,
    location_name VARCHAR(100),
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- Create sensor_data table with foreign key
CREATE TABLE IF NOT EXISTS sensor_data (
    time TIMESTAMPTZ NOT NULL,
    device_id VARCHAR(50) REFERENCES devices(device_id),
    temperature FLOAT CHECK (temperature BETWEEN -50 AND 100),
    humidity FLOAT CHECK (humidity BETWEEN 0 AND 100),
    pressure FLOAT CHECK (pressure BETWEEN 800 AND 1200),
    latitude FLOAT CHECK (latitude BETWEEN 36.0 AND 43.8),
    longitude FLOAT CHECK (longitude BETWEEN -9.5 AND 3.3),
    status device_status,
    event_type event_type
);

-- Convert to hypertable
SELECT create_hypertable('sensor_data', 'time');

-- Create indexes
CREATE INDEX ON sensor_data (device_id, time DESC);
CREATE INDEX ON sensor_data (status);
CREATE INDEX ON sensor_data (event_type);

-- Grant privileges on all tables in schema public
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO CURRENT_USER;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO CURRENT_USER;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON FUNCTIONS TO CURRENT_USER;

-- Allow creating new tables (needed for TimescaleDB hypertables)
GRANT CREATE ON SCHEMA public TO CURRENT_USER;

-- Create TimescaleDB extension
CREATE EXTENSION IF NOT EXISTS timescaledb;