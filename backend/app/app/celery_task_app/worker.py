import os
from celery import Celery


BROKER_URI = os.environ['BROKER_URI']
BACKEND_URI = os.environ['BACKEND_URI']

celery_app = Celery(
    "worker",
    broker=BROKER_URI,
    backend=BACKEND_URI,
    include=['app.celery_task_app.tasks']
)
