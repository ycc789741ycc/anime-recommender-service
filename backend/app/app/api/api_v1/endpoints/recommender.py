import time
from typing import Any, List

from celery.result import AsyncResult
from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.responses import JSONResponse
from recanime.recommender.ranking_base_filter.predict import RankingBaseAnimeRec
from recanime.schema.predict import AnimeAttributes, AnimeInfo, PredictResults

from app.schemas.celery import Task
from app.schemas.response import TaskResponse
from app.celery_task_app.tasks import predict_top_k_animes
from app.app.config import settings


router = APIRouter()


@router.post('/predict', response_model=Task, status_code=202)
async def anime_recommender_predict(
    anime_attributes: AnimeAttributes,
    top_k: int
) -> Task:
    """Create celery prediction task. Return task_id to client in order to retrieve result"""
    
    task_id = predict_top_k_animes.delay(anime_attributes, top_k)
    return Task(task_id=str(task_id), status='Processing')


@router.post(
    '/predict/{task_id}',
    response_model=TaskResponse,
    status_code=200,
    responses={202: {'model': Task, 'description': 'Accepted: Not Ready'}},
)
async def anime_recommender_predict_result(
    task_id,
    start_time: float = Depends(time.time)
) -> TaskResponse:
    """Fetch result for given task_id"""
    
    response = TaskResponse()
    try:
        task = AsyncResult(task_id)
        if not task.ready():
            print(router.url_path_for('anime_recommender_predict'))
            return JSONResponse(status_code=202, content=Task(task_id=str(task_id), status='Processing'))
        result = task.get()
        response.success = True
        response.data = result

    except Exception as e:
            settings.logger.exception(e)
            response.message = f"{type(e).__name__}: {str(e)}"
    response.time_cost = time.time() - start_time

    return response
