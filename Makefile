# Docker Compose command
DC=docker-compose
PYTHON=web
CELERY=celery
CELERY_BEAT=celery-beat
FLOWER=flower

# ---------------------------------------
# Start all services (dev mode)
# ---------------------------------------
up:
	@echo "Starting all services..."
	$(DC) up -d

# Stop all services
down:
	@echo "Stopping all services..."
	$(DC) down

# Rebuild containers
build:
	@echo "Building Docker images..."
	$(DC) build

# Apply database migrations
migrate:
	@echo "Applying migrations..."
	$(DC) exec $(PYTHON) python manage.py migrate

# Create superuser
createsuperuser:
	@echo "Creating superuser..."
	$(DC) exec $(PYTHON) python manage.py createsuperuser

# Collect static files
collectstatic:
	@echo "Collecting static files..."
	$(DC) exec $(PYTHON) python manage.py collectstatic --noinput

# Run Celery worker
celery:
	@echo "Starting Celery worker..."
	$(DC) exec $(PYTHON) celery -A DNarai worker -l info

# Run Celery beat
celery-beat:
	@echo "Starting Celery beat..."
	$(DC) exec $(PYTHON) celery -A DNarai beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler

# Start Flower
flower:
	@echo "Starting Flower monitoring..."
	$(DC) exec $(PYTHON) celery -A DNarai flower --port=5555 --broker=redis://redis:6379/0

# Run Django shell
shell:
	@echo "Opening Django shell..."
	$(DC) exec $(PYTHON) python manage.py shell

# View logs of all services
logs:
	@echo "Showing logs..."
	$(DC) logs -f

# Reset the database (drops volumes)
reset-db:
	@echo "Resetting database..."
	$(DC) down -v
	$(DC) up -d db
	$(MAKE) migrate
