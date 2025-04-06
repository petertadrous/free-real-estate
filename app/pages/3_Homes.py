import streamlit as st
import pandas as pd
import leafmap.foliumap as leafmap

from app.hidden_pages.states import _is_new_user


def saved_homes_page():
    """Display homes user is considering"""
    user_data = st.session_state.user_data

    st.title(f"Saved Homes for {user_data.name}")

    homes = user_data.homes

    if homes:
        display_homes(homes)
        display_map(user_data)
    else:
        st.write("No homes saved yet.")


def display_map(user_data):
    faves_df = user_data.map_favs
    homes_df = user_data.map_homes
    all_coords = pd.concat(
        [faves_df[["latitude", "longitude"]], homes_df[["latitude", "longitude"]]],
        axis=0,
    )
    map_center = all_coords[["latitude", "longitude"]].mean().values.tolist()
    m = leafmap.Map(center=map_center, zoom=11)

    m.add_points_from_xy(
        user_data.map_favs,
        x="longitude",
        y="latitude",
        color_column="name",
        icon_names=["heart"],
        marker_colors=["red"] * len(faves_df),
        spin=True,
        add_legend=True,
        layer_name="Favorites",
    )
    m.add_points_from_xy(
        homes_df,
        x="longitude",
        y="latitude",
        color_column="address",
        icon_names=["home"],
        marker_colors=["blue"] * len(homes_df),
        spin=True,
        add_legend=True,
        layer_name="Homes",
    )
    m.to_streamlit(height=700)


def display_homes(homes):
    # for home in homes:
    #     st.write(f"Home: {home.address}")
    user_data = st.session_state.user_data
    homes_df = user_data.homes_df
    new_homes_df = homes_df.copy()
    new_homes_df.columns = [c.replace("_", "\n") for c in new_homes_df.columns]
    st.dataframe(new_homes_df)


if _is_new_user():
    st.switch_page("1_Homepage.py")
else:
    saved_homes_page()
