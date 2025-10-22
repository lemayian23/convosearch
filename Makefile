.PHONY: test-install test-system

# Add these to your existing Makefile:

test-install:
	python test_installation.py

test-system:
	python tests/test_system.py

test-all: test-install test-system


.PHONY: build run test ingest-sample clean demo logs

build:
	docker-compose build

run:
	docker-compose up

run-detached:
	docker-compose up -d

test:
	python -m pytest tests/ -v

ingest-sample:
	docker-compose run api python scripts/seed_docs.py

init-db:
	docker-compose run api python scripts/init_db.py

demo:
	docker-compose run api python scripts/run_demo.py

logs:
	docker-compose logs -f

clean:
	docker-compose down
	rm -rf data/ logs/

reset: clean build run

status:
	@echo "=== Service Status ==="
	@curl -s http://localhost:8000/health || echo "API: Not available"
	@echo "=== Recent Tickets ==="
	@curl -s http://localhost:8000/api/tickets | python -m json.tool || echo "Cannot fetch tickets"