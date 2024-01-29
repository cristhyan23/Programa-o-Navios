import requests
import pandas as pd

"""Classe que contem a geração de um Datframe com os dados do terminal portuário de Salvador Wilson"""
class ProgramacaoTecon:

    # função para acessar as informações do terminal via request
    def acesso_escala(self):

        # URL da solicitação
        url = 'https://api.teconline.com.br/API/ProgNavio'
        # Definir o método de solicitação
        method = 'GET'
        params = {
        'situacao': ['Programado','Em operação','Atracado','Em espera'],
        'isBerth':'true',
        'tamanhoPagina': 10000
        }

        try:
            # Fazer a solicitação GET
            response = requests.request(method, url, params=params, timeout=300)
            response.raise_for_status()

            # Verificar a resposta da solicitação
            if response.status_code == 200:
                # A solicitação foi bem-sucedida
                objeto_lista = response.json().get('Data', [])
                for objeto_dict in objeto_lista:
                    if objeto_dict.get('NavioNome') == 'TRANSITO RODOVIARIO':
                        objeto_lista.remove(objeto_dict)
                    elif objeto_dict.get('Tipo') != 'Longo Curso':
                        objeto_lista.remove(objeto_dict)
                    else:
                        # Não é necessário fazer nada, pois você já está iterando sobre a lista original
                        pass

                return objeto_lista
            else:
                raise Exception(f"Request failed with status code: {response.status_code}")
        except Exception as e:
            print(f"Erro: {e}")

    # função que trata a informação e gera um data frame
    def gerar_informacao_porto(self):
        # Obter a lista de escala
        lista_escala = self.acesso_escala()

        # Verificar se a lista é válida antes de prosseguir
        if lista_escala:
            # Criar um DataFrame do pandas
            df = pd.DataFrame(lista_escala)
            df['Terminal'] = df.apply(lambda row: 'SALVADOR' if row['NavioNome'] != '' else "", axis=1)

            return df
        else:
            print("Não foi possível obter dados válidos para a lista de escala.")


