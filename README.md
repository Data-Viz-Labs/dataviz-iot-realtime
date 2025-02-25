# IoT Real-Time Data Visualization Practice

This project provides a real-time IoT data visualization environment using multiple visualization tools. It simulates IoT sensor data and stores it in a time-series database, making it available through Grafana, Metabase, and Apache Superset.

## Components

- Data Generator: Python script generating simulated IoT sensor data
- TimescaleDB: Time-series database for storing sensor data
- Grafana: Real-time monitoring dashboards
- Metabase: Business Intelligence and Analytics
- Apache Superset: Data exploration and visualization

## Quick Start

Requirements:
- Docker
- Docker Compose
- Make

To start all services:

```bash
make start
```

Access points:
- Grafana: http://localhost:3000
- Metabase: http://localhost:3001
- Superset: http://localhost:8088

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
