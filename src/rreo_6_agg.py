import requests
import pandas as pd
import time
import json

lista_tabs = list()

for ano in [2022, 2023]:
    for ente in [2611606]:
        for periodo in [1, 2, 3, 4, 5, 6]:

            url = f"https://apidatalake.tesouro.gov.br/ords/siconfi/tt/rreo?an_exercicio={ano}&nr_periodo={periodo}&co_tipo_demonstrativo=RREO&no_anexo=RREO-Anexo%2006&co_esfera=M&id_ente={ente}"
            print(f"Consultando dados de {ente} do ano de {ano} e periodo {periodo}")
        
            # pega dados do sincofi
            r = requests.get(url, verify=False)
            # pausa de 3s
            time.sleep(3)
            # estrutura os dados em json
            base = json.loads(r.text)
            # os dados que queremos se encontram na chace 'items' desse json
            info = base['items']
            # de json para tablea (datataframe)
            result = pd.DataFrame(info)
            # cria uma lista com as tabelas de cada ano
            lista_tabs.append(result)

    # junta todas as tabelas
    dataframes = pd.concat(lista_tabs)

    # salva o "tabelão" no drive
    dataframes.to_csv("rreo_anexo_06_capitais.csv", sep=";", index=False, decimal=",")