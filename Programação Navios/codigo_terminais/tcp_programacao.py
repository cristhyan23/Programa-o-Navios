import requests
from datetime import datetime
import pandas as pd

"""Classe que contem a geração de um Datframe com os dados do terminal portuário de TCP Paranagua"""
class ProgramacaoTCP:


#Função para consultar via request a escala do terminal
    def acesso_escala(self):
        # Obter a data atual
        data_inicial = datetime.today()

        # Formatar a data no formato necessário para a solicitação GET
        data_inicial_str = data_inicial.strftime('%Y-%m-%dT%H:%M:%S.000Z')

        # URL da solicitação
        url = "https://api.tcp.com.br/legado/N4Api/api/PortalProgramacaoNavio"

        # Definir o método de solicitação
        method = "GET"

        # Definir os parâmetros da solicitação
        params = {
            'IncluirObsoletos': 'false',
            'TamanhoPagina': '10',
            'SentidoOrdenacao': '1',
            'PaginaAtual': '1',
            'Ordenacao': 'PrevisaoAtracacao',
            'Situacao': ['ATRACADO', 'PREVISTO', 'EM OPERACAO'],
            'DataInicial': data_inicial_str
        }

        try:
            # Fazer a solicitação GET
            response = requests.request(method, url, params=params, timeout=300)
            response.raise_for_status()

            # Verificar a resposta da solicitação
            if response.status_code == 200:
                # A solicitação foi bem-sucedida

                objeto_lista = response.json().get('Objeto', [])
                for objeto_dict in objeto_lista:
                    if objeto_dict.get('Situacao') == 'CANCELADO':
                        objeto_lista.remove(objeto_dict)
                    else:
                        # Não é necessário fazer nada, pois você já está iterando sobre a lista original
                        pass
                return objeto_lista
            else:
                raise Exception(f"Request failed with status code: {response.status_code}")
        except Exception as e:
            print(f"Erro: {e}")

#função para fazer a conversão das datas que retorna ano-mes-dia para dia/mes/ano
    def converter_datas(self, pesquisa):
        # Função para ajustar como é o formato da data
        def converter_data(data):
            if data:
                data_obj = datetime.strptime(data, "%Y-%m-%dT%H:%M:%S")
                data_real = data_obj.strftime("%d/%m/%Y %H:%M:%S")
                return data_real
            else:
                return data

        # Aplicar a função de conversão aos campos relevantes
        campos_para_converter = ['DeadLine','ChegadaEstimada','ChegadaBarra','PrevisaoAtracacao','PrevisaoSaida','BWStarting']

        # Aplicar a função de conversão às colunas relevantes
        for campo in campos_para_converter:
            pesquisa[campo] = pesquisa[campo].apply(converter_data)

        return pesquisa

# função que recebe as informações de acesso escala e converte em um data frame tambem acessa a converter datas para ajuste das datas
    def gerar_informacao_porto(self):
        # Obter a lista de escala
        lista_escala = self.acesso_escala()

        # Verificar se a lista é válida antes de prosseguir
        if lista_escala:
            # Criar um DataFrame do pandas
            df = pd.DataFrame(lista_escala)
            df = self.converter_datas(df)
            df['Terminal'] = df.apply(lambda row: 'TCP' if row['Navio'] != '' else "", axis=1)
            # Construir o caminho completo do arquivo Excel usando pathlib

            return df
        else:
            print("Não foi possível obter dados válidos para a lista de escala.")



