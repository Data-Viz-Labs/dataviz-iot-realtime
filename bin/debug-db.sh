
# on EC2
make shell-db

# inside container
psql -U iotuser -d iotdata -f /docker-entrypoint-initdb.d/init-db.sql
psql -U iotuser -d iotdata

# insie psql CLI
\dt
SELECT * FROM devices;
SELECT * FROM sensor_data;