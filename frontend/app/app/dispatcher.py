from typing import Optional

import streamlit as st


from app.schemas.page_tab import PageTab
from app.page_creators.not_found.not_found import page_404
from app.page_creators.page_table import PAGE_TABLE


def dispatcher(placeholder: st._DeltaGenerator, page_tab: Optional[PageTab], *args, **kwargs):
    """Main window page dispatcher."""

    page_creator = page_404
    if page_tab is not None:
        page_creator = PAGE_TABLE.get(page_tab.key, page_404)

    page_creator(placeholder, *args, **kwargs)
