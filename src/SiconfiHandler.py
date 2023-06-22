import requests
import pandas as pd
import json

class SiconfiHandler:
    def __init__(self):
        self.base_url = 'https://apidatalake.tesouro.gov.br/ords/siconfi/tt/'
        
        # baseado na seguinte url, crie uma classe que faça a requisição para diferentes seleções
    def mount_url(
            self,
            ano:int, 
            bimestre:int,
            relatorio:str, 
            cd_anexo:str, 
            cd_municipio:str,
            nm_municipio:str,
            cd_esfera:str = 'M',
            debug=False, 
            ):
        relatorio = relatorio.upper()
        print(f"Extraindo {nm_municipio} - {bimestre} - {ano} ANEXO {cd_anexo}")
        self.mounted_url = self.base_url + f"rreo?an_exercicio={ano}" \
                  f"&nr_periodo={bimestre}&co_tipo_demonstrativo={relatorio}&no_anexo={relatorio}" \
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
        

