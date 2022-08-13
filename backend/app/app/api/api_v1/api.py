from fastapi import APIRouter

from app.api.api_v1.endpoints import recommender

api_router = APIRouter()
api_router.include_router(recommender.router, tags=["recommender"])
