import streamlit as st

from app.hidden_pages.new_user import create_new_user
from core.storage import get_user_ids, load_user_data

from app.hidden_pages.states import (
    _is_creating_new_user,
    _is_new_user,
    _is_changing_user,
)


def handle_user_change():
    st.session_state["is_changing_user"] = True


def welcome_page():
    st.title("Welcome to House Hunt!")
    st.write("Please select or create a user, or select from the list.")

    # Add button to create a new user
    if st.button("Create"):
        st.session_state["is_creating_new_user"] = True
    if _is_creating_new_user():
        create_new_user()

    user_ids = get_user_ids()

    if _is_new_user():
        default_user_id_idx = 0
    else:
        default_user_id_idx = user_ids.index(st.session_state.user_id) + 1

    user_id = st.selectbox(
        "Select Existing User",
        [""] + user_ids,
        index=default_user_id_idx,
        on_change=handle_user_change,
    )

    if _is_changing_user():
        st.session_state["user_id"] = user_id
        st.session_state["user_data"] = load_user_data(user_id)
        st.session_state["is_changing_user"] = False
        st.switch_page("pages/3_Homes.py")
