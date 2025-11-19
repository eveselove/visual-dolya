
import streamlit as st
import altair as alt
import pandas as pd
import numpy as np

st.set_page_config(layout="wide", page_title="Hex Map: ЦФО + Север")
st.title("Карта филиалов (Центр и Юг) 🇷🇺")

# --- 1. КООРДИНАТЫ (LAYOUT) ---
# Схема расположения сот
data = [
    # --- СЕВЕР (Ряд 0) ---
    {'region': 'Череповец',  'code': 'CHE', 'col': 0, 'row': 0}, 
    {'region': 'Вологда',    'code': 'VLG', 'col': 1, 'row': 0},
    
    # --- ВЕРХНЯЯ ВОЛГА (Ряд 1) ---
    {'region': 'Рыбинск',    'code': 'RYB', 'col': 0, 'row': 1},
    {'region': 'Ярославль',  'code': 'YAR', 'col': 1, 'row': 1},
    {'region': 'Кострома',   'code': 'KOS', 'col': 2, 'row': 1},

    # --- ПРОМЕЖУТОЧНЫЙ (Ряд 2) ---
    {'region': 'Иваново',    'code': 'IVA', 'col': 1, 'row': 2},

    # --- МОСКВА И ОКРУЖЕНИЕ (Ряд 3) ---
    {'region': 'Москва',     'code': 'MSK', 'col': 0, 'row': 3},
    {'region': 'Владимир',   'code': 'VLA', 'col': 1, 'row': 3}, # Справа от МСК

    # --- НОВЫЕ: ТУЛА И РЯЗАНЬ (Ряд 4) ---
    {'region': 'Тула',       'code': 'TUL', 'col': 0, 'row': 4},
    {'region': 'Рязань',     'code': 'RYA', 'col': 1, 'row': 4},

    # --- НОВЫЕ: ЧЕРНОЗЕМЬЕ (Ряд 5) ---
    {'region': 'Липецк',     'code': 'LIP', 'col': 0, 'row': 5},
    {'region': 'Тамбов',     'code': 'TAM', 'col': 1, 'row': 5},

    # --- ЮГ (Ряд 6) ---
    {'region': 'Воронеж',    'code': 'VOR', 'col': 0, 'row': 6},
]

df_hex = pd.DataFrame(data)

# --- 2. ДАННЫЕ ---
# Попытка загрузить реальные данные
try:
    df_real = pd.read_csv('population_clean.csv')
    # Создаем маппинг: Город -> Население
    # Используем 'Локация' или 'Город' из CSV
    if 'Локация' in df_real.columns:
        col_name = 'Локация'
    else:
        col_name = 'Город'
        
    pop_map = dict(zip(df_real[col_name], df_real['Население']))
    
    # Мапим данные на нашу сетку
    df_hex['value'] = df_hex['region'].map(pop_map)
    
    # Заполняем пропуски (для городов из схемы, которых нет в файле) нулями или средним
    df_hex['value'] = df_hex['value'].fillna(100000) # Дефолтное значение для фона
    metric_label = "Население"

except Exception as e:
    st.warning(f"Не удалось подтянуть реальные данные: {e}. Используем случайные.")
    df_hex['value'] = np.random.randint(40, 100, size=len(df_hex))
    metric_label = "Random"

# --- 3. РАСЧЕТ КООРДИНАТ ДЛЯ ALTAIR ---
# Сдвиг нечетных рядов для эффекта "пазла" (Hexagon Grid Logic)
df_hex['x_plot'] = df_hex['col'] + 0.5 * (df_hex['row'] % 2)
df_hex['y_plot'] = -df_hex['row']

# --- 4. ОТРИСОВКА ---
# Базовый слой (Соты)
hex_layer = alt.Chart(df_hex).mark_point(
    shape="hexagon",
    size=4500,       # Размер соты
    filled=True,
    stroke='white',
    strokeWidth=2
).encode(
    x=alt.X('x_plot', axis=None),
    y=alt.Y('y_plot', axis=None, scale=alt.Scale(padding=0.2)),
    color=alt.Color('value', scale=alt.Scale(scheme='viridis'), legend=alt.Legend(title=metric_label)),
    tooltip=['region', 'value', 'code']
).properties(
    height=700
)

# Текстовый слой (Коды городов)
text_layer = alt.Chart(df_hex).mark_text(
    fontSize=16,
    fontWeight='bold'
).encode(
    x=alt.X('x_plot', axis=None),
    y=alt.Y('y_plot', axis=None),
    text='code',
    color=alt.value('white') # Белый текст читается на цветном фоне
)

# Финальный вывод
st.altair_chart((hex_layer + text_layer).interactive(), use_container_width=True)

with st.expander("Таблица данных"):
    st.dataframe(df_hex)
