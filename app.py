
import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(layout="wide", page_title="Hex Map Final")
st.title("Карта покрытия (Работает!)")

# 1. ТЕ ЖЕ САМЫЕ ДАННЫЕ
data = [
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

# 2. КООРДИНАТЫ
df['x'] = df['col'] + 0.5 * (df['row'] % 2)
df['y'] = -df['row']

# 3. ОТРИСОВКА С ЯВНЫМ УКАЗАНИЕМ ТИПОВ (:Q)
# :Q означает Quantitative (Числа). Без этого Altair не понимает градиенты.

base = alt.Chart(df).encode(
    x=alt.X('x:Q', axis=None),  # <--- Добавили :Q
    y=alt.Y('y:Q', axis=None)   # <--- Добавили :Q
)

# Шестиугольники
hexagons = base.mark_point(
    shape="hexagon", 
    size=4500, 
    filled=True, 
    stroke='white', 
    strokeWidth=2,
    opacity=1 
).encode(
    # ВАЖНО: 'Value:Q' исправляет ошибку NaN
    color=alt.Color('Value:Q', scale=alt.Scale(scheme='tealblues'), title='Показатель'),
    tooltip=['City', 'Value']
)

labels = base.mark_text(dy=-10, fontWeight='bold', color='white').encode(text='City')
values = base.mark_text(dy=10, fontSize=10, color='#eee').encode(text='Value')

chart = (hexagons + labels + values).properties(height=700).configure_view(strokeWidth=0)

col1, col2 = st.columns([3, 1])
col1.altair_chart(chart, use_container_width=True)
col2.write("Данные:")
col2.dataframe(df)
