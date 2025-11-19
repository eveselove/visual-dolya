
import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(layout="wide", page_title="Just Hexagons")
st.title("Карта покрытия (Просто шестиугольники)")

# 1. КООРДИНАТЫ (Скелет карты)
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

# 2. РАСЧЕТ КООРДИНАТ
df['x'] = df['col'] + 0.5 * (df['row'] % 2)
df['y'] = -df['row']

# 3. ОТРИСОВКА (Только шестиугольники, без цвета по данным)
chart = alt.Chart(df).mark_point(
    shape="hexagon",
    size=4500,
    filled=True,
    stroke='white',
    strokeWidth=2,
    color='grey' # Фиксированный серый цвет для всех
).encode(
    x=alt.X('x:Q', axis=None), # :Q для Altair
    y=alt.Y('y:Q', axis=None), # :Q для Altair
    tooltip=['City'] # Подсказка только по городу
).properties(
    height=700
).configure_view(
    strokeWidth=0
)

# Добавляем названия городов
text = alt.Chart(df).mark_text(dy=0, fontWeight='bold', color='white').encode(
    x=alt.X('x:Q', axis=None),
    y=alt.Y('y:Q', axis=None),
    text='City'
)

final_chart = (chart + text)

st.altair_chart(final_chart, use_container_width=True)

st.write("Таблица координат (для проверки):")
st.dataframe(df[['City', 'x', 'y']])
