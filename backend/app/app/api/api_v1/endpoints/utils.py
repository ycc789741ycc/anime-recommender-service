from typing import Any

from fastapi import APIRouter, Depends

from app import models, schemas
from app.api import deps
from backend.app.app.celery_task_app.celery_app import celery_app


router = APIRouter()


@router.post("/test-celery/", response_model=schemas.Msg, status_code=201)
def test_celery(
    msg: schemas.Msg,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Test Celery worker.
    """
    celery_app.send_task("app.worker.test_celery", args=[msg.msg])
    return {"msg": "Word received"}
