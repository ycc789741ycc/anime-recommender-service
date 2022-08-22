import streamlit as st

from app.schemas.recanime.predict import AnimeAttributes


init_anime_attributes_value_state = {}
attributes = list(AnimeAttributes().dict().keys())
for attribute in attributes:
    init_anime_attributes_value_state[attribute + "value"] = 0.
