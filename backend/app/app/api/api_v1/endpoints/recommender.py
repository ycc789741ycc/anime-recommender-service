import time
from typing import Dict, List

from celery.result import AsyncResult
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from recanime.schema.predict import AnimeAttributes, PredictResults

from app.celery_task_app.tasks import predict_top_k_animes
from app.config import settings
from app.schemas.celery import Task
from app.schemas.response import TaskResponse
from app.utils.timer import start_time

router = APIRouter()


@router.post("/predict", response_model=Task, status_code=202)
async def anime_recommender_predict(
    anime_attributes: AnimeAttributes, top_k: int
) -> Task:
    """Create celery prediction task. Return task_id to client in order to retrieve result"""

    task_id = predict_top_k_animes.delay(anime_attributes.dict(by_alias=True), top_k)
    return Task(task_id=str(task_id), status="Processing")


@router.get(
    "/predict/{task_id}",
    response_model=TaskResponse,
    status_code=200,
    responses={202: {"model": Task, "description": "Accepted: Not Ready"}},
)
async def anime_recommender_predict_result(
    task_id, start_time: float = Depends(start_time)
) -> TaskResponse:
    """Fetch result for given task_id"""

    response = TaskResponse(task_id=task_id)
    try:
        task = AsyncResult(task_id)
        if not task.ready():
            print(router.url_path_for("anime_recommender_predict"))
            return JSONResponse(
                status_code=202,
                content={"task_id": str(task_id), "status": "Processing"},
            )
        results: List[Dict] = task.get()
        response.success = True
        response.data = [PredictResults(**result) for result in results]

    except Exception as e:
        settings.logger.exception(e)
        response.message = f"{type(e).__name__}: {str(e)}"
    response.time_cost = time.time() - start_time

    return response
