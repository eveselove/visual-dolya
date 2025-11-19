
import streamlit as st
import pandas as pd
import pydeck as pdk

st.set_page_config(page_title="Geo Model 2025", layout="wide")

st.title("HEX-MODEL 2025")

try:
    df = pd.read_csv('population_geo_v3.csv')
    
    df_target = df[df['Status'] == 'Target']
    df_neutral = df[df['Status'] == 'Neutral']
    
    mid_lat = df['lat'].mean()
    mid_lon = df['lon'].mean()

    # СЛОЙ 1: Target
    layer_target = pdk.Layer(
        "HexagonLayer",
        data=df_target,
        get_position='[lon, lat]',
        radius=20000,
        elevation_scale=50,
        elevation_range=[0, 3000],
        pickable=True,
        extruded=True,
        color_range=[[255, 100, 0], [255, 50, 0], [200, 0, 0]]
    )

    # СЛОЙ 2: Neutral
    layer_neutral = pdk.Layer(
        "ColumnLayer",
        data=df_neutral,
        get_position='[lon, lat]',
        get_elevation=20000,
        radius=15000,
        get_fill_color=[80, 80, 80, 150],
        pickable=True,
        extruded=True,
    )

    view_state = pdk.ViewState(
        latitude=mid_lat,
        longitude=mid_lon,
        zoom=4,
        pitch=50,
        bearing=10
    )

    # Убрали map_style="mapbox://..." чтобы избежать проблем с токенами
    r = pdk.Deck(
        layers=[layer_neutral, layer_target],
        initial_view_state=view_state,
        tooltip={"text": "{Локация}
Население: {Население}"}
    )

    st.pydeck_chart(r)
    
    with st.expander("Данные"):
        st.dataframe(df)

except Exception as e:
    st.error(f"Application Error: {e}")
