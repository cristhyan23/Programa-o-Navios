import requests
import pandas as pd
from datetime import datetime

"""Classe que contem a geração de um Datframe com os dados do terminal portuário de Portonave Navegantes"""

class ProgramacaoPortonave:

    #função que captura as informações dos navios atracados no porto
    def consultar_navios_atracados(self):
        # Defina a URL da solicitação e os cabeçalhos necessários
        url = "https://extranet.portonave.com.br/lineup/list/atracados"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Cookie": "www.portonave.com.br.x-csrf-token=s%3A14427cf3c2b9df4359106a3e0be9c37388704ce33e485c663a9126ccce8e9570.FL45FmPAQ785FNya5mRZPQ7HPIEj%2FaVmiJ6%2F%2FVRfUg0",
        }
        # Faz a solicitação à API
        response = requests.get(url, headers=headers)

        # Verifica se a solicitação foi bem-sucedida (código de status 200)
        if response.status_code == 200:
            # Converte a resposta JSON em um dicionário
            dados_json = response.json()

            # Retorna o dicionário resultante
            return dados_json
        else:
            # Se a solicitação falhar, imprime informações de erro
            print(f"Erro ao acessar a API. Código de status: {response.status_code}")
            print(response.text)
            return None

    # função que captura a informaçõs do navio em programação
    def consultar_navios_esperados(self):
        # Defina a URL da solicitação e os cabeçalhos necessários
        url = "https://extranet.portonave.com.br/lineup/list/esperados"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Cookie": "www.portonave.com.br.x-csrf-token=s%3A14427cf3c2b9df4359106a3e0be9c37388704ce33e485c663a9126ccce8e9570.FL45FmPAQ785FNya5mRZPQ7HPIEj%2FaVmiJ6%2F%2FVRfUg0",
        }
        # Faz a solicitação à API
        response = requests.get(url, headers=headers)

        # Verifica se a solicitação foi bem-sucedida (código de status 200)
        if response.status_code == 200:
            # Converte a resposta JSON em um dicionário
            dados_json = response.json()

            # Retorna o dicionário resultante
            return dados_json
        else:
            # Se a solicitação falhar, imprime informações de erro
            print(f"Erro ao acessar a API. Código de status: {response.status_code}")
            print(response.text)
            return None

    # função para converter as datas para o padrão dd/mm/aaaa
    def converter_datas(self, pesquisa):
        # Função para ajustar como é o formato da data
        def converter_data(data):
            if not data:
                return None

            try:
                # Tentar converter para datetime incluindo fração de segundos
                data_obj = datetime.strptime(data, "%Y-%m-%d %H:%M:%S.%f")
                data_real = data_obj.strftime("%d/%m/%Y %H:%M:%S")
            except ValueError:
                # Se falhar, tentar converter sem fração de segundos
                data_obj = datetime.strptime(data, "%Y-%m-%d %H:%M:%S")
                data_real = data_obj.strftime("%d/%m/%Y %H:%M:%S")

            return data_real

        # Aplicar a função de conversão aos campos relevantes
        campos_para_converter = ['ATRACACAO_PREVISTA','SAIDA','DRY','DEADLINE','CHEGADA_PREVISTA','CHEGADA','REEFER']

        # Aplicar a função de conversão às colunas relevantes
        for campo in campos_para_converter:
            pesquisa[campo] = pesquisa[campo].apply(converter_data)

        return pesquisa

    # função para unir os navios atracados e navios esperados e salvar em um data frame
    def gerar_informacao_porto(self):
        lista_prevista = self.consultar_navios_esperados()
        lista_operacao = self.consultar_navios_atracados()

        # Usar extend para adicionar os elementos da segunda lista à primeira
        lista_prevista.extend(lista_operacao)
        #caminho para salvar arquivo

        if lista_prevista:
            df = pd.DataFrame(lista_prevista)
            df = self.converter_datas(df)
            df['Terminal'] = df.apply(lambda row: 'PORTONAVE' if row['NOME_NAVIO'] != '' else "", axis=1)
            # Construir o caminho completo do arquivo Excel usando pathlib

            # Escrever para Excel

            return df
        else:
            print("Não foi possível obter dados válidos para a lista de escala.")

