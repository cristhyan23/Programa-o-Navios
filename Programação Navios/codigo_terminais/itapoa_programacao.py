import requests
import pandas as pd
from io import BytesIO
import warnings
from openpyxl import Workbook
from openpyxl.styles import NamedStyle

"""Classe que contem a geração de um Datframe com os dados do terminal portuário de Itapoa """


# Suppress the UserWarning
warnings.simplefilter("ignore")

# Create a default style and apply it to the workbook
default_style = NamedStyle(name='default')
Workbook.default_style = default_style

"""classe responsavel por gerar o data frame dos navios que estão programados para terminal de itapoa"""
class ProgramacaoItapoa:

    #função que captura o relatório em excel gerado pelo terminal portuário e faz tratativa no meso para salvar em um data frame
    def gerar_informacao_porto(self):
        url = "https://faturamento-n4-prod-k8s.portoitapoa.com/api/processos-n4/navios/programacao-exportar"
        headers = {
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJQb3J0byBJdGFwb8OhIiwic3ViIjoiaS5pdGFwb2F0ZXIuc2l0ZWluc3QiLCJpYXQiOjE2NDQwMDc3MzksImF1dGhvcml0aWVzIjpbIlVTRVIiXSwiZW1haWwiOiJ0aS1zaXN0ZW1hc0Bwb3J0b2l0YXBvYS5jb20uYnIiLCJjaGF2ZSI6Ik1BN1EySzZIWTZMMlFNWjEyS0VNIiwiY3BmIjoiMDc3ODEyNTI5NzciLCJub21lQ29tcGxldG8iOiJTaXRlIGluc3RpdHVjaW9uYWwgQVBJIiwiY25wakNsaWVudGVzVmlzaXZlaXMiOiIwNzc4MTI1MjktNzc7MDEzMTcyNzcwLTAwMTA1IiwiY25wakVtcHJlc2EiOiIwMTMxNzI3NzAwMDEwNSIsInBlcmZpbEFkbWluaXN0cmFkb3JQb3J0YWwiOmZhbHNlLCJwZXJmaWxzIjpbXSwiZXhwIjoxODAxNjg3NzM5fQ.8GtdUVU3mwzDr9H5HePwHMTDOAAFHwns9DcM-xkzRbs",
            "Origin": "https://www.portoitapoa.com",
            "Referer": "https://www.portoitapoa.com/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            # Carregue os dados do relatório em um DataFrame do pandas
            df = pd.read_excel(BytesIO(response.content))

            # Exclua todas as linhas em que a coluna 'status' tem a informação 'closed'
            df = df[~df['Status'].isin(['CLOSED', 'DEPARTED'])]
            df['Terminal'] = df.apply(lambda row: 'ITAPOA' if row['Navio'] != '' else "", axis=1)
            return df
        else:
            print(f"Erro ao acessar o relatório. Código de status: {response.status_code}")
            print(response.text)

