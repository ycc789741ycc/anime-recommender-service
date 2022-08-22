import streamlit as st

from app.page_creators.home_page.init_session_states import init_anime_attributes_value_state
from app.schemas.recanime.predict import AnimeAttributes
from app.utils.session_state import set_session_state


def create_sidebars():
    """Create the sidebar contains all of the anime attributes"""
    
    st.sidebar.header("Tune Your Attributes:")
    attributes = list(AnimeAttributes().dict().keys())
    for attribute in attributes:
        st.session_state[attribute + "value"] = st.sidebar.slider(
            label=attribute,
            min_value=0.,
            max_value=10.,
            step=0.01,
            value=0.
        )


def create_page(placeholder: 'st._DeltaGenerator', *args, **kwargs):
    """Create the page"""
    
    set_session_state(init_anime_attributes_value_state)

    with placeholder.container():
        st.title('Anime Recommender System')
        create_sidebars()
