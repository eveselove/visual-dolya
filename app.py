
import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(layout="wide", page_title="Debug Mode")
st.title("🔧 Режим отладки карты")

# 1. Загрузка
try:
    df_data = pd.read_csv("data_debug.csv")
    # Ищем колонку с цифрами
    numeric_cols = df_data.select_dtypes(include=['float64', 'int64']).columns
    target_col = 'Население' if 'Население' in df_data.columns else (numeric_cols[0] if len(numeric_cols)>0 else None)
except:
    st.error("Файл данных пуст или не читается.")
    st.stop()

# 2. Координаты карты (Эталонные имена)
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

# --- БЛОК ДИАГНОСТИКИ (ПОКАЖЕТ ОШИБКУ) ---
with st.expander("🚨 ДИАГНОСТИКА ОШИБОК (ОТКРОЙ МЕНЯ)", expanded=True):
    st.write(f"**Выбранная колонка значений:** `{target_col}`")
    
    cities_map = set(df_layout['Город'])
    cities_excel = set(df_data['Город'])
    
    # Кто не нашелся?
    missing = cities_map - cities_excel
    if missing:
        st.error(f"❌ ЭТИ ГОРОДА ЕСТЬ НА КАРТЕ, НО НЕТ В EXCEL (или названия отличаются):")
        st.write(missing)
        st.info("Проверьте пробелы! Например 'Москва' != 'Москва '")
    else:
        st.success("✅ Все названия городов совпадают!")

    st.write("Пример данных из Excel (первые 5 строк):")
    st.dataframe(df_data.head())

# 3. Объединение
df_hex = pd.merge(df_layout, df_data, on='Город', how='left')
df_hex[target_col] = df_hex[target_col].fillna(0)

# 4. Рисуем
df_hex['x'] = df_hex['col'] + 0.5 * (df_hex['row'] % 2)
df_hex['y'] = -df_hex['row']

chart = alt.Chart(df_hex).mark_point(
    shape="hexagon", size=4500, filled=True, stroke='white', strokeWidth=2
).encode(
    x=alt.X('x', axis=None),
    y=alt.Y('y', axis=None),
    color=alt.Color(f'{target_col}:Q', scale=alt.Scale(scheme='tealblues')),
    tooltip=['Город', f'{target_col}:Q']
).configure_view(strokeWidth=0).properties(height=600)

col1, col2 = st.columns([2,1])
col1.altair_chart(chart, use_container_width=True)
col2.dataframe(df_hex[['Город', target_col]])
