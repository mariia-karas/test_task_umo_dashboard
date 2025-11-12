
import streamlit as st
import pandas as pd


st.set_page_config(page_title="Аналіз Математичних Олімпіад", layout="wide")
st.title("🏆 Дашборд-аналіз Олімпіад УМО")


@st.cache_data
def load_data(filepath):
    try:
        df = pd.read_csv(filepath)
        return df
    except FileNotFoundError:
        st.error(f"Файл '{filepath}' не знайдено. Будь ласка, завантажте його у Colab.")
        return None

df = load_data("umo_data_raw.csv")

if df is not None:
    st.header("Огляд даних")
    st.dataframe(df.head(10))

    st.sidebar.header("Фільтри ")

    unique_years = sorted(df['Рік'].unique(), reverse=True)
    selected_year = st.sidebar.selectbox("Оберіть рік:", unique_years)

    unique_teams = sorted(df['Команда'].unique())
    selected_team = st.sidebar.selectbox("Оберіть команду:", ["Всі команди"] + unique_teams)

  
    df_filtered = df[df['Рік'] == selected_year]

    if selected_team != "Всі команди":
        df_filtered = df_filtered[df_filtered['Команда'] == selected_team]

    st.header(f"Результати за {selected_year} рік")
    if selected_team != "Всі команди":
        st.subheader(f"Команда: {selected_team}")
    
    st.dataframe(df_filtered)

    st.header("Аналітика")

    # 1. Кількість учасників за командами (для обраного року)
    st.subheader(f"Кількість учасників за командами у {selected_year} році")
    team_counts_year = df[df['Рік'] == selected_year]['Команда'].value_counts()
    if not team_counts_year.empty:
        st.bar_chart(team_counts_year)
    else:
        st.write("Немає даних для відображення.")

    # 2. Кількість учасників за всі роки (загальна)
    st.subheader("Загальна кількість учасників за всі роки (Top 20)")
    team_counts_all = df['Команда'].value_counts().head(20)
    st.bar_chart(team_counts_all)

else:
    st.warning("Не вдалося завантажити дані для аналізу.")
