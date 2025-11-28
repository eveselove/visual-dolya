
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.colors

st.set_page_config(layout="wide", page_title="Coverage Map")

df = pd.read_csv('population_grid.csv')

# --- СТИЛИ ---
st.markdown("""
    <style>
    .title-text {
        font-size: 28px !important;
        text-align: center;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .footer-text {
        font-size: 12px;
        color: #666;
        text-align: center;
        margin-top: 20px;
        font-family: sans-serif;
    }
    </style>
""", unsafe_allow_html=True)

# --- ЗАГОЛОВОК ---
st.markdown('<div class="title-text">Карта покрытия</div>', unsafe_allow_html=True)

if not df.empty:
    text_col = 'Локация' if 'Локация' in df.columns else 'Город'
    
    # ЦВЕТОВАЯ ШКАЛА (Белый -> Синий)
    custom_colorscale = [
        [0.0, '#ffffff'], 
        [1.0, '#0033cc'] 
    ]
    
    # НАСТРОЙКА ГРАНИЦ ШКАЛЫ (ОБНОВЛЕНО: МАКС 800К)
    color_min = 50000.0   
    color_max = 800000.0  # Синий насыщенный

    fig = go.Figure()
    shapes = []
    
    def get_color_hex(val):
        # Обрезаем значения (Clamp)
        val = max(color_min, min(color_max, val))
        # Нормализация 0..1
        norm = (val - color_min) / (color_max - color_min)
        return plotly.colors.sample_colorscale(custom_colorscale, [norm])[0]

    for index, row in df.iterrows():
        color = get_color_hex(row['Население'])
        
        shapes.append(dict(
            type="circle",
            xref="x", yref="y",
            x0=row['x'] - row['r'],
            y0=row['y'] - row['r'],
            x1=row['x'] + row['r'],
            y1=row['y'] + row['r'],
            fillcolor=color,
            line=dict(color="rgba(0,0,0,0.2)", width=1.5), 
            layer="below"
        ))
    
    fig.update_layout(shapes=shapes)

    # ТЕКСТ
    fig.add_trace(go.Scatter(
        x=df['x'],
        y=df['y'],
        mode='text',
        text=df[text_col],
        textposition='middle center',
        textfont=dict(color='#333333', size=13, weight='bold', shadow='1px 1px 2px white'),
        hovertext=[f"{row[text_col]}: {row['Население']:,}" for _, row in df.iterrows()],
        hoverinfo="text",
        showlegend=False
    ))

    # ШКАЛА СПРАВА
    fig.add_trace(go.Scatter(
        x=[None], y=[None],
        mode='markers',
        marker=dict(
            colorscale=custom_colorscale,
            showscale=True,
            cmin=color_min,
            cmax=color_max,
            colorbar=dict(
                title="Население",
                thickness=15,
                len=0.6,
                yanchor="middle",
                y=0.5,
                # Обновленные подписи шкалы
                tickvals=[50000, 200000, 400000, 600000, 800000],
                ticktext=["50k", "200k", "400k", "600k", "800k+"]
            )
        ),
        hoverinfo='none',
        showlegend=False
    ))

    fig.update_yaxes(visible=False, showgrid=False, scaleanchor="x", scaleratio=1, 
                     showline=True, linewidth=2, linecolor='black', mirror=True)
    fig.update_xaxes(visible=False, showgrid=False, 
                     showline=True, linewidth=2, linecolor='black', mirror=True)
    
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        height=700,
        margin=dict(l=20, r=20, t=30, b=20),
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""
        <div class="footer-text">
            Data Source: Внутренняя аналитика • Copyright 2025 VisualDolya
            <br>Размеры кругов пропорциональны численности населения.
        </div>
    """, unsafe_allow_html=True)

else:
    st.write("Нет данных.")
