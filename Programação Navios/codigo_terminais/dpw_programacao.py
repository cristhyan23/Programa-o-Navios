import requests
from datetime import datetime, timedelta
import pandas as pd


"""Classe que contem a geração de um Datframe com os dados do terminal portuário de Santos DPW """

class ProgramacaoDPW:

    """Função faz a busca no site da DPW santos de todos os barcos que estão com escala prevista para esse porto"""
    def acesso_consulta_escala_prevista(self):
        data_inicial = datetime.today()
        data_inicial_str = data_inicial.strftime('%d/%m/%Y')
        data_final = data_inicial + timedelta(days=21)
        data_final_str = data_final.strftime('%d/%m/%Y')

        url = "http://www.embraportonline.com.br/Navios/buscarEscalaPesquisa"

        # Define the payload with the required parameters
        payload = {
            'prNroOperacao': '',
            'prDataInicial': data_inicial_str,
            'prDataFinal': data_final_str,
            'prArmador': '',
            'prServico': '',
            'skipresult': '0',
            'takeresult': '10'
        }

        # Define headers
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.9,pt-BR;q=0.8,pt;q=0.7,de-DE;q=0.6,de;q=0.5,es-ES;q=0.4,es;q=0.3,fr-FR;q=0.2,fr;q=0.1',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': 'www.embraportonline.com.br',
            'Origin': 'http://www.embraportonline.com.br',
            'Referer': 'http://www.embraportonline.com.br/Navios/Escala',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }

        # Make the POST request
        response = requests.post(url, data=payload, headers=headers)

        # Check the response
        if response.status_code == 200:
            # Print the response content
            return response.json()
        else:
            print(f"Request failed with status code: {response.status_code}")
            print(response.text)

    """Função faz a busca no site da DPW santos de todos os barcos que estão em operação escala prevista para esse porto"""
    def acesso_consulta_escala_em_operacao(self):
        data_inicial = datetime.today()
        data_inicial_str = data_inicial.strftime('%d/%m/%Y')
        data_final = data_inicial + timedelta(days=21)
        data_final_str = data_final.strftime('%d/%m/%Y')

        url = "http://www.embraportonline.com.br/Navios/getEscalaEmOperacao"

        # Define the payload with the required parameters
        payload = {
            'prDataInicial': data_inicial_str,
            'prDataFinal': data_final_str,
            'skipresult': '0',
            'takeresult': '10'
        }

        # Define headers
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.9,pt-BR;q=0.8,pt;q=0.7,de-DE;q=0.6,de;q=0.5,es-ES;q=0.4,es;q=0.3,fr-FR;q=0.2,fr;q=0.1',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': 'www.embraportonline.com.br',
            'Origin': 'http://www.embraportonline.com.br',
            'Referer': 'http://www.embraportonline.com.br/Navios/Escala',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }

        # Make the POST request
        response = requests.post(url, data=payload, headers=headers)

        # Check the response
        if response.status_code == 200:
            # Print the response content
            return response.json()
        else:
            print(f"Request failed with status code: {response.status_code}")
            print(response.text)

    # função que faz a converção das datas para manter um padrão dd/mm/aaaa
    def converter_datas(self, pesquisa):
        # Função para converter datas no formato \/Date(1706198400000)\/ para DD/MM/AAAA HH:MM
        def converter_data(data):
            if data and data.startswith('/Date('):
                data_em_milissegundos = data.replace("/Date(", "").replace(")/", "")
                data_em_segundos = int(data_em_milissegundos) / 1000
                data_real = datetime.utcfromtimestamp(data_em_segundos)
                return data_real.strftime('%d/%m/%Y %H:%M')
            else:
                return data

        # Aplicar a função de conversão aos campos relevantes
        campos_para_converter = ['ETA', 'ETD', 'AberturaGate','ReeferDeadline','DryDeadline','PrevisaoChegada']

        # Aplicar a função de conversão às colunas relevantes
        for campo in campos_para_converter:
            pesquisa[campo] = pesquisa[campo].apply(converter_data)

        return pesquisa


    """Une as 2 operações e salva um excel na mesma pasta que está salvo o arquivo py"""
    def gerar_informacao_porto(self):
        lista_prevista = self.acesso_consulta_escala_prevista()
        lista_operacao = self.acesso_consulta_escala_em_operacao()

        # Usar extend para adicionar os elementos da segunda lista à primeira
        lista_prevista.extend(lista_operacao)
        if lista_prevista:
            df = pd.DataFrame(lista_prevista)
            df = self.converter_datas(df)
            df['Terminal'] = df.apply(lambda row: 'DPW' if row['NAVIO'] != '' else "", axis=1)
            # Construir o caminho completo do arquivo Excel usando pathlib

            return df
        else:
            print("Não foi possível obter dados válidos para a lista de escala.")

