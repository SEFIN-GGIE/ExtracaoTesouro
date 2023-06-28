import requests
import pandas as pd
import time
import json

df_municipio = pd.read_excel(
    "cd_municipio.xlsx", sheet_name="Sheet1", usecols=["cod_completo", "nome_municipio"]
)

cd_mun = df_municipio.cod_completo.to_list()
mun = df_municipio.nome_municipio.to_list()

for ano in [2022]:
    for cd_municipio, municipio in zip(cd_mun, mun):
        print(f"Extraindo {municipio} - {ano}.csv")
        url = (
            f"https://apidatalake.tesouro.gov.br/ords/siconfi/tt/dca?an_exercicio={ano}"
            f"&no_anexo=DCA-Anexo%20I-AB&id_ente={cd_municipio}"
        )

        r = requests.get(url)
        base = json.loads(r.text)
        info = base["items"]
        df = pd.DataFrame(info)
        time.sleep(5)

        df.to_excel(f"_dca_iab\\_dca_iab_{municipio}_{ano}.xlsx")
