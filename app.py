import streamlit as st
import pandas as pd
from src.SiconfiHandler import SiconfiHandler
import time

st.set_page_config(layout="wide")

def carrega_municipios():
    df_municipio = pd.read_excel('src/dicio/cd_municipio_.xlsx', sheet_name='Sheet1', usecols=['cod_completo', 'nome_municipio'])
    return df_municipio

def extract_data(documento, anos_sel, cd_mun_sel, mun_sel, anexo_sel, esfera_sel):
    sh = SiconfiHandler()
    data = list()
    
    for ano in anos_sel:
        for cd_municipio, municipio in zip(cd_mun_sel, mun_sel):
            for bimestre in range(1, 7):
                if documento == 'RREO':
                    sh.mount_rreo(ano, bimestre, anexo_sel, cd_municipio, municipio, esfera_sel, debug=True)
                df = sh.receive_data()
                data.append(df)
                time.sleep(0.5)
    concat_data = pd.concat(data)

    return concat_data

@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')


def main():
    st.title("Extrator de dados do Siconfi")

    # Seleções disponíveis
    documentos = ['RREO', 'RGF', 'DCA', 'MSC - Patrimonial', 'MSC - Orçamentária', 'MSC - Controle']
    df_municipio = carrega_municipios()

    # Criando filtros
    st.title("Menu")
    st.markdown("Selecione os dados que deseja extrair")
    doc_sel = st.selectbox("Selecione o documento", options=documentos)
    anos_sel = st.multiselect("Selecione o periodo", options=range(2015, 2024))
    mun_sel = st.multiselect("Selecione o ente", df_municipio.nome_municipio.unique())
    esfera_sel = st.selectbox("Selecione a esfera", options=['M', 'E', 'U', 'C'])
    anexo_sel = st.selectbox("Selecione o anexo", options=['01', '02', '03', '04', '05', '06', '07', '10'])

    # Aplicando filtros de entes
    df_municipio = df_municipio[df_municipio['nome_municipio'].isin(mun_sel)]
    cd_mun_sel, mun_sel = df_municipio.cod_completo.to_list(), df_municipio.nome_municipio.to_list()

    if st.button("Extrair dados"):
        # Iniciando extração
        data = extract_data(doc_sel, anos_sel, cd_mun_sel, mun_sel, anexo_sel, esfera_sel)
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

