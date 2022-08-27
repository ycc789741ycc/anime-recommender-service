from pydantic import BaseSettings
from app.schemas.recanime.predict import AnimeAttributes


class ComponentKeys(BaseSettings):

    # Component Keys
    reset_button_key = "reset_button"
    predict_button_key = "predict_button"
    
    anime_attribute_slider_keys = [key + "_slidebar" for key in AnimeAttributes().dict().keys()]


component_keys = ComponentKeys()
