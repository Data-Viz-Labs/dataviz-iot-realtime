# IoT Real-Time Data Visualization Practice

This project provides a real-time IoT data visualization environment using multiple visualization tools. It simulates IoT sensor data and stores it in a time-series database, making it available through Grafana, Metabase, and others...

## Components

- Data Generator: Python script generating simulated IoT sensor data
- TimescaleDB: Time-series database for storing sensor data
- Grafana: Real-time monitoring dashboards
- Metabase: Business Intelligence and Analytics

## Quick Start

Requirements:
- Docker/Podman
- Docker Compose/Podman Compose
- Make

To start all services:

```bash
make start
```

Access points:

### Grafana
- URL: http://localhost:3000
- Username: admin
- Password: admin

### Metabase
- URL: http://localhost:3001
- Configure on first access with your desired credentials

### Database Connection Details
When configuring data sources manually:
- Host: timescaledb
- Port: 5432
- Database: iotdata
- Username: iotuser
- Password: iotpass

## Project Structure

```
.
├── docker-compose.yml
├── Makefile
├── data_generator/
│   └── generator.py
└── config/
    ├── grafana/
    ├── metabase/
    └── superset/
```

## Data Model

The simulated IoT data includes:
- Event timestamps
- Geolocation data (within Iberian Peninsula)
- Sensor readings (temperature, humidity, pressure)
- Device status and categories
- Event types

## Practice Tasks

1. Create a monitoring dashboard in Grafana showing real-time sensor data
2. Build an analytical dashboard in Metabase for historical analysis
3. Develop a comprehensive dashboard in Superset for data exploration
