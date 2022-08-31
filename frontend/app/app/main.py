import streamlit as st

from app.config import settings
from app.dispatcher import dispatcher
from app.schemas.page_tab import PageTab


def create_app():
    """Create the frontend page from start."""

    placeholder = st.empty()
    dispatcher(
        placeholder=placeholder,
        page_tab=PageTab(page_name="home-page", key=settings.home_page_key),
    )


create_app()
