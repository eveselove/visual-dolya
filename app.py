
import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(layout="wide", page_title="Map Test")
st.title("Карта покрытия (Тестовые данные)")

# 1. КООРДИНАТЫ (Скелет карты)
layout_data = [
    {'City': 'Череповец', 'col': 0, 'row': 0}, {'City': 'Вологда', 'col': 1, 'row': 0},
    {'City': 'Рыбинск', 'col': 0, 'row': 1}, {'City': 'Ярославль', 'col': 1, 'row': 1},
    {'City': 'Кострома', 'col': 2, 'row': 1}, {'City': 'Иваново', 'col': 1, 'row': 2},
    {'City': 'Москва', 'col': 0, 'row': 3}, {'City': 'Владимир', 'col': 1, 'row': 3},
    {'City': 'Тула', 'col': 0, 'row': 4}, {'City': 'Рязань', 'col': 1, 'row': 4},
    {'City': 'Липецк', 'col': 0, 'row': 5}, {'City': 'Тамбов', 'col': 1, 'row': 5},
    {'City': 'Воронеж', 'col': 0, 'row': 6},
]
df_layout = pd.DataFrame(layout_data)

# 2. ДАННЫЕ (ВШИТЫЕ ПРЯМО В КОД)
# Мы имитируем, будто файл прочитался идеально.
mock_data = [
    {'City': 'Череповец', 'Value': 300000},
    {'City': 'Вологда', 'Value': 311000},
    {'City': 'Ярославль', 'Value': 500000},
    {'City': 'Москва', 'Value': 12000000},
    {'City': 'Владимир', 'Value': 350000},
    {'City': 'Тула', 'Value': 400000},
    {'City': 'Воронеж', 'Value': 1000000},
    # Рыбинск и прочие специально пропустим, чтобы проверить серый цвет
]
df_data = pd.DataFrame(mock_data)

# 3. ОБЪЕДИНЕНИЕ
# how='left' гарантирует, что все соты из layout останутся на карте
df_hex = pd.merge(df_layout, df_data, on='City', how='left')
df_hex['Value'] = df_hex['Value'].fillna(0) # Заполняем пропуски нулями

# 4. КООРДИНАТЫ ДЛЯ РИСОВАНИЯ
df_hex['x'] = df_hex['col'] + 0.5 * (df_hex['row'] % 2)
df_hex['y'] = -df_hex['row']

# 5. ОТРИСОВКА
base = alt.Chart(df_hex).encode(
    x=alt.X('x', axis=None),
    y=alt.Y('y', axis=None)
)

# Соты
hexagons = base.mark_point(
    shape="hexagon", size=4500, filled=True, stroke='white', strokeWidth=2
).encode(
    # Простое условие цвета: Градиент по Value
    color=alt.Color('Value:Q', scale=alt.Scale(scheme='tealblues'), title='Показатель'),
    tooltip=['City', 'Value']
)

labels = base.mark_text(dy=-10, fontWeight='bold', color='white').encode(text='City')
values = base.mark_text(dy=10, fontSize=10, color='#eee').encode(text='Value')

chart = (hexagons + labels + values).properties(height=700).configure_view(strokeWidth=0)

col1, col2 = st.columns([3, 1])
col1.altair_chart(chart, use_container_width=True)

# ВАЖНО: Выводим таблицу, чтобы видеть, что пошло в график
col2.write("Финальная таблица для графика:")
col2.dataframe(df_hex[['City', 'Value']])
