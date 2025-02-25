FROM timescale/timescaledb:latest-pg14

COPY postgresql.conf /etc/postgresql/postgresql.conf
COPY init-db.sql /docker-entrypoint-initdb.d/

CMD ["postgres", "-c", "config_file=/etc/postgresql/postgresql.conf"]
