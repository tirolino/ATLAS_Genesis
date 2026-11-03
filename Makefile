.PHONY: install test lint arch typecheck check up down migrate
install:
	pip install -e ".[dev,db]"
test:
	pytest -q
lint:
	ruff check src tests
arch:
	lint-imports
typecheck:
	mypy src
check: lint arch typecheck test
up:
	docker compose up -d postgres
down:
	docker compose down
migrate:
	@for f in database/migrations/*.sql; do echo "-> $$f"; psql "$$DATABASE_URL" -v ON_ERROR_STOP=1 -f $$f; done
