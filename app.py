
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide", page_title="Abstract Population Grid")

# Загрузка
df = pd.read_csv('population_grid.csv')

# --- ВАЛИДАЦИЯ НАСЕЛЕНИЯ (FIX) ---
df['Население'] = pd.to_numeric(df['Население'], errors='coerce')
df = df.dropna(subset=['Население'])
# ---------------------------------

# --- САЙДБАР УБРАН ---
# st.sidebar.header("Настройки Визуализации")

st.title("Абстрактная карта филиалов")
# st.markdown("Используйте слайдер **'Масштаб пузырей'** слева, чтобы настроить плотность кругов.")

# Метрика
total_pop = df['Население'].sum()
st.metric("Общее население", f"{total_pop:,.0f}")

if not df.empty:
    text_col = 'Локация' if 'Локация' in df.columns else 'Город'

    # График
    fig = px.scatter(
        df,
        x='Rank X',
        y='Rank Y',
        size='Население',
        color='Население',
        text=text_col,
        hover_data=['Население'],
        color_continuous_scale=px.colors.sequential.Viridis,
        size_max=85, # ФИКСИРОВАННЫЙ РАЗМЕР
        title="Относительное расположение городов"
    )

    fig.update_traces(textposition='top center')

    # Фиксация 1:1
    fig.update_yaxes(scaleanchor="x", scaleratio=1, visible=False, showgrid=False)
    fig.update_xaxes(visible=False, showgrid=False)

    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        height=700,
        margin=dict(l=10, r=10, t=30, b=10)
    )

    st.plotly_chart(fig, use_container_width=True)
else:
    st.write("Нет данных для отображения.")

with st.expander("Исходные данные"):
    st.dataframe(df)
