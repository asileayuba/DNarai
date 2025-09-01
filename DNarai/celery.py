import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DNarai.settings')

app = Celery('DNarai')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
