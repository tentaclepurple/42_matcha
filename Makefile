.PHONY: up all down exec env clean

all: up

up:
	docker compose up -d

down:
	docker compose down

exec:
	docker exec -it backend bash

run:
	cd matcha_backend && python3 run.py

logs:
	docker logs backend

test:
	cd matcha_backend/app/scripts/ && python3 generate_test_users.py

clean: down
	yes | docker system prune -a