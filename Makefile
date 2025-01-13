.PHONY: up all down exec env clean

all: env up

up:
	docker compose up -d

down:
	docker compose down

exec:
	docker exec -it backend bash

run:
	cd matcha_backend && python3 run.py

env:
	@if [ -f .env ]; then \
		echo ".env exists."; \
	else \
		echo ".env file not found..."; \
	fi

logs:
	docker logs backend

test:
	cd matcha_backend/app/scripts/ && python3 generate_test_users.py

clean: down
	yes | docker system prune -a