
import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(layout="wide", page_title="Карта Филиалов")
st.title("Карта покрытия (План 2025)")

# 1. Загрузка
try:
    df_data = pd.read_csv("data_final.csv")
    # Определяем колонку с данными автоматически
    numeric_cols = df_data.select_dtypes(include=['number']).columns
    target_col = 'Население' if 'Население' in numeric_cols else (numeric_cols[0] if len(numeric_cols) > 0 else 'Value')
except:
    st.error("Нет данных")
    st.stop()

# 2. Скелет карты (Все нужные города)
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

# 3. Объединение (Left Join - оставляет все города из layout)
df_hex = pd.merge(df_layout, df_data, on='Город', how='left')

# ЗАПОЛНЯЕМ ПУСТОТЫ НУЛЯМИ
df_hex[target_col] = df_hex[target_col].fillna(0)

# 4. Координаты
df_hex['x'] = df_hex['col'] + 0.5 * (df_hex['row'] % 2)
df_hex['y'] = -df_hex['row']

# 5. Рисуем
chart = alt.Chart(df_hex).mark_point(
    shape="hexagon", size=4500, filled=True, stroke='white', strokeWidth=2
).encode(
    x=alt.X('x', axis=None),
    y=alt.Y('y', axis=None),
    
    # --- УМНАЯ РАСКРАСКА ---
    # Если значение > 0 -> Синий градиент. 
    # Если значение == 0 -> Серый цвет (#d3d3d3).
    color=alt.condition(
        alt.datum[target_col] > 0,
        alt.Color(f'{target_col}:Q', scale=alt.Scale(scheme='tealblues'), title='Показатель'),
        alt.value('#d3d3d3')  # Серый цвет для пустых
    ),
    
    tooltip=['Город', f'{target_col}:Q']
).configure_view(strokeWidth=0).properties(height=700)

# Текст (Город)
text = alt.Chart(df_hex).mark_text(dy=0, fontWeight='bold', color='white').encode(
    x='x', y='y', text='Город'
)
# Текст (Цифра)
val = alt.Chart(df_hex).mark_text(dy=20, fontSize=10, color='#333').encode(
    x='x', y='y', text=f'{target_col}:Q'
)

final = chart + text + val

col1, col2 = st.columns([3, 1])
col1.altair_chart(final, use_container_width=True)
col2.write("Таблица данных:")
col2.dataframe(df_hex[['Город', target_col]])
