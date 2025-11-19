
import streamlit as st
import pandas as pd
import altair as alt
import numpy as np

st.set_page_config(layout="wide", page_title="Карта 2025")
st.title("Карта покрытия (Hex Map 2025)")

# --- 1. ДАННЫЕ ---
try:
    df_data = pd.read_csv("data_2025.csv")
    target_metric = 'Население' if 'Население' in df_data.columns else 'Value'
except:
    st.error("Нет данных")
    st.stop()

# --- 2. КООРДИНАТЫ ГОРОДОВ (Ваша карта) ---
layout_data = [
    {'Город': 'Череповец',  'col': 0, 'row': 0}, 
    {'Город': 'Вологда',    'col': 1, 'row': 0},
    {'Город': 'Рыбинск',    'col': 0, 'row': 1},
    {'Город': 'Ярославль',  'col': 1, 'row': 1},
    {'Город': 'Кострома',   'col': 2, 'row': 1},
    {'Город': 'Иваново',    'col': 1, 'row': 2},
    {'Город': 'Москва',     'col': 0, 'row': 3},
    {'Город': 'Владимир',   'col': 1, 'row': 3},
    {'Город': 'Тула',       'col': 0, 'row': 4},
    {'Город': 'Рязань',     'col': 1, 'row': 4},
    {'Город': 'Липецк',     'col': 0, 'row': 5},
    {'Город': 'Тамбов',     'col': 1, 'row': 5},
    {'Город': 'Воронеж',    'col': 0, 'row': 6},
]
df_layout = pd.DataFrame(layout_data)

# --- 3. ОБЪЕДИНЕНИЕ ---
# Объединяем по столбцу 'Город'. 
# Важно: имена должны совпадать буква в букву (пробелы мы почистили в Colab)
df_hex = pd.merge(df_layout, df_data, on='Город', how='left')

# Если данных нет, ставим 0
df_hex[target_metric] = df_hex[target_metric].fillna(0)

# --- 4. КООРДИНАТЫ ДЛЯ РИСОВАНИЯ ---
df_hex['x_plot'] = df_hex['col'] + 0.5 * (df_hex['row'] % 2)
df_hex['y_plot'] = -df_hex['row']

# --- 5. ГРАФИК ---
# Основной слой (Соты)
hex_layer = alt.Chart(df_hex).mark_point(
    shape="hexagon", size=4500, filled=True, stroke='white', strokeWidth=2
).encode(
    x=alt.X('x_plot', axis=None),
    y=alt.Y('y_plot', axis=None),
    color=alt.Color(f'{target_metric}:Q', scale=alt.Scale(scheme='tealblues'), title='Население'),
    tooltip=['Город', f'{target_metric}:Q']
)

# Текст (Названия)
text_layer = alt.Chart(df_hex).mark_text(dy=0, fontWeight='bold', color='white').encode(
    x='x_plot', y='y_plot', text='Город'
)

# Текст (Цифры)
val_layer = alt.Chart(df_hex).mark_text(dy=20, fontSize=10, color='#eee').encode(
    x='x_plot', y='y_plot', text=f'{target_metric}:Q'
)

final_chart = (hex_layer + text_layer + val_layer).configure_view(strokeWidth=0).properties(
    height=700
)

# Вывод
col1, col2 = st.columns([3, 1])
with col1:
    st.altair_chart(final_chart, use_container_width=True)
with col2:
    st.dataframe(df_hex[['Город', target_metric]])
