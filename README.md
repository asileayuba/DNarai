# DNarai

DNarai is a mentorship session booking platform built with **Django**, **Celery**, and **Redis**.  
It allows mentees to book leadership sessions, receive email confirmations, and for mentors to confirm and complete sessions.  
All emails are handled asynchronously using Celery.

---

## 🚀 Features
- Custom user authentication (username or email login)
- Session booking system with mentor/mentee email notifications
- Asynchronous tasks with Celery + Redis
- Contact form with duplicate prevention and confirmation emails
- Logging for better observability
- Environment-based configuration using `.env`

---

## 📦 Tech Stack
- [Django](https://www.djangoproject.com/) — Web Framework
- [Celery](https://docs.celeryq.dev/) — Distributed Task Queue
- [Redis](https://redis.io/) — Celery Broker
- [django-celery-beat](https://django-celery-beat.readthedocs.io/) — Periodic Task Scheduling
- [django-celery-results](https://django-celery-results.readthedocs.io/) — Task Results Storage
- [Honcho](https://github.com/nickstenning/honcho) — Process Manager for development
- [Postgres](https://www.postgresql.org/) — Production Database (SQLite for quick dev)

---

## ⚙️ Installation (Local Development without Docker)

1. Clone the repository:
    ```bash
    git clone https://github.com/asileayuba/DNarai.git
    cd DNarai
    ```

2. Create a virtual environment & install dependencies:
    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/macOS
    venv\Scripts\activate     # Windows
    pip install -r requirements.txt
    ```

3. Setup your `.env` file (see `.env.sample`):
    ```bash
    cp .env.sample .env
    ```

4. Run database migrations:
    ```bash
    python manage.py migrate
    ```

5. Collect static files:
    ```bash
    python manage.py collectstatic --noinput
    ```

---

## 🔑 Environment Variables

All sensitive settings are stored in `.env`.

Example `.env.sample`:

```env
# ==========================
# Django Settings
# ==========================
DJANGO_HOST=localhost
DJANGO_ENV=development
DEBUG=True
SECRET_KEY=your-secret-key-here

# Comma-separated list of allowed hosts
ALLOWED_HOSTS=127.0.0.1,localhost,web

# ==========================
# Postgres (for docker-compose)
# ==========================
POSTGRES_DB=your_db_name
POSTGRES_USER=your_db_user
POSTGRES_PASSWORD=your_db_password
POSTGRES_HOST=db
POSTGRES_PORT=5432

# ==========================
# Mentor / Admin Defaults
# ==========================
DEFAULT_MENTOR_EMAIL=mentor@example.com

# ==========================
# Email Settings (SMTP)
# ==========================
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=mailpit # Change to your SMTP server address for production
EMAIL_PORT=1025
EMAIL_USE_SSL=False # Set to True if your SMTP server requires SSL
EMAIL_USE_TLS=False # Set to True if your SMTP server requires TLS
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-email-password
DEFAULT_FROM_EMAIL=your-email@example.com
REMINDER_EMAIL_SUBJECT=Session Reminder: Please Confirm Your Attendance
REMINDER_EMAIL_HTML=<h1>Hi there!</h1><p>This is a friendly reminder to confirm your session attendance. Please click the link below to complete the process.</p>
REMINDER_EMAIL_RECIPIENT=your-email@example.com

# ==========================
# Base URL (used in links inside emails)
# ==========================
BASE_URL=http://127.0.0.1:8000

# ==========================
# Mailpit (for development)
# ==========================
http://127.0.0.1:8025

# ==========================
# Celery / Redis
# ==========================
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=django-db

# ==========================
# Optional
# ==========================
ENVIRONMENT=development
TIME_ZONE=Africa/Lagos
```

---

## 🐳 Running with Docker Compose Profiles

You can run the project in **development** or **production** mode:

### Development Mode

This enables extra services (like Flower, dev ports, etc):

```bash
docker-compose --profile dev build up -d
```

### Production Mode

This runs only the production services:

```bash
docker-compose up -d
```

To stop all services:

```bash
docker-compose down
```

Available Services

- **Django app** → [http://localhost:8000](http://localhost:8000)  
- **Flower (Celery monitoring, dev only)** → [http://localhost:5555](http://localhost:5555)  
- **Mailpit (mailing service, dev only)** → [http://localhost:8025](http://localhost:8025)  
- **Postgres** → `localhost:5432`  
  - Connect with `psql`:  
    ```bash
    psql -h localhost -p 5432 -U dnarai_user -d dnarai_db
    ```  
  - Or use GUI tools like **pgAdmin**, **TablePlus**, **DBeaver**, etc.  
- **Redis** → `localhost:6379`  
  - Connect with `redis-cli`:  
    ```bash
    redis-cli -h localhost -p 6379
    ```  
  - Or use a GUI like **RedisInsight**.  

---

## 🛠️ Running with Makefile (Simpler Workflow)

Instead of long `docker-compose` commands, use the included Makefile.

Common Commands

| Command                   | Description                                         |
|---------------------------|-----------------------------------------------------|
| `make up`                 | Start all services in detached (production) mode    |
| `make up-dev`             | Start all services in development mode              |
| `make down`               | Stop all services and force remove containers/net   |
| `make down-prod`          | Stop only production services and containers        |
| `make down-dev`           | Stop only development services and containers       |
| `make build-dev`          | Build Docker images for dev                         |
| `make build-prod`         | Build Docker images for prod                        |
| `make migrate-prod`       | Run Django migrations (production)                  |
| `make migrate-dev`        | Run Django migrations (development)                 |
| `make createsuperuser-prod` | Create Django superuser (production)              |
| `make createsuperuser-dev`  | Create Django superuser (development)             |
| `make collectstatic-prod` | Collect static files (production)                   |
| `make collectstatic-dev`  | Collect static files (development)                  |
| `make shell-prod`         | Open Django shell (production)                      |
| `make shell-dev`          | Open Django shell (development)                     |
| `make celery-prod`        | Run a Celery worker (production)                    |
| `make celery-dev`         | Run a Celery worker (development)                   |
| `make celery-beat-prod`   | Run Celery Beat scheduler (production)              |
| `make celery-beat-dev`    | Run Celery Beat scheduler (development)             |
| `make flower`             | Start Flower monitoring (development only)          |
| `make logs`               | Tail all container logs                             |
| `make logs-dev`           | Tail development logs                               |
| `make logs-prod`          | Tail production logs                                |
| `make reset-db`           | Reset database by dropping volumes                  |

Example Workflow with Make
```bash
# Start all containers (production)
make up

# Or start in development mode
make up-dev

# Run migrations (production)
make migrate-prod

# Or run migrations (development)
make migrate-dev

# Create superuser (production)
make createsuperuser-prod

# Or create superuser (development)
make createsuperuser-dev

# Collect static files (production)
make collectstatic-prod

# Or collect static files (development)
make collectstatic-dev

# Open Django shell (production)
make shell-prod

# Or open Django shell (development)
make shell-dev

# Start Celery worker (production)
make celery-prod

# Or start Celery worker (development)
make celery-dev

# Start Celery Beat scheduler (production)
make celery-beat-prod

# Or start Celery Beat scheduler (development)
make celery-beat-dev

# Start Flower monitoring (development only)
make flower

# View logs (all)
make logs

# View logs (development only)
make logs-dev

# View logs (production only)
make logs-prod

# Stop everything (any environment)
make down

# Stop only production services
make down-prod

# Stop only development services
make down-dev

# Reset database (drop all volumes)
make reset-db
```

---

## Running the Project with Honcho (Alternative Dev Setup)
For local dev without Docker, you can use [Honcho](https://github.com/nickstenning/honcho) with `Procfile.dev`.

Procfile already exists:
```Procfile
redis: redis-server
web: python manage.py runserver 0.0.0.0:8000
worker: celery -A DNarai worker -l info
beat: celery -A DNarai beat -l info
flower: celery -A DNarai flower --port=5555
```

Start all processes:
```bash
honcho start -f Procfile.dev
```

---

## 📂 Project Structure

```bash
DNarai/
│── DNarai/          # Project settings
│── accounts/        # Custom user model + auth backend
│── core/            # Booking + messaging app
│── templates/       # HTML templates
│── core/static/     # CSS, JS, assets
│── manage.py
│── requirements.txt
│── Procfile.dev
│── Dockerfile
│── docker-compose.yml
│── Makefile
│── Caddyfile
│── nginx.conf
│── .env.sample
│── README.md
```

---

## 📜 License
MIT License.
