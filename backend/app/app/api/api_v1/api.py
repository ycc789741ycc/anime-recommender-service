from typing import Dict

from fastapi import APIRouter

from app.api.api_v1.endpoints import recommender
from app.config import settings

api_router = APIRouter()
api_router.include_router(recommender.router, tags=["recommender"])


@api_router.get("/health")
async def health() -> Dict:
    settings.logger.debug("Request get host/")
    return {"success": True, "message": "OK"}
