
import streamlit as st
import pandas as pd
import altair as alt
import re

st.set_page_config(layout="wide", page_title="Map Fixed")

st.title("Карта покрытия (Simple Color)")

# 1. Загрузка и очистка
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("data_raw.csv")
    except:
        return pd.DataFrame(), "Error"
    
    # Определяем колонки
    city_col = next((c for c in df.columns if 'Город' in c or 'Локация' in c), None)
    val_col = next((c for c in df.columns if 'Население' in c or 'Оборот' in c), None)
    
    if not city_col or not val_col:
        return df, "Columns not found"
    
    # Чистим
    clean_df = pd.DataFrame()
    clean_df['City'] = df[city_col].astype(str).str.strip()
    
    def clean_num(x):
        s = str(x)
        s = re.sub(r'[^0-9]', '', s) # Оставляем только цифры
        if s == '': return 0
        return int(s)

    clean_df['Value'] = df[val_col].apply(clean_num)
    return clean_df, "OK"

df_data, status = load_data()
if status != "OK":
    st.stop()

# 2. Координаты (Layout)
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

# 3. Объединение
df_hex = pd.merge(df_layout, df_data, on='City', how='left')
df_hex['Value'] = df_hex['Value'].fillna(0) # Заполняем нулями

# 4. Координаты для Altair
df_hex['x'] = df_hex['col'] + 0.5 * (df_hex['row'] % 2)
df_hex['y'] = -df_hex['row']

# 5. Рисуем (УПРОЩЕННАЯ ВЕРСИЯ)
base = alt.Chart(df_hex).encode(
    x=alt.X('x', axis=None),
    y=alt.Y('y', axis=None)
)

# --- ИСПРАВЛЕННЫЙ СЛОЙ ---
# Убрали alt.condition. Просто красим по Value.
hexagons = base.mark_point(
    shape="hexagon", size=4500, filled=True, stroke='white', strokeWidth=2
).encode(
    color=alt.Color('Value:Q', scale=alt.Scale(scheme='tealblues'), title='Население'),
    tooltip=['City', 'Value']
)
# -------------------------

labels = base.mark_text(dy=-10, fontWeight='bold', color='white').encode(text='City')
values = base.mark_text(dy=10, fontSize=10, color='#eee').encode(text='Value')

chart = (hexagons + labels + values).properties(height=700).configure_view(strokeWidth=0)

st.altair_chart(chart, use_container_width=True)
