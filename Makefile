# Detect container engine (podman or docker)
CONTAINER_ENGINE := $(shell which podman 2>/dev/null || which docker 2>/dev/null)
COMPOSE_CMD := $(shell if [ -x "$$(which podman-compose)" ]; then echo "podman-compose"; else echo "docker-compose"; fi)

.PHONY: start stop restart clean setup logs

setup:
	mkdir -p config/grafana/provisioning/{dashboards,datasources}
	mkdir -p config/grafana/dashboards
	mkdir -p config/metabase/metabase-data
	mkdir -p config/superset
	@echo "Using container engine: $(CONTAINER_ENGINE)"
	@echo "Using compose command: $(COMPOSE_CMD)"

start: setup
	$(COMPOSE_CMD) up -d

stop:
	$(COMPOSE_CMD) down

restart: stop start

clean:
	$(COMPOSE_CMD) down -v
	rm -rf config/metabase/metabase-data/*

logs:
	$(COMPOSE_CMD) logs -f

ps:
	$(COMPOSE_CMD) ps
