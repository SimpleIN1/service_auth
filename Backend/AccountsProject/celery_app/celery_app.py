import os
from celery import Celery
from django.apps import apps

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'celery_app.settings')

app = Celery('celery_app') #при локале убрать параметр broker
app.config_from_object('django.conf:settings')

app.autodiscover_tasks(lambda: [n.name for n in apps.get_app_configs()])
