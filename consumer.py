import pandas as pd
from src.SiconfiHandler import SiconfiHandler
from configs import configuracao_extracao
import time

def extract(anos, bimestres, relatorio, anexo, cod_entes, nome_entes, file_name):
    sh = SiconfiHandler()
    dfs = []
    for ano in anos:
        for bimestre in bimestres:
            for cod_ente, municipio in zip(cod_entes, nome_entes):
                sh.mount_url(ano, bimestre, relatorio, anexo, cod_ente, municipio)
                df = sh.receive_data()
                dfs.append(df)
                time.sleep(0.5)
    df = pd.concat(dfs)
    df.to_csv(f'processed/{relatorio}/{file_name}.csv', index=False, decimal=',', sep=';')

if __name__ == '__main__':

    # CONFIGURAÇÃO
    ANEXO = configuracao_extracao['ANEXO']
    ANOS = configuracao_extracao['ANOS']
    BIMESTRES = configuracao_extracao['BIMESTRES']
    COD_MUNICIPIOS = configuracao_extracao['COD_MUNICIPIOS']
    NOMES_MUNICIPIOS = configuracao_extracao['NOMES_MUNICIPIOS']
    NOME_ARQUIVO = configuracao_extracao['NOME_ARQUIVO']
    RELATORIO = configuracao_extracao['RELATORIO']

    # EXTRACAO
    extract(ANOS, BIMESTRES, RELATORIO, ANEXO, COD_MUNICIPIOS, NOMES_MUNICIPIOS, NOME_ARQUIVO)
    