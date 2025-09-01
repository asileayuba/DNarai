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
- [Huncho](https://github.com/nickstenning/honcho) — Process Manager for development
- [SQLite/Postgres] — Database (SQLite by default, Postgres ready)

---

## ⚙️ Installation

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

3. Setup your .env file (see .env.sample):
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
DEBUG=True
SECRET_KEY=your-secret-key

# Emails
DEFAULT_MENTOR_EMAIL=mentor@example.com
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=DNarai <no-reply@dnarai.com>

# App
BASE_URL=http://127.0.0.1:8000

# Celery / Redis
CELERY_BROKER_URL=redis://127.0.0.1:6379/0
CELERY_RESULT_BACKEND=django-db

```

---

## Running the Project with Huncho
We use Huncho with a `Procfile` to run Django, Celery, and Redis workers together.

Create a `Procfile.dev`:

```Procfile
redis: redis-server
web: python manage.py runserver 0.0.0.0:8000
worker: celery -A DNarai worker -l info
beat: celery -A DNarai beat -l info
flower: celery -A DNarai flower --port=5555
```
Note: `Procfile.dev` has been created already.

Start all processes:

```bash
honcho start -f Procfile.dev
```

---
## 🛠️ Common Commands
Run tests:
```bash
python manage.py test
```

Create a superuser:
```bash
python manage.py createsuperuser
```
Run Celery worker only:
```bash
celery -A DNarai worker -l info
```

Run Celery beat scheduler only:
```bash
celery -A DNarai beat -l info
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
│── .env.sample
│── README.md

```

--- 
## 📜 License
