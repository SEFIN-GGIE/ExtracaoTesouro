import requests
import pandas as pd
import json

class SiconfiHandler:
    def __init__(self):
        self.base_url = 'https://apidatalake.tesouro.gov.br/ords/siconfi/tt/'
        
        # baseado na seguinte url, crie uma classe que faça a requisição para diferentes seleções
    def mount_rreo(
            self,
            ano:int, 
            bimestre:int, 
            cd_anexo:str, 
            cd_municipio:str,
            nm_municipio:str,
            cd_esfera:str = 'M',
            debug=False, 
            ):
        print(f"Extraindo {nm_municipio} - {bimestre} - {ano}.csv")
        self.mounted_url = self.base_url + f"rreo?an_exercicio={ano}" \
                  f"&nr_periodo={bimestre}&co_tipo_demonstrativo=RREO&no_anexo=RREO" \
                  f"-Anexo%20{cd_anexo}&co_esfera={cd_esfera}&id_ente={cd_municipio}"
        if debug:
            print(self.mounted_url)

    def receive_data(self):
        try:
            r = requests.get(self.mounted_url)
        except Exception as e:
            print(e)
            return None
        base = json.loads(r.text)
        info = base['items']
        df = pd.DataFrame(info)
        
        return df
        

