import streamlit as st
import pandas as pd

# Настройка страницы
st.set_page_config(page_title="Аналитика", layout="wide")
st.title('Дашборд: Население и Оборот')

# Вкладки
tab1, tab2 = st.tabs(["👥 Население", "💰 Оборот"])

# --- Вкладка 1: Население ---
with tab1:
    st.header("Демография")
    try:
        df_p = pd.read_csv('population_data.csv')
        
        # Фильтры
        cities = df_p['Город'].unique() if 'Город' in df_p.columns else []
        selected_city = st.selectbox('Выберите город', cities, key='sb_city')
        
        if selected_city:
            filtered_p = df_p[df_p['Город'] == selected_city]
        else:
            filtered_p = df_p
            
        col1, col2 = st.columns(2)
        col1.metric("Количество записей", len(filtered_p))
        if 'Население' in filtered_p.columns:
             total_pop = pd.to_numeric(filtered_p['Население'], errors='coerce').sum()
             col2.metric("Общее население", f"{total_pop:,.0f}")
        
        st.dataframe(filtered_p, use_container_width=True)
        
        if 'Население' in filtered_p.columns and 'Город' in filtered_p.columns:
            st.bar_chart(filtered_p.set_index('Город')['Население'])
            
    except Exception as e:
        st.error(f"Ошибка загрузки данных населения: {e}")

# --- Вкладка 2: Оборот ---
with tab2:
    st.header("Финансовые показатели")
    try:
        df_t = pd.read_csv('turnover_data.csv')
        
        # Метрики
        if 'Оборот' in df_t.columns:
             # Чистим данные для графика
             df_t['Оборот_Числ'] = pd.to_numeric(df_t['Оборот'], errors='coerce').fillna(0)
             total_turnover = df_t['Оборот_Числ'].sum()
             st.metric("Общий оборот (фильтр 'Расчет доли'=ДА)", f"{total_turnover:,.2f}")
             
             st.subheader("Топ локаций по обороту")
             if 'Локация' in df_t.columns:
                st.bar_chart(df_t.set_index('Локация')['Оборот_Числ'])
             else:
                st.bar_chart(df_t['Оборот_Числ'])
        
        st.dataframe(df_t, use_container_width=True)
        
    except Exception as e:
        st.info("Данные по обороту не найдены или пустые.")
