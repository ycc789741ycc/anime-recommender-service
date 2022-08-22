from typing import Any, Dict, Text

import streamlit as st


def set_session_state(session_state: Dict[Text, Any]) -> None:
    """Set the session state."""

    for key, value in session_state.items():
        st.session_state[key] = value
