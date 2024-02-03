import requests
from datetime import datetime
import pandas as pd

"""Classe que contem a geração de um Datframe com os dados do terminal portuário de Santos BTP """
class ProgramacaoBTP:

    def acesso_escala(self):
        data_inicial = datetime.today()
        data_inicial_str = data_inicial.strftime('%d/%m/%Y')

        url = "https://tas.btp.com.br/ConsultasLivres/ListaAtracacao"

        # Headers
        headers = {
            "authority":'tas.btp.com.br',
            "method":"POST",
            "path":"/ConsultasLivres/ListaAtracacao",
            "scheme":"https",
            "__requestverificationtoken":"Wn4DmqK_5fcqk2-dlbICuhnlkIG1MGyFv_K65bai54Vr5VGFWWGWp7ODr1nZqh7h40BvYPzTkcSIZ98_pwfMsWTOsDRH2gsCAGlpKkp1169ZD1QU2jIuzDIBnMyJvVwOjTTrX--XRFOhb2H2PUcj-A2:OrdPC-uzSpL2_VG-JiqbfraJyXU292ojo7V0lW1mdMJQTXY20-RQu3i2PX25ANi3m7DUAh89nYI3gWi13JBemEPiYDB9zZz8gWMCieMWtOHdMfVpwqM7ysUAAAy3mocmpd6sDPkpgmAnkVZzXWUbTXwXMhGfh7uySVYMgVurJDs1",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9,pt-BR;q=0.8,pt;q=0.7,de-DE;q=0.6,de;q=0.5,es-ES;q=0.4,es;q=0.3,fr-FR;q=0.2,fr;q=0.1",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": "https://tas.btp.com.br",
            "Referer": "https://tas.btp.com.br",
            "Sec-Ch-Ua": "\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"120\", \"Google Chrome\";v=\"120\"",
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": "\"Windows\"",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
        }

        # Form data
        data = {
            "dias": "0",
            "tpPesquisa": "0",
            "dtInicial": data_inicial_str ,
            "dtFinal": "",
            "id": "",
        }

        # Cookies
        cookies = {
            "TAS_SessionId": "fwduvpqk25zqddeau1uxbmgi",
            "_gid": "GA1.3.1719045680.1706177849",
            "_ga": "GA1.1.1027923941.1700770676",
            "_ga_GCK1HKXQYX": "GS1.1.1706177848.3.1.1706177929.60.0.0",
        }
        try:
            # Make the request
            response = requests.post(url, headers=headers, data=data)
            if response.status_code == 200:
                # A solicitação foi bem-sucedida
                objeto_lista = response.json().get('Records',[])
                return objeto_lista
            else:
                raise Exception(f"Request failed with status code: {response.status_code}")
        except Exception as e:
            print(f"Erro: {e}")

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
        campos_para_converter = ['Chegada', 'PrevisaoAtracacao', 'Atracacao', ]

        # Aplicar a função de conversão às colunas relevantes
        for campo in campos_para_converter:
            pesquisa[campo] = pesquisa[campo].apply(converter_data)

        return pesquisa

    def gerar_informacao_porto(self):
        # Obter a lista de escala
        lista_escala = self.acesso_escala()

        # Verificar se a lista é válida antes de prosseguir
        if lista_escala:
            # Criar um DataFrame do pandas
            df = pd.DataFrame(lista_escala)
            df = self.converter_datas(df)
            df['Terminal'] = df.apply(lambda row: 'BTP' if row['Navio'] != '' else "", axis=1)
            # Construir o caminho completo do arquivo Excel usando pathlib
            return df
        else:
            print("Não foi possível obter dados válidos para a lista de escala.")

