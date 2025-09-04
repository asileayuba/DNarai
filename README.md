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
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-email-password
DEFAULT_FROM_EMAIL=your-email@example.com

# ==========================
# Base URL (used in links inside emails)
# ==========================
BASE_URL=http://127.0.0.1:8000

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

## 🐳 Running with Docker

This project comes with a Dockerfile and docker-compose.yml for running Django, Postgres, Redis, Celery, Celery Beat, and Flower.

1. Build images
```bash
docker-compose build
```

2. Start services

```bash
docker-compose up -d

```

3. Run database migrations
```bash
docker-compose exec web python manage.py migrate

```

4. Create superuser
```bash
docker-compose exec web python manage.py createsuperuser
```

5. Check logs
```bash
docker-compose logs -f

```

6. Stop services
```bash
docker-compose down

```

Available services
- Django app → http://localhost:8000
- Flower (Celery monitoring) → http://localhost:5555
- Postgres → localhost:5432
- Redis → localhost:6379

---

## 🛠️ Running with Makefile (Simpler Workflow)

Instead of long `docker-compose` commands, use the included Makefile.

Common Commands

| Command                | Description                         |
| ---------------------- | ----------------------------------- |
| `make up`              | Start all services in detached mode |
| `make down`            | Stop all services                   |
| `make build`           | Build Docker images                 |
| `make migrate`         | Run Django migrations               |
| `make createsuperuser` | Create Django superuser             |
| `make collectstatic`   | Collect static files                |
| `make celery`          | Run a Celery worker                 |
| `make celery-beat`     | Run Celery Beat scheduler           |
| `make flower`          | Start Flower monitoring             |
| `make shell`           | Open Django shell                   |
| `make logs`            | Tail all container logs             |
| `make reset-db`        | Reset database by dropping volumes  |


Example Workflow with Make
```bash
# Start all containers
make up

# Run migrations
make migrate

# Create superuser
make createsuperuser

# View logs
make logs

# Stop everything
make down

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
│── .env.sample
│── README.md

```

---

## 📜 License
MIT License. 
