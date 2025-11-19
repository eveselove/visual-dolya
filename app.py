
import streamlit as st
import pandas as pd
import altair as alt
import numpy as np

st.set_page_config(layout="wide", page_title="Карта Филиалов 2025")

st.title("🗺️ Карта покрытия (Hex Map 2025)")

# 1. ЗАГРУЗКА ДАННЫХ ИЗ CSV
try:
    df_data = pd.read_csv("data_2025.csv")
    # Убедимся, что колонка с числом (например, Население) есть
    # Если у вас другая колонка с цифрами, замените 'Население' на неё ниже
    target_metric = 'Население' if 'Население' in df_data.columns else df_data.columns[-1]
except FileNotFoundError:
    st.error("Файл данных не найден.")
    st.stop()

# 2. ОПРЕДЕЛЕНИЕ КООРДИНАТ (LAYOUT)
# Здесь мы вручную "рисуем" карту
layout_data = [
    # СЕВЕР
    {'Город': 'Череповец',  'col': 0, 'row': 0}, 
    {'Город': 'Вологда',    'col': 1, 'row': 0},
    # ВЕРХНЯЯ ВОЛГА
    {'Город': 'Рыбинск',    'col': 0, 'row': 1},
    {'Город': 'Ярославль',  'col': 1, 'row': 1},
    {'Город': 'Кострома',   'col': 2, 'row': 1},
    # ПРОМЕЖУТОЧНЫЙ
    {'Город': 'Иваново',    'col': 1, 'row': 2},
    # ЦЕНТР
    {'Город': 'Москва',     'col': 0, 'row': 3},
    {'Город': 'Владимир',   'col': 1, 'row': 3},
    # НИЖЕ МОСКВЫ
    {'Город': 'Тула',       'col': 0, 'row': 4},
    {'Город': 'Рязань',     'col': 1, 'row': 4},
    # ЧЕРНОЗЕМЬЕ
    {'Город': 'Липецк',     'col': 0, 'row': 5},
    {'Город': 'Тамбов',     'col': 1, 'row': 5},
    # ЮГ
    {'Город': 'Воронеж',    'col': 0, 'row': 6},
]
df_layout = pd.DataFrame(layout_data)

# 3. ОБЪЕДИНЕНИЕ (MERGE)
# Соединяем нарисованную сетку с вашими данными из таблицы
# how='left' значит: показываем карту, даже если данных для города нет (будет серым)
df_hex = pd.merge(df_layout, df_data, on='Город', how='left')

# Заполняем пропуски нулями, чтобы график не ломался
if target_metric in df_hex.columns:
    df_hex[target_metric] = df_hex[target_metric].fillna(0)
else:
    df_hex['Value'] = 0 # Заглушка

# 4. РАСЧЕТ КООРДИНАТ ОТРИСОВКИ
df_hex['x_plot'] = df_hex['col'] + 0.5 * (df_hex['row'] % 2)
df_hex['y_plot'] = -df_hex['row']

# 5. ВИЗУАЛИЗАЦИЯ
metric_col = target_metric if target_metric in df_hex.columns else 'Value'

hex_layer = alt.Chart(df_hex).mark_point(
    shape="hexagon", size=4500, filled=True, stroke='white', strokeWidth=3
).encode(
    x=alt.X('x_plot', axis=None),
    y=alt.Y('y_plot', axis=None),
    # Цвет зависит от значения метрики
    color=alt.Color(f'{metric_col}:Q', scale=alt.Scale(scheme='tealblues'), title='Показатель'),
    tooltip=['Город', f'{metric_col}:Q']
)

text_layer = alt.Chart(df_hex).mark_text(dy=0, fontWeight='bold', color='white').encode(
    x='x_plot', y='y_plot', text='Город'
)

final_chart = (hex_layer + text_layer).configure_view(strokeWidth=0).properties(
    width=650, height=750
)

col1, col2 = st.columns([2, 1])
with col1:
    st.altair_chart(final_chart, use_container_width=True)
with col2:
    st.subheader("Данные")
    st.dataframe(df_hex[['Город', metric_col]].dropna())
