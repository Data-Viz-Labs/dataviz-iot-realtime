# IoT Real-Time Data Visualization Practice

A practical environment for visualizing simulated IoT sensor data in real-time using industry-standard tools. This project stores time-series data in TimescaleDB and makes it available through multiple visualization platforms.

## Components

- **Data Generator**: Python script that simulates IoT sensor data
- **TimescaleDB**: Specialized time-series database for efficient storage
- **Grafana**: Real-time monitoring and visualization dashboards
- **Metabase**: Business intelligence and analytics platform

## Quick Start

### Requirements
- Docker/Podman
- Docker Compose/Podman Compose
- Make

### Starting the Environment
```bash
make start
```

### Access Points

| Tool | URL | Default Credentials |
|------|-----|---------------------|
| Grafana | http://localhost:3000 | admin / admin |
| Metabase | http://localhost:3001 | Set on first access |

### Database Connection Details
- Host: timescaledb
- Port: 5432
- Database: iotdata
- Username: iotuser
- Password: iotpass

## Data Model

The simulated IoT data includes:
- Timestamps
- Geolocation (within Iberian Peninsula)
- Environmental readings (temperature, humidity, pressure)
- Device status and categories
- Event classifications

## Project Structure
```
.
├── docker-compose.yml    # Service definitions
├── Makefile              # Convenience commands
├── data_generator/       # Python data simulation
└── timescaledb/          # Database configuration
```

## Available Commands

| Command | Description |
|---------|-------------|
| `make start` | Start all services |
| `make stop` | Stop all services |
| `make logs` | View service logs |
| `make shell-db` | Access database shell |
| `make clean` | Remove containers and images |
| `make clean-all` | Remove all containers, images and volumes |

## Practice Tasks

1. Create a real-time monitoring dashboard in Grafana
2. Build an analytical dashboard in Metabase for historical analysis
3. Analyze sensor data patterns and anomalies
