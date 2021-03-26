from __future__ import absolute_import, unicode_literals
import logging
from celery import shared_task
from celery.decorators import task
from testapi.email import send_worker_email

logging = logging.getLogger('testapi')

@shared_task
def add(x, y):
    return x + y

@task(name='send_worker_email_task')
def send_worker_email_task(data):
    logging.info("Worker email sent")
    return send_worker_email(data)
