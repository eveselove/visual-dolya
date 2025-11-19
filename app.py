
import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(layout="wide", page_title="Just Hexagons Fix")
st.title("Карта покрытия (Шестиугольники)")

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

# 2. СОЗДАЕМ СЛОИ (БЕЗ НАСТРОЕК)

# Слой 1: Шестиугольники
hex_layer = alt.Chart(df).mark_point(
    shape="hexagon",
    size=4500,
    filled=True,
    stroke='white',
    strokeWidth=2,
    color='grey'
).encode(
    x=alt.X('x:Q', axis=None),
    y=alt.Y('y:Q', axis=None),
    tooltip=['City']
)

# Слой 2: Текст
text_layer = alt.Chart(df).mark_text(
    dy=0, fontWeight='bold', color='white'
).encode(
    x=alt.X('x:Q', axis=None),
    y=alt.Y('y:Q', axis=None),
    text='City'
)

# 3. ОБЪЕДИНЯЕМ И НАСТРАИВАЕМ (ТЕПЕРЬ ПРАВИЛЬНО)
# Сначала сложение (+), потом properties и configure
final_chart = (hex_layer + text_layer).properties(
    height=700
).configure_view(
    strokeWidth=0
)

st.altair_chart(final_chart, use_container_width=True)
st.dataframe(df)
