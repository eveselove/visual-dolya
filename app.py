
import streamlit as st
import pandas as pd
import pydeck as pdk

st.set_page_config(page_title="Гео-Аналитика 2025", layout="wide")

st.title("🗺️ Карта городов (2025)")

try:
    df = pd.read_csv("population_geo.csv")
    
    st.markdown("**Визуализация**: Распределение городов на карте (Hexagon Layer).")
    
    if not df.empty and 'lat' in df.columns and 'lon' in df.columns:
        # Определяем центр карты
        mid_lat = df['lat'].mean()
        mid_lon = df['lon'].mean()
        
        layer = pdk.Layer(
            "HexagonLayer",
            data=df,
            get_position='[lon, lat]',
            radius=30000,
            elevation_scale=40,
            elevation_range=[0, 1000],
            pickable=True,
            extruded=True,
        )
        
        view_state = pdk.ViewState(
            latitude=mid_lat,
            longitude=mid_lon,
            zoom=3,
            pitch=50,
        )
        
        r = pdk.Deck(
            layers=[layer],
            initial_view_state=view_state,
            tooltip={"text": "Concentration"}
        )
        
        st.pydeck_chart(r)
        
        with st.expander("Показать сырые данные"):
            st.dataframe(df)
    else:
        st.warning("Нет данных с координатами для отображения.")
        
except FileNotFoundError:
    st.error("Файл данных population_geo.csv не найден.")
