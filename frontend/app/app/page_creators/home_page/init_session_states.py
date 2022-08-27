import streamlit as st

from app.page_creators.home_page.component_keys import component_keys
from app.schemas.recanime.predict import AnimeAttributes

init_anime_attributes_value_state = {}
for slider_key in component_keys.anime_attribute_slider_keys:
    init_anime_attributes_value_state[slider_key] = 0.
