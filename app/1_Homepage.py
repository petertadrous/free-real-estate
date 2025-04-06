import streamlit as st

from app.hidden_pages.welcome import welcome_page

if "user_id" not in st.session_state:
    st.session_state.user_id = None

if "page" not in st.session_state:
    st.session_state["page"] = "welcome"


welcome_page()
