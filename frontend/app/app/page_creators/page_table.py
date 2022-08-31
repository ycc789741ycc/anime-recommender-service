import app.page_creators.home_page.page_content as home_page
from app.config import settings

PAGE_TABLE = {settings.home_page_key: home_page.create_page}
