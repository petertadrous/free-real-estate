import pandas as pd
import streamlit as st


from core.storage import load_user_data, save_user_data

from core.datamodels import (
    Days,
    FavoriteLocation,
    CommutePreferences,
    CommuteWindow,
    CommuteMode,
    Address,
)


def display_favorites(saved_locations: dict[str, FavoriteLocation]):
    if saved_locations:
        data = []
        for name, location in saved_locations.items():
            data.append([name, location.address.address])

        df = pd.DataFrame(data, columns=["Nickname", "Address"])
        event = st.dataframe(
            df,
            on_select="rerun",
            selection_mode="single-row",
            hide_index=True,
        )
        if len(event.selection["rows"]):
            selected_row = event.selection["rows"][0]
            st.session_state["is_editing_fav"] = True
        else:
            st.session_state["is_editing_fav"] = False

        if is_editing_favorite():
            name = df.iloc[selected_row]["Nickname"]
            edit_location(saved_locations[name])

    else:
        st.write("No saved locations yet.")


def is_adding_favorites():
    if "is_adding_fav" in st.session_state.keys() and st.session_state["is_adding_fav"]:
        return True
    else:
        return False


def is_editing_favorite():
    if (
        "is_editing_fav" in st.session_state.keys()
        and st.session_state["is_editing_fav"]
    ):
        return True
    else:
        return False


def add_new_favorite(user_id):
    """Add a new location to the user's saved locations."""
    _days = [day.value for day in Days]
    _modes = [mode.value for mode in CommuteMode]

    st.title("Add New Location")

    nickname = st.text_input("Nickname (e.g. 'Work', 'School')")
    address = st.text_input("Address")
    modes = st.multiselect("Commute Modes", _modes)

    # Commute windows
    to_days = st.multiselect("To Days", _days, default=_days)
    to_time = st.time_input("Arrival Time", value="09:00")

    from_days = st.multiselect("From Days", _days, default=_days)
    from_time = st.time_input("Departure Time", value="17:00")

    if st.button("Save Location"):
        # Retrieve current user data
        user_data = st.session_state.user_data

        # Save the new location
        user_data.add_favorite(
            FavoriteLocation(
                address=Address(address=address),
                nickname=nickname,
                commute_config=CommutePreferences(
                    modes=[CommuteMode(mode) for mode in modes],
                    arrival=CommuteWindow(
                        days=[Days(day) for day in to_days],
                        time=to_time.strftime("%H:%M"),
                    ),
                    departure=CommuteWindow(
                        days=[Days(day) for day in from_days],
                        time=from_time.strftime("%H:%M"),
                    ),
                ),
            )
        )

        # Save the updated user data
        save_user_data(user_id, user_data)
        st.session_state.user_data = load_user_data(user_id)
        st.success(f"Location '{nickname}' added successfully!")
        st.session_state["is_adding_fav"] = False
        st.rerun()

    if st.button("Cancel"):
        st.session_state["is_adding_fav"] = False
        st.rerun()


def edit_location(favorite: FavoriteLocation):
    """Edit an existing saved location."""
    st.subheader(f'Editing "{favorite.nickname}"')
    _days = [day.value for day in Days]
    _modes = [mode.value for mode in CommuteMode]

    nickname = st.text_input(
        "Nickname (e.g. 'Work', 'School')", value=favorite.nickname
    )
    address = st.text_input("Address", value=favorite.address.address)
    modes = st.multiselect(
        "Commute Modes",
        _modes,
        default=[mode.value for mode in favorite.commute_config.modes],
    )

    # Commute windows
    to_days = st.multiselect(
        "To Days",
        _days,
        default=[day.value for day in favorite.commute_config.arrival.days],
    )
    to_time = st.time_input("Arrival Time", value=favorite.commute_config.arrival.time)

    from_days = st.multiselect(
        "From Days",
        _days,
        default=[day.value for day in favorite.commute_config.departure.days],
    )
    from_time = st.time_input(
        "Departure Time", value=favorite.commute_config.departure.time
    )

    if st.button(f"Save Changes to {favorite.nickname}"):
        # Retrieve current user data
        user_data = st.session_state.user_data
        user_id = user_data.user_id
        user_data.remove_favorite(favorite.nickname)

        # Save the new location
        user_data.add_favorite(
            FavoriteLocation(
                address=Address(address=address),
                nickname=nickname,
                commute_config=CommutePreferences(
                    modes=[CommuteMode(mode) for mode in modes],
                    arrival=CommuteWindow(
                        days=[Days(day) for day in to_days],
                        time=to_time.strftime("%H:%M"),
                    ),
                    departure=CommuteWindow(
                        days=[Days(day) for day in from_days],
                        time=from_time.strftime("%H:%M"),
                    ),
                ),
            )
        )

        # Save the updated user data
        save_user_data(user_id, user_data)
        st.session_state.user_data = load_user_data(user_id)
        st.success(f"Location '{nickname}' changed successfully!")
        st.session_state["is_editing_fav"] = False
        st.rerun()

    # if st.button("Cancel"):
    #     st.session_state["is_editing_fav"] = False
    #     st.rerun()
