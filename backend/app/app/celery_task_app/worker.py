import os
from celery import Celery


CELERY_QUEUE_NAME = os.environ['CELERY_QUEUE_NAME']
BROKER_URI = os.environ['BROKER_URI']
BACKEND_URI = os.environ['BACKEND_URI']

celery_app = Celery(
    main=CELERY_QUEUE_NAME,
    broker=BROKER_URI,
    backend=BACKEND_URI,
    include=['app.celery_task_app.tasks']
)
celery_app.conf.task_routes = {'app.celery_task_app.tasks.*': CELERY_QUEUE_NAME}
