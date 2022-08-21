#! /usr/bin/env bash
set -e

export C_FORCE_ROOT=1
celery worker -A app.celery_task_app.worker -Q $CELERY_QUEUE_NAME -l info -c 1
