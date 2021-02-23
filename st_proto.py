import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import pearsonr
from statsmodels.sandbox.stats.multicomp import multipletests 
import seaborn as sns
import plotly as py
import plotly.graph_objs as go
import plotly.express as px
import matplotlib.pyplot as plt
#https://medium.com/@u.praneel.nihar/building-multi-page-web-app-using-streamlit-7a40d55fa5b4
st.sidebar.title('Navigation')
selection = st.sidebar.radio("Go to", ['Сводный индекс','Визуализация исходных данных', 'Поиск взаимосвязей', 'О проекте'])
if selection == 'Сводный индекс':
	st.header('Сводный индекс эпидемической обстановки')
	sum_cor2=pd.read_excel('data/index_correlated.xlsx')
	fig2 = px.scatter(sum_cor2, x='month', y="relative",
	     size="relative", hover_name=sum_cor2.month,color_discrete_sequence=px.colors.diverging.RdYlBu, 
	                 color='relative', log_y=True, size_max=100,  hover_data=['absolute'])
	st.plotly_chart(fig2)
	st.markdown('Absolute - общее количество коррелирующих с ковидом запросов за месяц')
	st.markdown('Reative - относительное количество запросов, по сравнению с максимумом')
	corr_data=pd.read_excel('data/only_correlated_data.xlsx', index_col='month')
	st.write('Помесячное количество коррелирующих запросов ', corr_data)
if selection == 'О проекте':
	st.header('О проекте')
	st.markdown('Цель данного проекта: поиск математической устойчивой взаимосвязи между релевантной поисковой статистикой россиян и динамикой заболеваемости COVID-19 в РФ')
	st.markdown('Для анализа поисковой статистики использовался перечень симптомов и названий лекарств связанных с протоколом лечения COVID-19')
	st.markdown('Найденные взаимосвязи указывают на то, что поисковая статистика может указывать на понижение или повышение количества людей заболевших COVID-19')
	st.markdown('Данные заболевмаемости/смертности от COVID-19 были получены на сайте www.lll..www')
	st.markdown('Данный проект реализован в рамках квалификационной выпускной работы программы MBA Цифровая Экономика 2019-2021, МФТИ и МГИМО')
	st.markdown('Авторы проекта: А. Батрименко, С. Денисова')
	st.markdown('Научный руководитель: С. Сошников')
	st.markdown('>Используйте меню слева для перехода на другие страницы сайта')
if selection == 'Визуализация исходных данных':
	df_cov_sc=pd.read_excel('data/scaled_data.xlsx')
	fig = px.line(df_cov_sc, x='month', y='value', color='query', hover_name="query").for_each_trace(lambda t: t.update(name=t.name.split("=")[1]))
	fig.update_traces(mode='markers+lines')
	fig.update_layout(legend_traceorder="reversed")
	st.header('Визуализация данных')
	st.write('Ниже представлены графики релевантной поисковой семантики и случаев заражения covid-19 и смертей')
	st.header('Масштабированные данные')
	st.write('Данные были нормированы для приведения к одному масштабу, с помощью инструмента MinMaxScaler изsklearn')
	st.plotly_chart(fig)
	st.markdown('>Нажмите дважды в области легенды графика чтобы отключить все графики')
	st.markdown('>Включайте/выключайте одним кликом любой компонент график или набор графиков для сравнения')
	st.header('Графики абсолютных значений')
	df_cov=pd.read_excel('data/month_russia_data.xlsx', sheet_name='query')
	fig = px.line(df_cov, x='month', y='value', color='query', hover_name="query").for_each_trace(lambda t: t.update(name=t.name.split("=")[1]))
	fig.update_traces(mode='markers+lines')
	fig.update_layout(legend_traceorder="reversed")
	st.plotly_chart(fig)
if selection == 'Поиск взаимосвязей':
	st.header('Поиск взаимосвязей. Методика расчета')
	st.markdown("""Для поиска связей в данных были подготовленны датасеты помесячных данных релевантной поисковой статистики и статистики COVID-19<br>
    Далее, был проведен поиск корреляций Пирсона между всеми наборами данных данного датасета<br>
    И к полученным результатам применена поправка Бенджамини-Хохберга на множественную проверку гипотез, для повышения надежности результатов. <br>
    Подтвержденные значения корреляций показаны ниже. 
    """, unsafe_allow_html=True)
	df_cov_true=pd.read_excel('data/corr_true_data.xlsx')
	st.write(df_cov_true)
	st.markdown("""corr - значение корреляции пирсона между A и B<br>
				p - первичный уровень значимости для данной пары<br>
				p_corrected - скорректированный уровень значимости для данной пары
	""", unsafe_allow_html=True)
	st.header('Построчный анализ подтвержденных корреляций')
	zz=pd.unique(df_cov_true.A)
	option = st.selectbox('Выберите строки для анализа',zz)
	#st.write('You selected:', option)
	data=df_cov_true.loc[df_cov_true.A ==option]
	st.write('Все подтвержденные корреляции для %s' % option, data)
