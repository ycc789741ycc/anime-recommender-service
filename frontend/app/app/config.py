import logging
from typing import Text

from pydantic import BaseSettings


class Settings(BaseSettings):
    
    logger_name = "recanime-frontend"
    logger = logging.getLogger(logger_name)
    
    # page keys
    key_home_page: Text = "home-page"

    class Config:
        case_sensitive = True


settings = Settings()
