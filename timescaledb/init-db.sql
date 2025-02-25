-- Create the database
CREATE DATABASE iotdata;

-- Create the user
CREATE USER iotuser WITH PASSWORD 'iotpass';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE iotdata TO iotuser;

-- Connect to the iotdata database
\c iotdata

-- Create TimescaleDB extension
CREATE EXTENSION IF NOT EXISTS timescaledb;

-- Grant privileges on all tables in schema public to iotuser
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO iotuser;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO iotuser;
GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public TO iotuser;

-- Allow iotuser to create new tables (needed for TimescaleDB hypertables)
GRANT CREATE ON SCHEMA public TO iotuser;
