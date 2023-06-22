import requests
import pandas as pd
import time
import json

df_municipio = pd.read_excel('cd_municipio.xlsx', sheet_name='Sheet1', usecols=['cod_completo', 'nome_municipio'])

cd_mun = df_municipio.cod_completo.to_list()
mun = df_municipio.nome_municipio.to_list()

for ano in [2022]:
    for quadrimestre in [3]:
        for cd_municipio, municipio in zip(cd_mun, mun):
            print(f"Extraindo {municipio} - {quadrimestre} - {ano}.csv")
            url = f"http://apidatalake.tesouro.gov.br/ords/siconfi/tt/rgf?an_exercicio={ano}" \
                  f"&in_periodicidade=Q&nr_periodo={quadrimestre}&co_tipo_demonstrativo=RGF&no_anexo=RGF" \
                  f"-Anexo%2001&co_esfera=M&co_poder=E&id_ente={cd_municipio}"

            print(url)

            r = requests.get(url)
            base = json.loads(r.text)
            info = base['items']
            df = pd.DataFrame(info)
            time.sleep(5)

            df.to_excel(f"_rgf_1\\rgf_1_{municipio}_{quadrimestre}_{ano}.xlsx")
