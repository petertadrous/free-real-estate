import streamlit as st


def _is_new_user():
    if (
        ("user_id" not in st.session_state.keys())
        or (st.session_state["user_id"] is None)
        or (st.session_state["user_id"] == "")
    ):
        return True
    else:
        return False


def _is_creating_new_user():
    if (
        "is_creating_new_user" in st.session_state.keys()
        and st.session_state["is_creating_new_user"]
    ):
        return True
    else:
        return False


def _is_changing_user():
    if (
        "is_changing_user" in st.session_state.keys()
        and st.session_state["is_changing_user"]
    ):
        return True
    else:
        return False
