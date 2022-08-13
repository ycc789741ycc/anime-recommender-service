from typing import Generator

from fastapi import Depends, HTTPException, status

from pydantic import ValidationError
from sqlalchemy.orm import Session

from app import crud, models, schemas
from backend.app.app.setting.config import settings
from app.db.session import SessionLocal


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
