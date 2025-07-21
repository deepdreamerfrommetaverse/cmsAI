.PHONY: dev up down logs

dev:
	docker compose --env-file .env.example up --build

up:
	docker compose --env-file .env.example up -d

down:
	docker compose down

logs:
	docker compose logs -f --tail=50
