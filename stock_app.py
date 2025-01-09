import streamlit as st
import pandas as pd
import numpy as np
import datetime

d = pd.read_csv('app_stock/1.csv')
d
st.set_page_config(layout="wide")

@st.cache_data
def load_data_1():
    return pd.read_csv('app_stock/df_1.csv')

@st.cache_data
def load_data_final():
    return pd.read_csv('app_stock/df_final.csv', parse_dates=[0])

df= load_data_final()
df_1 = load_data_1()
    


st.markdown(
    """
    <style>
    .main .block-container {
        padding-top: 2rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)


col1, col2, col3 = st.columns(3)
with col1:
    with st.expander("Фильтры первого уровня"):

        # Создание формы
        with st.form(key="filters_form_1"):

            # Капитализация (две колонки)
            cap1, cap2 = st.columns([1, 1])
            with cap1:
                market_cap_min = st.number_input("Капитализация (млн $) От", value=None)
            with cap2:
                market_cap_max = st.number_input("Капитализация (млн $) До", value=None)

            # Бета компании (две колонки)
            std1, std2 = st.columns([1, 1])
            with std1:
                std_min = st.number_input("Отн. волатильность От", value=None)
            with std2:
                std_max = st.number_input("Отн. волатильность До", value=None)

            # Даты (две колонки)
            t1, t2 = st.columns([1, 1])
            with t1:
                date_1 = st.date_input("Дата От", value=None, min_value=datetime.date(2004, 1, 1))
            with t2:
                date_2 = st.date_input("Дата До", value=None, min_value=datetime.date(2004, 1, 1))

            # Страна и объем торгов (две колонки)
            c1, c2 = st.columns([1, 1])
            with c1:
                country = st.selectbox("Страна акции", ("кроме Китая", "Китай"))
            with c2:
                volume = st.number_input("Объем торгов (тыс. $) От", value=None)

            # Кнопка "Применить"
            apply_button = st.form_submit_button(label="Применить")


with col2:
    with st.expander("Фильтры второго уровня"):

        # Создание формы
        with st.form(key="filters_form_2"):
            # Переоценненость (P/S)
            p_s1, p_s2 = st.columns(2)
            with p_s1:
                ps_min = st.number_input("Переоценненность (P/S) От", value=None)
            with p_s2:
                ps_max = st.number_input("Переоценненность (P/S) До", value=None)
            
            # Форма dS
            ds1, ds2 = st.columns(2)
            with ds1:
                ds_min = st.number_input("Форма dS (%) От", value=None)
            with ds2:
                ds_max = st.number_input("Форма dS (%) До", value=None)

            # PEG TTM
            peg1, peg2 = st.columns(2)
            with peg1:
                peg_min = st.number_input("PEG TTM От", value=None)
            with peg2:
                peg_max = st.number_input("PEG TTM До", value=None)

            # P/E TTM / (P/E)
            pe1, pe2 = st.columns(2)
            with pe1:
                pe_min = st.number_input("P/E отношение (%) От", value=None)
            with pe2:
                pe_max = st.number_input("P/E отношение (%) До", value=None)

            # P/E TTM / (P/E)
            pe51, pe52 = st.columns(2)
            with pe51:
                pe5_min = st.number_input("P/E 5 лет От", value=None)
            with pe52:
                pe5_max = st.number_input("P/E 5 лет До", value=None)

            # Кнопка "Применить"
            apply_button = st.form_submit_button(label="Применить")

with col3:
    with st.expander("Фильтры третьего уровня"):
        # Создание формы
        with st.form(key="filters_form_3"):
            # Увеличенный объем за последние 5 дней до отчета
            volume_increase1, volume_increase2 = st.columns(2)
            with volume_increase1:
                volume_increase_min = st.number_input("Увеличенный объем за последние 5 дней От (%)", value=None)
            with volume_increase2:
                volume_increase_max = st.number_input("Увеличенный объем за последние 5 дней До (%)", value=None)

            # RS за 5 дней против индекса
            rs_5days1, rs_5days2 = st.columns(2)
            with rs_5days1:
                rs_5days_min = st.number_input("RS_5 (%) От", value=None)
            with rs_5days2:
                rs_5days_max = st.number_input("RS_5 (%) До", value=None)

            # RS стандартный против индекса
            rs_standard1, rs_standard2 = st.columns(2)
            with rs_standard1:
                rs_standard_min = st.number_input("RS_14 (%) От", value=None)
            with rs_standard2:
                rs_standard_max = st.number_input("RS_14 (%) До", value=None)

            # RSI
            rsi1, rsi2 = st.columns(2)
            with rsi1:
                rsi_min = st.number_input("RSI От", value=None)
            with rsi2:
                rsi_max = st.number_input("RSI До", value=None)

            # Кнопка "Применить"
            apply_button = st.form_submit_button(label="Применить")


# Инициализация начальных условий фильтрации (True для всех строк)
filter_condition_df = pd.Series([True] * len(df))
filter_condition_df_1 = pd.Series([True] * len(df_1))

# Применение фильтров первого уровня
if date_1 is not None:
    date_1_dt = pd.to_datetime(date_1)
    filter_condition_df &= df['date'] >= date_1_dt
    filter_condition_df_1 &= df_1['year'] >= date_1_dt.year

if date_2 is not None:
    date_2_dt = pd.to_datetime(date_2)
    filter_condition_df &= df['date'] <= date_2_dt
    filter_condition_df_1 &= df_1['year'] <= date_2_dt.year

# Фильтрация по символам после группировки
df_group = df_1[filter_condition_df_1].groupby('symbol').mean()

if market_cap_min is not None:
    df_group = df_group[df_group['marketCap'] >= market_cap_min]
if market_cap_max is not None:
    df_group = df_group[df_group['marketCap'] <= market_cap_max]

# if std_min is not None:
#     df_group = df_group[df_group['std_rel'] >= std_min]
# if std_max is not None:
#     df_group = df_group[df_group['std_rel'] <= std_max]


if country == "кроме Китая":
    df_group = df_group[df_group['country'] == 0]
else:
    df_group = df_group[df_group['country'] == 1]

if volume is not None:
    df_group = df_group[df_group['Volume'] >= volume * 1000]

# Обновление условия фильтрации для df
filter_condition_df &= df['symbol'].isin(list(df_group.index))

if std_min is not None:
    filter_condition_df &= df['std_rel'] >= std_min
if std_max is not None:
    filter_condition_df &= df['std_rel'] <= std_max

# Применение фильтров второго уровня для df
if ps_min is not None:
    filter_condition_df &= df['filter_2_1'] >= ps_min
if ps_max is not None:
    filter_condition_df &= df['filter_2_1'] <= ps_max

if ds_min is not None:
    filter_condition_df &= df['filter_2_2'] >= ds_min
if ds_max is not None:
    filter_condition_df &= df['filter_2_2'] <= ds_max

if peg_min is not None:
    filter_condition_df &= df['PEG_TTM'] >= peg_min
if peg_max is not None:
    filter_condition_df &= df['PEG_TTM'] <= peg_max

if pe_min is not None:
    filter_condition_df &= df['filter_2_4'] >= pe_min
if pe_max is not None:
    filter_condition_df &= df['filter_2_4'] <= pe_max

if pe5_min is not None:
    filter_condition_df &= df['PE_TTM_5_mean'] >= pe5_min
if pe5_max is not None:
    filter_condition_df &= df['PE_TTM_5_mean'] <= pe5_max

# Применение фильтров третьего уровня для df
if volume_increase_min is not None:
    filter_condition_df &= df['Volume_metric'] >= volume_increase_min
if volume_increase_max is not None:
    filter_condition_df &= df['Volume_metric'] <= volume_increase_max

if rs_5days_min is not None:
    filter_condition_df &= df['RS_5'] >= rs_5days_min
if rs_5days_max is not None:
    filter_condition_df &= df['RS_5'] <= rs_5days_max

if rs_standard_min is not None:
    filter_condition_df &= df['RS_14'] >= rs_standard_min
if rs_standard_max is not None:
    filter_condition_df &= df['RS_14'] <= rs_standard_max

if rsi_min is not None:
    filter_condition_df &= df['RSI'] >= rsi_min
if rsi_max is not None:
    filter_condition_df &= df['RSI'] <= rsi_max

# Применение фильтрации к df и df_1
df_filtered = df[filter_condition_df]

# Переключатель для отображения графика Target_0
show_target_0 = st.toggle("Показать график для Исходных")

if show_target_0:
    # Отображение графика
    st.bar_chart(df_filtered['Target_0'].value_counts().reindex(range(-30, 31), fill_value=0), height=400)
    # Расчет среднего значения и стандартного отклонения
    mean_target = df_filtered['Target_0'].mean()
    std_target = df_filtered['Target_0'].std()
else:
    # Отображение графика для Target
    st.bar_chart(df_filtered['Target'].value_counts().reindex(range(-30, 31), fill_value=0), height=400)
    # Расчет среднего значения и стандартного отклонения
    mean_target = df_filtered['Target'].mean()
    std_target = df_filtered['Target'].std()

# Вывод количества отфильтрованных строк
st.write(f"Количество отфильтрованных данных: {len(df_filtered)}")

# Вывод среднего значения и стандартного отклонения
st.write(f"Среднее значение Target: {mean_target:.2f} %")
st.write(f"Стандартное отклонение Target: {std_target:.2f} %")
