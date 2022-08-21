#! /usr/bin/env bash
set -e

celery worker -A app.celery_task_app.worker -Q $CELERY_QUEUE_NAME -l info -c 1
