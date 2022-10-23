import streamlit as st
import pandas as pd
import altair as alt
from urllib.error import URLError
import MySQLdb as my
import datetime


def conexao():
    con = my.connect(host='localhost',
                        user='Caio',
                        password='Caio123456@',
                        database='projeto_final')
    return con

def get_data(inst=''):
    con = conexao()
    cursor = con.cursor()

    sql = """SELECT ID_CLIENTES, NOME, BAIRRO, CIDADE, RUA, NUMERO,
            LIGACAO, MES_ATUAL, MES_01, MES_02,
            MES_03, MES_04, MES_05, MES_06, MES_07,
            MES_08, MES_09, MES_10, MES_11, MES_12
            FROM projeto_final.CLIENTES
            INNER JOIN projeto_final.CONSUMO
            on ID_CLIENTES = INSTALACAO
            WHERE ID_CLIENTES = '{}'
            """.format(inst)
    cursor.execute(sql)
    dados = pd.DataFrame(cursor.fetchall(), columns=['ID_CLIENTES', 'NOME', 'BAIRRO', 'CIDADE', 'RUA', 'NUMERO',
                    'LIGACAO', 'MES_ATUAL', 'MES_01', 'MES_02',
                    'MES_03', 'MES_04', 'MES_05', 'MES_06', 'MES_07',
                    'MES_08', 'MES_09', 'MES_10', 'MES_11', 'MES_12'])
    return dados



st.title("Projeto Final de Banco de Dados 👩‍💻")
st.subheader('Curva de Consumo')
st.sidebar.text('Alunos:')
st.sidebar.text('Caio Sóter\nPablo')


try:
    instalacao = st.text_input('Digite uma Instalação', key='name')
    chart_data = get_data(instalacao)
    chart_data = pd.melt(chart_data, id_vars=['ID_CLIENTES', 'NOME',
                                         'BAIRRO','CIDADE', 'RUA', 'NUMERO', 'LIGACAO'], value_name='CONSUMO(kWh)', var_name='MESES')
    coluna_data = [(datetime.date.today() - datetime.timedelta(days=i*30)).strftime('%Y-%m') for i in range(13)]
    chart_data['MESES_DATETIME'] = coluna_data
    
    if instalacao:
        st.write('Nome:', chart_data['NOME'][0])
        st.write('Endereço: {}, {}'.format(chart_data['RUA'][0], chart_data['NUMERO'][0]))
        st.write('Bairro: {}'.format(chart_data['BAIRRO'][0]))
        st.line_chart(chart_data, x='MESES_DATETIME', y='CONSUMO(kWh)')
except URLError as e:
    st.error('A aplicação necessita de internet!')










    







