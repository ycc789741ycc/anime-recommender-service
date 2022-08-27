import logging
from typing import Text

from pydantic import BaseSettings


class Settings(BaseSettings):
    
    logger_name = "recanime-frontend"
    logger = logging.getLogger(logger_name)
    
    # page keys
    home_page_key: Text = "home-page"

    # urls
    recanime_backend_base_url: Text = "http://localhost/api/v1"

    class Config:
        case_sensitive = True


settings = Settings()
