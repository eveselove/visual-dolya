
import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(layout="wide", page_title="Карта Филиалов")
st.title("Карта покрытия (План 2025)")

# 1. Загрузка
try:
    df_data = pd.read_csv("data_final.csv")
    numeric_cols = df_data.select_dtypes(include=['number']).columns
    target_col = 'Население' if 'Население' in numeric_cols else (numeric_cols[0] if len(numeric_cols) > 0 else 'Value')
except:
    st.error("Нет данных")
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
df_hex[target_col] = df_hex[target_col].fillna(0)

# 4. Координаты
df_hex['x'] = df_hex['col'] + 0.5 * (df_hex['row'] % 2)
df_hex['y'] = -df_hex['row']

# 5. Рисуем (БЕЗ НАСТРОЕК, ТОЛЬКО СЛОИ)

# Базовый слой (чтобы не писать X и Y три раза)
base = alt.Chart(df_hex).encode(
    x=alt.X('x', axis=None),
    y=alt.Y('y', axis=None)
)

# Слой 1: Шестиугольники
hex_layer = base.mark_point(
    shape="hexagon", size=4500, filled=True, stroke='white', strokeWidth=2
).encode(
    color=alt.condition(
        alt.datum[target_col] > 0,
        alt.Color(f'{target_col}:Q', scale=alt.Scale(scheme='tealblues'), title='Показатель'),
        alt.value('#d3d3d3')
    ),
    tooltip=['Город', f'{target_col}:Q']
)

# Слой 2: Текст (Город)
text_layer = base.mark_text(dy=0, fontWeight='bold', color='white').encode(
    text='Город'
)

# Слой 3: Текст (Цифра)
val_layer = base.mark_text(dy=20, fontSize=10, color='#333').encode(
    text=f'{target_col}:Q'
)

# 6. СБОРКА И НАСТРОЙКА (ИСПРАВЛЕНО ТУТ)
# Сначала складываем слои, ПОТОМ применяем configure_view
final_chart = (hex_layer + text_layer + val_layer).properties(
    height=700
).configure_view(
    strokeWidth=0
)

col1, col2 = st.columns([3, 1])
with col1:
    st.altair_chart(final_chart, use_container_width=True)
with col2:
    st.write("Таблица данных:")
    st.dataframe(df_hex[['Город', target_col]])
