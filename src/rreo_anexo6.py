import os
import requests
import time
import pandas as pd

DIR = "rreo06"

df_municipio = pd.read_excel(
    "cd_municipio_.xlsx",
    sheet_name="Sheet1",
    usecols=["cod_completo", "capital", "nome_municipio", "cd_uf"],
)


def extracao(ano: list, bimestres: list):
    cd_mun = df_municipio.cod_completo.to_list()
    mun = df_municipio.nome_municipio.to_list()

    for ano in ano:
        prev = f"PREVISÃO ATUALIZADA {ano}"
        coluna_corte = ["TOTAL (ÚLTIMOS 12 MESES)", prev]
        for bimestre in bimestres:
            # for cd_municipio, municipio in zip(cd_mun, mun):
            # print(f"Extraindo {municipio} - {bimestre} - {ano}.csv")
            url = (
                f"http://apidatalake.tesouro.gov.br/ords/siconfi/tt/rreo?an_exercicio={ano}"
                f"&nr_periodo={bimestre}&co_tipo_demonstrativo=RREO&no_anexo=RREO-Anexo%2006&id_ente=2611606"
            )
            print(url)
            r = requests.get(url)
            time.sleep(2)
            base = r.json()
            info = base["items"]
            result = pd.DataFrame(info)

            if info:
                result.to_csv(
                    f"{DIR}/dados/Recife_{ano}{bimestre}.csv", index=False, sep=";"
                )


def exporta_dataset(ano):
    arquivos = os.listdir(f"{DIR}/dados")
    df_list = list()

    for arquivo in arquivos:
        if arquivo.endswith(".csv"):
            if int(arquivo[-9:-5]) in ano:
                df = pd.read_csv(
                    f"{DIR}/dados/{arquivo}",
                    sep=";",
                )
                print(arquivo)
                df_list.append(df)

    df = pd.concat(df_list)

    df.to_csv(f"{DIR}/rreo_anexo6_stn.csv", sep=";", index=False)


if __name__ == "__main__":
    ano_lista = [2021, 2022]
    bimestre_lista = [1]
    extracao(ano_lista, bimestre_lista)
    exporta_dataset(ano_lista)
