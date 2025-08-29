.PHONY: compose-up compose-down logs clean

compose-up:
	docker compose up -d --build

compose-down:
	docker compose down

logs:
	docker compose logs -f

clean:
	docker compose down -v
