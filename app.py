
import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(layout="wide", page_title="Bright Hexagons")
st.title("Карта покрытия (Яркие шестиугольники)")

# 1. КООРДИНАТЫ
data = [
    {'City': 'Череповец', 'col': 0, 'row': 0}, {'City': 'Вологда', 'col': 1, 'row': 0},
    {'City': 'Рыбинск', 'col': 0, 'row': 1}, {'City': 'Ярославль', 'col': 1, 'row': 1},
    {'City': 'Кострома', 'col': 2, 'row': 1}, {'City': 'Иваново', 'col': 1, 'row': 2},
    {'City': 'Москва', 'col': 0, 'row': 3}, {'City': 'Владимир', 'col': 1, 'row': 3},
    {'City': 'Тула', 'col': 0, 'row': 4}, {'City': 'Рязань', 'col': 1, 'row': 4},
    {'City': 'Липецк', 'col': 0, 'row': 5}, {'City': 'Тамбов', 'col': 1, 'row': 5},
    {'City': 'Воронеж', 'col': 0, 'row': 6},
]
df = pd.DataFrame(data)
df['x'] = df['col'] + 0.5 * (df['row'] % 2)
df['y'] = -df['row']

# 2. СОЗДАЕМ СЛОИ

# Слой 1: ОЧЕНЬ ЗАМЕТНЫЕ ШЕСТИУГОЛЬНИКИ
hex_layer = alt.Chart(df).mark_point(
    shape="hexagon",
    size=7000,          # УВЕЛИЧЕННЫЙ РАЗМЕР
    filled=True,
    stroke='white',     # БЕЛАЯ ОБВОДКА
    strokeWidth=4,      # ЖИРНАЯ ОБВОДКА
    color='red',        # ЯРКО-КРАСНЫЙ ЦВЕТ
    opacity=1           # ПОЛНАЯ НЕПРОЗРАЧНОСТЬ
).encode(
    x=alt.X('x:Q', axis=None),
    y=alt.Y('y:Q', axis=None),
    tooltip=['City']
)

# Слой 2: Текст (с отступом, чтобы не сливался с красным)
text_layer = alt.Chart(df).mark_text(
    dy=0,                  # Отступ от центра по Y
    dx=0,                  # Отступ от центра по X
    fontWeight='bold',
    color='white'
).encode(
    x=alt.X('x:Q', axis=None),
    y=alt.Y('y:Q', axis=None),
    text='City'
)

# 3. ОБЪЕДИНЯЕМ И НАСТРАИВАЕМ
final_chart = (hex_layer + text_layer).properties(
    height=700
).configure_view(
    strokeWidth=0
)

st.altair_chart(final_chart, use_container_width=True)
st.write("Таблица координат:")
st.dataframe(df)
