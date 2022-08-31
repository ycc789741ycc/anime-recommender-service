from typing import Text

from pydantic import BaseModel


class PageTab(BaseModel):
    page_name: Text
    key: Text
