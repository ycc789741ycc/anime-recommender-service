from typing import Any, List

from recanime.recommender.ranking_base_filter.predict import RankingBaseAnimeRec
from fastapi import APIRouter, Body, Depends, HTTPException

from app import schemas
from app.api import deps
from backend.app.app.setting.config import settings


router = APIRouter()


@router.get("/", response_model=List[schemas.Item])
def get_predict():
    pass
