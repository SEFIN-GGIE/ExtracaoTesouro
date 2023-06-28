import requests
import pandas as pd
import time
import json

df_municipio = pd.read_excel(
    "dicio/cd_municipio_.xlsx",
    sheet_name="Sheet1",
    usecols=["cod_completo", "nome_municipio"],
)

cd_mun = df_municipio.cod_completo.to_list()
mun = df_municipio.nome_municipio.to_list()

lista_dfs = []

for ano in range(2018, 2024):
    for cd_municipio, municipio in zip(cd_mun, mun):
        for bimestre in [1, 2, 3, 4, 5, 6]:
            print(f"Extraindo {municipio} - {bimestre} - {ano}.csv")
            url = (
                f"https://apidatalake.tesouro.gov.br/ords/siconfi/tt/rreo?an_exercicio={ano}"
                f"&nr_periodo={bimestre}&co_tipo_demonstrativo=RREO&no_anexo=RREO"
                f"-Anexo%2003&co_esfera=M&id_ente={cd_municipio}"
            )

            try:
                r = requests.get(url)
            except:
                continue

            base = json.loads(r.text)
            info = base["items"]
            df = pd.DataFrame(info)
            time.sleep(1)
            lista_dfs.append(df)

dataframes = pd.concat(lista_dfs)

dataframes.to_csv(
    f"../processed/rreo/rreo_3_capitais_2015_2023.csv",
    sep=";",
    index=False,
    decimal=",",
)
