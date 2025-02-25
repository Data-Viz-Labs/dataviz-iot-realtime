# Detect container engine (podman or docker)
CONTAINER_ENGINE := $(shell which podman 2>/dev/null || which docker 2>/dev/null)
COMPOSE_CMD := $(shell if [ -x "$$(which podman-compose)" ]; then echo "podman-compose"; else echo "docker-compose"; fi)

.PHONY: start stop restart clean clean-all logs ps shell-db shell-grafana shell-metabase shell-superset shell-generator

start:
	$(COMPOSE_CMD) up -d

stop:
	$(COMPOSE_CMD) down

restart: stop start

clean:
	$(COMPOSE_CMD) down
	rm -rf config/metabase/metabase-data/*
	# Remove custom built images
	$(CONTAINER_ENGINE) rmi -f iot-real-time-data-visualization_data_generator iot-real-time-data-visualization_timescaledb 2>/dev/null || true

clean-all:
	$(COMPOSE_CMD) down -v
	rm -rf config/metabase/metabase-data/*
	# Remove custom built images
	$(CONTAINER_ENGINE) rmi -f iot-real-time-data-visualization_data_generator iot-real-time-data-visualization_timescaledb 2>/dev/null || true

logs:
	$(COMPOSE_CMD) logs -f

ps:
	$(COMPOSE_CMD) ps

# Shell access to containers
shell-db:
	$(COMPOSE_CMD) exec timescaledb bash

shell-grafana:
	$(COMPOSE_CMD) exec grafana bash

shell-metabase:
	$(COMPOSE_CMD) exec metabase bash

shell-superset:
	$(COMPOSE_CMD) exec superset bash

shell-generator:
	$(COMPOSE_CMD) exec data_generator bash
