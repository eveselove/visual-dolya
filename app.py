
import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(layout="wide", page_title="Final Hex Test")
st.title("Карта покрытия (ФИНАЛЬНЫЙ ТЕСТ)")

# 1. СОЗДАЕМ ЕДИНУЮ ТАБЛИЦУ ВРУЧНУЮ
# Здесь мы сразу прописываем И координаты, И данные.
# Никаких merge, никаких CSV.
data = [
    # Город       X (col)  Y (row)  Значение
    {'City': 'Череповец', 'col': 0, 'row': 0, 'Value': 300000},
    {'City': 'Вологда',   'col': 1, 'row': 0, 'Value': 311000},
    {'City': 'Рыбинск',   'col': 0, 'row': 1, 'Value': 180000},
    {'City': 'Ярославль', 'col': 1, 'row': 1, 'Value': 600000},
    {'City': 'Кострома',  'col': 2, 'row': 1, 'Value': 270000},
    {'City': 'Иваново',   'col': 1, 'row': 2, 'Value': 400000},
    {'City': 'Москва',    'col': 0, 'row': 3, 'Value': 12000000},
    {'City': 'Владимир',  'col': 1, 'row': 3, 'Value': 350000},
    {'City': 'Тула',      'col': 0, 'row': 4, 'Value': 500000},
    {'City': 'Рязань',    'col': 1, 'row': 4, 'Value': 530000},
    {'City': 'Липецк',    'col': 0, 'row': 5, 'Value': 500000},
    {'City': 'Тамбов',    'col': 1, 'row': 5, 'Value': 290000},
    {'City': 'Воронеж',   'col': 0, 'row': 6, 'Value': 1000000},
]

df = pd.DataFrame(data)

# 2. РАСЧЕТ КООРДИНАТ ПРЯМО В PYTHON
# Считаем x и y здесь, чтобы Altair не мучился
df['x'] = df['col'] + 0.5 * (df['row'] % 2)
df['y'] = -df['row']

# 3. ВЫВОДИМ ТАБЛИЦУ НА ЭКРАН (ДЛЯ ПРОВЕРКИ)
st.write("Если вы видите эту таблицу с цифрами, график ОБЯЗАН работать:")
st.dataframe(df)

# 4. РИСУЕМ ГРАФИК
# Максимально простая конфигурация
chart = alt.Chart(df).mark_point(
    shape="hexagon",
    size=4500,
    filled=True,
    stroke='white',
    strokeWidth=2
).encode(
    x=alt.X('x', axis=None),
    y=alt.Y('y', axis=None),
    color=alt.Color('Value', scale=alt.Scale(scheme='tealblues')),
    tooltip=['City', 'Value']
).properties(
    height=700
).configure_view(
    strokeWidth=0
)

st.altair_chart(chart, use_container_width=True)
