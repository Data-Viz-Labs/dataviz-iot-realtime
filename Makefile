.PHONY: start stop restart clean

start:
	docker-compose up -d

stop:
	docker-compose down

restart: stop start

clean:
	docker-compose down -v

init-superset:
	docker-compose exec superset superset-init

logs:
	docker-compose logs -f
