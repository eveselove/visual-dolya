import streamlit as st
import pandas as pd

# Загрузка набора данных
df = pd.read_csv('population_data.csv')

# Фильтрация данных: только 2025 год и только города
# Предполагаем, что столбцы 'Год' и 'Тип' существуют и корректны
if 'Год' in df.columns and 'Тип' in df.columns:
    # Приводим к нужному типу для фильтрации (на случай если год считался как строка)
    df['Год'] = pd.to_numeric(df['Год'], errors='coerce')
    # Фильтр: Год 2025 И Тип 'город'
    df = df[(df['Год'] == 2025) & (df['Тип'] == 'город')]

# Обеспечение согласованности имен столбцов: Переименовать 'Локация' в 'Город', если необходимо
if 'Локация' in df.columns and 'Город' not in df.columns:
    df = df.rename(columns={'Локация': 'Город'})

# Добавление заголовка приложения
st.title('Визуализация данных о населении (2025 год)')

# Создание фильтра в боковой панели
cities_list = df['Город'].unique() if 'Город' in df.columns else []
selected_cities = st.sidebar.multiselect('Выберите города', cities_list)

# Фильтрация DataFrame по выбранным городам
if selected_cities:
    filtered_df = df[df['Город'].isin(selected_cities)]
else:
    filtered_df = df

# Отображение таблицы с данными
st.subheader('Таблица данных')
st.dataframe(filtered_df)

# Создание столбчатой диаграммы
st.subheader('График численности населения')
if not filtered_df.empty and 'Город' in filtered_df.columns:
    st.bar_chart(filtered_df.set_index('Город')['Население'])
else:
    st.write("Нет данных для отображения.")
