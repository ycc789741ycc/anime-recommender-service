import app.page_creators.home_page.page_content as home_page
from app.config import settings


PAGE_TABLE = {
    settings.key_home_page: home_page.create_page
}
