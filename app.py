
import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(layout="wide", page_title="Карта Филиалов")
st.title("Карта покрытия (План 2025)")

# 1. Загрузка
try:
    df_data = pd.read_csv("data_clean.csv")
except:
    st.error("Ошибка чтения данных")
    st.stop()

# 2. Скелет карты
layout_data = [
    {'Город': 'Череповец', 'col': 0, 'row': 0}, {'Город': 'Вологда', 'col': 1, 'row': 0},
    {'Город': 'Рыбинск', 'col': 0, 'row': 1}, {'Город': 'Ярославль', 'col': 1, 'row': 1},
    {'Город': 'Кострома', 'col': 2, 'row': 1}, {'Город': 'Иваново', 'col': 1, 'row': 2},
    {'Город': 'Москва', 'col': 0, 'row': 3}, {'Город': 'Владимир', 'col': 1, 'row': 3},
    {'Город': 'Тула', 'col': 0, 'row': 4}, {'Город': 'Рязань', 'col': 1, 'row': 4},
    {'Город': 'Липецк', 'col': 0, 'row': 5}, {'Город': 'Тамбов', 'col': 1, 'row': 5},
    {'Город': 'Воронеж', 'col': 0, 'row': 6},
]
df_layout = pd.DataFrame(layout_data)

# 3. Объединение
df_hex = pd.merge(df_layout, df_data, on='Город', how='left')
df_hex['Value'] = df_hex['Value'].fillna(0)

# 4. Координаты
df_hex['x'] = df_hex['col'] + 0.5 * (df_hex['row'] % 2)
df_hex['y'] = -df_hex['row']

# 5. Рисуем
# Базовая диаграмма
base = alt.Chart(df_hex).encode(
    x=alt.X('x', axis=None),
    y=alt.Y('y', axis=None)
)

# Слой сот
hexagons = base.mark_point(
    shape="hexagon", size=4500, filled=True, stroke='white', strokeWidth=2
).encode(
    # Используем простое условие (datum.Value > 0)
    color=alt.condition(
        "datum.Value > 0",
        alt.Color('Value:Q', scale=alt.Scale(scheme='tealblues'), title='Население'),
        alt.value('#d3d3d3') # Серый, если 0
    ),
    tooltip=['Город', alt.Tooltip('Value:Q', title='Население')]
)

# Текст (Названия)
labels = base.mark_text(dy=-10, fontWeight='bold', color='white').encode(text='Город')

# Текст (Цифры)
values = base.mark_text(dy=15, fontSize=10, color='#eee').encode(text='Value:Q')

# Сборка
final_chart = (hexagons + labels + values).properties(
    height=700
).configure_view(
    strokeWidth=0
)

col1, col2 = st.columns([3, 1])
with col1:
    st.altair_chart(final_chart, use_container_width=True)
with col2:
    st.write("Таблица (Проверка типов):")
    # Показываем таблицу
    st.dataframe(df_hex[['Город', 'Value']])
