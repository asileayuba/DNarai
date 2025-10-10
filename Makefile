# --------------------------------------------------
# Makefile for managing DNarai (Django + Docker)
# --------------------------------------------------

# Docker Compose command
DC=docker-compose 

# Service names
PYTHON_PROD=web
PYTHON_DEV=web-dev
CELERY=celery
CELERY_BEAT=celery-beat
FLOWER=flower

# ---------------------------------------
# Start services
# ---------------------------------------
up:
	@echo "Starting all services (production)..."
	$(DC) --profile prod up -d

up-dev:
	@echo "Starting all services (development)..."
	$(DC) --profile dev up -d

# ---------------------------------------
# Stop services
# ---------------------------------------
down:
	@echo "Stopping all services (any environment)..."
	$(DC) down || true
	@echo "Force removing leftover containers and network..."
	docker stop $$(docker ps -aq --filter "name=dnarai") 2>/dev/null || true
	docker rm $$(docker ps -aq --filter "name=dnarai") 2>/dev/null || true
	docker network rm dnarai_default 2>/dev/null || true

down-prod:
	@echo "Stopping production services..."
	$(DC) --profile prod down || true
	docker stop $$(docker ps -aq --filter "name=dnarai-.*prod") 2>/dev/null || true
	docker rm $$(docker ps -aq --filter "name=dnarai-.*prod") 2>/dev/null || true

down-dev:
	@echo "Stopping development services..."
	$(DC) --profile dev down || true
	docker stop $$(docker ps -aq --filter "name=dnarai-.*dev") 2>/dev/null || true
	docker rm $$(docker ps -aq --filter "name=dnarai-.*dev") 2>/dev/null || true

# ---------------------------------------
# Build & maintenance
# ---------------------------------------
build-dev:
	@echo "Building Docker images..."
	$(DC) --profile dev build

build-prod:
	@echo "Building Docker images..."
	$(DC) --profile prod build

# Apply migrations
migrate-prod:
	@echo "Applying migrations (production)..."
	$(DC) exec $(PYTHON_PROD) python manage.py migrate

migrate-dev:
	@echo "Applying migrations (development)..."
	$(DC) exec $(PYTHON_DEV) python manage.py migrate

# Create superuser
createsuperuser-prod:
	@echo "Creating superuser (production)..."
	$(DC) exec $(PYTHON_PROD) python manage.py createsuperuser

createsuperuser-dev:
	@echo "Creating superuser (development)..."
	$(DC) exec $(PYTHON_DEV) python manage.py createsuperuser

# Collect static files
collectstatic-prod:
	@echo "Collecting static files (production)..."
	$(DC) exec $(PYTHON_PROD) python manage.py collectstatic --noinput

collectstatic-dev:
	@echo "Collecting static files (development)..."
	$(DC) exec $(PYTHON_DEV) python manage.py collectstatic --noinput

# Open Django shell
shell-prod:
	@echo "Opening Django shell (production)..."
	$(DC) exec $(PYTHON_PROD) python manage.py shell

shell-dev:
	@echo "Opening Django shell (development)..."
	$(DC) exec $(PYTHON_DEV) python manage.py shell

# ---------------------------------------
# Celery workers (both prod & dev)
# ---------------------------------------
celery-prod:
	@echo "Starting Celery worker (production)..."
	$(DC) --profile prod up -d $(CELERY)

celery-dev:
	@echo "Starting Celery worker (development)..."
	$(DC) --profile dev up -d $(CELERY)

celery-beat-prod:
	@echo "Starting Celery Beat scheduler (production)..."
	$(DC) --profile prod up -d $(CELERY_BEAT)

celery-beat-dev:
	@echo "Starting Celery Beat scheduler (development)..."
	$(DC) --profile dev up -d $(CELERY_BEAT)

# ---------------------------------------
# Monitoring (dev only)
# ---------------------------------------
flower:
	@echo "Starting Flower monitoring..."
	$(DC) --profile dev up -d $(FLOWER)

# ---------------------------------------
# Logs & DB
# ---------------------------------------
logs:
	@echo "Tailing all container logs..."
	$(DC) logs -f

logs-dev:
	@echo "Tailing development logs..."
	$(DC) --profile dev logs -f

logs-prod:
	@echo "Tailing production logs..."
	$(DC) --profile prod logs -f

reset-db:
	@echo "Resetting database (dropping volumes)..."
	$(DC) down -v || true
	docker volume rm dnarai_postgres_data 2>/dev/null || true

.PHONY: up up-dev down down-dev down-prod build \
	migrate-prod migrate-dev createsuperuser-prod createsuperuser-dev \
	collectstatic-prod collectstatic-dev shell-prod shell-dev \
	celery-prod celery-dev celery-beat-prod celery-beat-dev flower \
	logs logs-dev logs-prod reset-db
