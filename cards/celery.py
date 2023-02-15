from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cards.settings')
app = Celery('cards')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()