.PHONY: up all down exec env clean

all: env up exec

up:
	docker compose up -d

down:
	docker compose down

exec:
	docker exec -it backend bash

env:
	@if [ -f .env ]; then \
		echo ".env file already exists. Skipping .env creation."; \
	else \
		read -p "Enter your key: " key; \
		echo "Downloading .env file..."; \
		curl -L "https://www.$$key.com/scl/fi/xq4kwbk1z5rpwy1etgr8l/env?rlkey=fl913obdcaddlo9m06ced0ng9&dl=1" -o .env; \
		echo ".env file has been downloaded."; \
	fi

clean: down
	yes | docker system prune -a