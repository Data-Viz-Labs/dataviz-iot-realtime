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

## Troubleshooting

### Common Issues and Solutions

#### Database Connection Problems

If the data generator can't connect to the database:

1. Check if the TimescaleDB container is running:
   ```bash
   make ps
   ```

2. Use the debug script to test database connectivity:
   ```bash
   docker-compose run data_generator python debug.py
   ```

3. Access the database shell to verify the schema:
   ```bash
   make shell-db
   # Then inside the container:
   psql -U iotuser -d iotdata -c "\dt"
   ```

#### Data Not Appearing in Visualizations

1. Verify data is being generated:
   ```bash
   make logs data_generator
   ```

2. Check if data exists in the database:
   ```bash
   make shell-db
   # Then inside the container:
   psql -U iotuser -d iotdata -c "SELECT COUNT(*) FROM sensor_data;"
   ```

3. For Grafana issues, verify the data source configuration:
   - Access Grafana at http://localhost:3000
   - Go to Configuration > Data Sources
   - Check the TimescaleDB connection settings

### Utility Scripts

The repository includes several utility scripts to help with debugging and setup:

- **bin/debug-db.sh**: Provides commands to access and verify the database schema and data
- **data_generator/debug.py**: Tests database connectivity and inserts a test device

### Logs and Monitoring

To view logs from all services:
```bash
make logs
```

To view logs from a specific service:
```bash
docker-compose logs timescaledb
```

For more detailed database diagnostics:
```bash
make shell-db
# Then inside the container:
psql -U iotuser -d iotdata -c "SELECT pg_size_pretty(pg_database_size('iotdata'));"
```
