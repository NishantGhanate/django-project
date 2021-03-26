from __future__ import absolute_import, unicode_literals
from celery import Celery
import os 

os.environ.setdefault('DJANGO_SETTINGS_MODULE','django_project.settings')

app = Celery('django_project')
app.config_from_object('django.conf:settings', namespace='Celery')
app.autodiscover_tasks()