import streamlit as st
from core.storage import load_user_data, save_user_data
from app.hidden_pages.favorites import (
    display_favorites,
    add_new_favorite,
    is_adding_favorites,
)


def user_settings_page():
    user_id = st.session_state.user_id
    user_profile = st.session_state.user_data

    # Display and edit top-level fields
    st.title(f"User Settings - {user_profile.name}")

    # Make settings editable
    name = st.text_input("Name", value=user_profile.name)
    down_payment = st.number_input(
        "Down Payment Budget", value=user_profile.down_payment
    )

    if st.button("Save Changes"):
        user_profile.name = name
        user_profile.down_payment = down_payment
        save_user_data(user_id, user_profile)
        st.session_state.user_data = load_user_data(user_id)
        st.success("Settings Saved!")

    # Display and manage saved locations
    st.subheader("Saved Locations")
    display_favorites(user_profile.favorites)

    if st.button("Add New Location"):
        st.session_state["is_adding_fav"] = True

    if is_adding_favorites():
        add_new_favorite(user_id)


if "user_data" not in st.session_state:
    st.switch_page("1_Homepage.py")
else:
    user_settings_page()
