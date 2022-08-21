set -a

source .env

SERVER_NAME=${DOMAIN?Variable not set}
SERVER_HOST=https://${DOMAIN?Variable not set}
BROKER_URI=amqp://guest:guest@localhost:5672
BACKEND_URI=redis://localhost:6379

set +a

cd ./backend/app/

celery worker -A app.celery_task_app.worker -Q $CELERY_QUEUE_NAME -l info -c 1 &
uvicorn app.main:app
