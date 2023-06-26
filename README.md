# ExtracaoTesouro

Extração de dados abertos da Secretaria do Tesouro Nacional (Siconfi).

## Índice
- Visão Geral
- Tecnologias
- Instalação
- Uso
- Contribuição
- Licença
## Visão Geral
Este projeto realiza a extração de dados abertos da Secretaria do Tesouro Nacional, com finalidades de análise e Business Intelligence a partir dos dados orçamentários. Todo o consumo é realizado a partir da API do Siconfi, disponível em [SICONFI API](https://apidatalake.tesouro.gov.br/docs/siconfi/#/DCA/get_dca)

## Tecnologias

- Python
- Streamlit

## Instalação

Clone o repositório:

```bash
git clone https://github.com/seu-usuario/seu-projeto.git
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

## Usabilidade

O módulo pode ser utilizado de 3 formas:

1. Consultas manuais e executadas localmente;
2. Consultas manuais executadas por webapp;
3. Consultas agendadas; (A DESENVOLVER)
   
### 1 - Consultas locais.
As consultas manuais e locais devem ser configuradas no arquivo `configs.py`. As configurações definidas no arquivo serão lidas pelo `consumer.py` no momento de realizar a consulta e enviar as requisições à API do Siconfi.

### 2 - Consultas no webapp.

As consultas no webapp são de fácil usabilidade para usuários não técnicos por meio da interface gráfica do frameowrk streamlit. O acesso ao app é feito pelo [link](https://extracao-siconfi.streamlit.app/). Para execuções locais, precisa-se instalar o streamlit no ambiente de execução disponível nos requerimentos, e a partir daí, executar o comando:

```bash
streamlit run app.py
```

### 3 - Consultas Agendadas.

As consultas agendadas serão desenvolvidas e integradas ao módulo do DataHub. As consultas serão agendadas e executadas por meio de cronjobs, tendo dados armazenados em um banco de dados PostgreSQL e visualização por meio de Plotly Dash.