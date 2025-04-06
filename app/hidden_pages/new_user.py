import streamlit as st

from core.storage import save_user_data, get_user_ids
from core.userprofile import UserProfile


def create_new_user():
    """Create a new user with a unique ID and initial settings."""
    st.title("Create New User")

    # Step 1: Ask for the user's name
    name = st.text_input("Enter your name")

    if st.button("Create User"):
        # Step 2: Ensure that name doesn't already exist
        existing_users = get_user_ids()
        if name in existing_users:
            st.error("User with that name already exists!")
            return
        user_id = name.lower().replace(" ", "_")
        new_user_data = UserProfile(
            user_id=user_id,
            name=name,
        )
        # Step 5: Save the user data
        save_user_data(user_id, new_user_data)

        st.success(f"New user '{name}' created successfully!")
        st.session_state["user_id"] = user_id
        st.session_state["user_data"] = new_user_data
        st.session_state["is_creating_new_user"] = False

        st.switch_page("pages/2_User.py")
