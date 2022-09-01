from typing import List

import pandas as pd
import streamlit as st

from app.api.recanime import RecanimeApi
from app.page_creators.home_page.component_keys import component_keys
from app.page_creators.home_page.init_session_states import \
    init_anime_attributes_value_state
from app.schemas.recanime.predict import AnimeAttributes, PredictResults
from app.utils.session_state import set_session_state

recanime_api = RecanimeApi()
recanime_predict_results_pd = pd.DataFrame(
    {"anime name": [], "synopsis": [], "score": []}
)


def create_buttons():
    """Create the buttons for reset the attributes and predict the result."""

    button_cols: List["st._DeltaGenerator"] = st.sidebar.columns(2)
    button_cols[0].button(
        label="Reset",
        key=component_keys.reset_button_key,
        on_click=handle_reset_button_click,
    )
    button_cols[1].button(
        label="Predict",
        key=component_keys.predict_button_key,
        on_click=handle_predict_button_click,
    )


def create_sidebars():
    """Create the sidebar contains all of the anime attributes."""

    st.sidebar.header("Tune Your Attributes:")
    create_buttons()

    attributes = list(AnimeAttributes().dict(by_alias=True).keys())
    for attribute, slidebar_key in zip(
        attributes, component_keys.anime_attribute_slider_keys,
    ):
        st.sidebar.slider(
            label=attribute, key=slidebar_key, min_value=0.0, max_value=10.0, step=0.01,
        )


def create_page(placeholder: "st._DeltaGenerator", *args, **kwargs):
    """Create the page"""

    with placeholder.container():
        st.title("Anime Recommender System")
        create_sidebars()
        st.table(data=recanime_predict_results_pd)


def handle_reset_button_click():
    """handle when reset button is clicked"""

    global recanime_predict_results_pd

    set_session_state(init_anime_attributes_value_state)
    recanime_predict_results_pd = pd.DataFrame(
        {"anime name": [], "synopsis": [], "score": []}
    )


def handle_predict_button_click():
    """handle when predict button is clicked"""

    global recanime_predict_results_pd

    anime_attributes_dict = {}
    for anime_attribute_key, component_key in zip(
        AnimeAttributes().dict(by_alias=True).keys(),
        component_keys.anime_attribute_slider_keys,
    ):
        anime_attributes_dict[anime_attribute_key] = st.session_state[component_key]

    anime_attributes = AnimeAttributes(**anime_attributes_dict)
    results: List[PredictResults] = recanime_api.predict_top_k_animes(
        anime_attributes=anime_attributes, top_k=10, timeout=3
    )

    selected_results = {
        "anime name": [],
        "synopsis": [],
        "score": [],
    }
    for result in results:
        selected_results["anime name"].append(result.anime_info.anime_name)
        selected_results["synopsis"].append(result.anime_info.synopsis)
        selected_results["score"].append(result.predict_score)

    recanime_predict_results_pd = pd.DataFrame(data=selected_results)
