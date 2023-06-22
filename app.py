import streamlit as st
import pandas as pd
from src.SiconfiHandler import SiconfiHandler
import time

st.set_page_config(layout="wide")

def carrega_municipios():
    df_municipio = pd.read_excel('src/dicio/cd_municipio_.xlsx', sheet_name='Sheet1', usecols=['cod_completo', 'nome_municipio'])
    return df_municipio

def extract(anos, bimestres, documento, anexo, cod_entes, nome_entes):
    sh = SiconfiHandler()
    dfs = []
    for ano in anos:
        for bimestre in bimestres:
            for cod_ente, municipio in zip(cod_entes, nome_entes):
                sh.mount_url(ano, bimestre, documento, anexo, cod_ente, municipio)
                df = sh.receive_data()
                dfs.append(df)
                time.sleep(0.5)
    df = pd.concat(dfs)
    return df

@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

def main():
    st.title("Extrator de dados do Siconfi")

    # Seleções disponíveis
    #documentos = ['RREO', 'RGF', 'DCA', 'MSC - Patrimonial', 'MSC - Orçamentária', 'MSC - Controle']
    documentos = ['RREO', 'RGF']
    df_municipio = carrega_municipios()

    # Criando filtros
    with st.sidebar:
        st.title("Menu")
        st.markdown("Selecione os dados que deseja extrair")
        doc_sel = st.selectbox("Selecione o documento", options=documentos).lower()
        anos_sel = st.multiselect("Selecione o exercício", options=range(2015, 2024))
        bimestres_sel = st.multiselect("Selecione o período de referência (bimestre/quadrimestre)", options=range(1,7))
        mun_sel = st.multiselect("Selecione o ente", df_municipio.nome_municipio.unique())
        #esfera_sel = st.selectbox("Selecione a esfera", options=['M', 'E', 'U', 'C'])
        anexo_sel = st.selectbox("Selecione o anexo", options=['01', '02', '03', '04', '05', '06', '07', '10'])

    # Aplicando filtros de entes
    df_municipio = df_municipio[df_municipio['nome_municipio'].isin(mun_sel)]
    cd_mun_sel, mun_sel = df_municipio.cod_completo.to_list(), df_municipio.nome_municipio.to_list()

    if st.button("Extrair dados"):
        # Iniciando extração
        data = extract(anos_sel, bimestres_sel, doc_sel, anexo_sel, cd_mun_sel, mun_sel)
        st.write("Dados extraídos com sucesso!")
        st.write(f"### {doc_sel}")
        st.dataframe(data)
        # botão para download
        csv = convert_df(data)

        st.download_button(
            label="Exportar",
            data=csv,
            file_name=f'{doc_sel}-{anexo_sel}.csv',
            mime='text/csv',
        )

main()

