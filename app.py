
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.colors
import math

st.set_page_config(layout="wide", page_title="Coverage Map")

try:
    df = pd.read_csv('population_grid.csv')
except FileNotFoundError:
    st.error("Нет данных.")
    st.stop()

st.markdown("""
    <style>
    .title-text { font-size: 28px; text-align: center; font-weight: bold; margin-bottom: 10px; }
    .footer-text { font-size: 12px; color: #666; text-align: center; margin-top: 20px; font-family: sans-serif; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="title-text">Карта покрытия (Hex Tile Map)</div>', unsafe_allow_html=True)

if not df.empty:
    text_col = 'Локация' if 'Локация' in df.columns else 'Город'

    custom_colorscale = [[0.0, '#ebf3ff'], [1.0, '#0033cc']]
    color_min = 50000.0
    color_max = 800000.0

    def get_color_hex(val):
        val = max(color_min, min(color_max, val))
        norm = (val - color_min) / (color_max - color_min)
        return plotly.colors.sample_colorscale(custom_colorscale, [norm])[0]

    def get_hex_path(x, y, r):
        points = []
        r_draw = r * 1.02
        for i in range(6):
            angle_deg = 60 * i - 30
            angle_rad = math.pi / 180 * angle_deg
            px = x + r_draw * math.cos(angle_rad)
            py = y + r_draw * math.sin(angle_rad)
            points.append(f"{px:.2f} {py:.2f}")
        return f"M {points[0]} L {points[1]} L {points[2]} L {points[3]} L {points[4]} L {points[5]} Z"

    fig = go.Figure()
    shapes = []
    NEUTRAL_CITIES = ["Рязань"]

    for index, row in df.iterrows():
        if row[text_col] in NEUTRAL_CITIES:
            color = "#FFFFFF"
            line_color = "#CCCCCC"
        else:
            color = get_color_hex(row['Население'])
            line_color = "white"

        shapes.append(dict(
            type="path",
            path=get_hex_path(row['x'], row['y'], row['r']),
            fillcolor=color,
            line=dict(color=line_color, width=1.5),
            layer="below"
        ))

    fig.update_layout(shapes=shapes)

    fig.add_trace(go.Scatter(
        x=df['x'], y=df['y'], mode='text',
        text=df[text_col],
        textposition='middle center',
        textfont=dict(color='#333333', size=11, weight='bold'),
        hovertext=[f"{row[text_col]}: {row['Население']:,}" for _, row in df.iterrows()],
        hoverinfo="text",
        showlegend=False
    ))

    fig.add_trace(go.Scatter(
        x=[None], y=[None], mode='markers',
        marker=dict(
            colorscale=custom_colorscale, showscale=True, cmin=color_min, cmax=color_max,
            colorbar=dict(title="Население", thickness=15, len=0.6)
        ),
        hoverinfo='none', showlegend=False
    ))

    fig.update_yaxes(visible=False, showgrid=False, scaleanchor="x", scaleratio=1)
    fig.update_xaxes(visible=False, showgrid=False)

    fig.update_layout(
        plot_bgcolor='white', paper_bgcolor='white', height=750,
        margin=dict(l=20, r=20, t=30, b=20), showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)
    st.markdown('<div class="footer-text">VisualDolya 2025 • Спартак Чемпион! 🔴⚪</div>', unsafe_allow_html=True)
else:
    st.write("Нет данных.")
