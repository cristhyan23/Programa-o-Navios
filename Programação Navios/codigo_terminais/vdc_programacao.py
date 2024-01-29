import pandas as pd
from playwright.sync_api import sync_playwright
import json
from datetime import datetime

"""Classe que contem a geração de um Datframe com os dados do terminal portuário de Vila do Conde"""
class ProgramacaoVDC:

    # Função para consultar via playwright a escala do terminal previsto chegada
    def acesso_escala(self):
        data_inicial = datetime.today()
        data_inicial_str = data_inicial.strftime('%Y-%m-%d')
        url = f"https://www.santosbrasil.com.br/v2021/mooring-list/pesquisa?unidade=tecon-vila-do-conde&lista=recebimento-de-exportacao&atracadouro=TECON&pesquisa=&dataInicial={data_inicial_str}&dataFinal=&statusNavio="

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()

            try:
                # Navegar para a URL
                page.goto(url)

                # Aguardar o carregamento da página (você pode ajustar este tempo conforme necessário)
                page.wait_for_load_state("load", timeout=10000)

                # Obter os dados desejados (assumindo que os dados estão dentro de uma tag <pre>)
                dados_elementos = page.query_selector_all('pre')

                # Inicializar uma lista para armazenar os dados
                dados = []

                # Iterar sobre os elementos para obter o conteúdo de cada elemento
                for elemento in dados_elementos:
                    # Adicionar o conteúdo do elemento à lista
                    dados.append(elemento.inner_text())

                # Juntar os dados como uma única string
                dados_como_string = ''.join(dados)

                # Converter a string para JSON
                pesquisa_escala = json.loads(dados_como_string).get('VRecebimentoExportacaoTvc', [])

                # Aplicar a função de conversão de datas
             #   pesquisa_escala = self.converter_datas(pesquisa_escala)

                # envia os dados para excel
                return pesquisa_escala

            except Exception as e:
                print(f"Erro: {e}")

            finally:
                # Fechar o navegador
                browser.close()

    # Função para consultar via playwright a escala do terminal o que está em atracacao
    def acesso_escala_atracacao(self):
        data_inicial = datetime.today()
        data_inicial_str = data_inicial.strftime('%Y-%m-%d')
        url = f"https://www.santosbrasil.com.br/v2021/mooring-list/pesquisa?unidade=tecon-vila-do-conde&lista=lista-de-atracacao&atracadouro=TECON&pesquisa=&dataInicial={data_inicial_str}&dataFinal=&statusNavio=navios_esperados"

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()

            try:
                # Navegar para a URL
                page.goto(url)

                # Aguardar o carregamento da página (você pode ajustar este tempo conforme necessário)
                page.wait_for_load_state("load", timeout=10000)

                # Obter os dados desejados (assumindo que os dados estão dentro de uma tag <pre>)
                dados_elementos = page.query_selector_all('pre')

                # Inicializar uma lista para armazenar os dados
                dados = []

                # Iterar sobre os elementos para obter o conteúdo de cada elemento
                for elemento in dados_elementos:
                    # Adicionar o conteúdo do elemento à lista
                    dados.append(elemento.inner_text())

                # Juntar os dados como uma única string
                dados_como_string = ''.join(dados)

                # Converter a string para JSON
                pesquisa_atracacao = json.loads(dados_como_string).get('VAtracacaoTvc', [])

                # Aplicar a função de conversão de datas
               # pesquisa_atracacao = self.converter_datas(pesquisa_atracacao)

                # envia os dados para excel
                return pesquisa_atracacao

            except Exception as e:
                print(f"Erro: {e}")

            finally:
                # Fechar o navegador
                browser.close()
   # função que faz ajuste das datas
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
        campos_para_converter = ['PREVISAO_CHEGADA_y', 'PREVISAO_ATRACACAO', 'PREVISAO_SAIDA']

        # Aplicar a função de conversão às colunas relevantes
        for campo in campos_para_converter:
            pesquisa[campo] = pesquisa[campo].apply(converter_data)

        return pesquisa

    # função que une as acesso escala e a acesso escala atracacao e gera o data frame
    def gerar_informacao_porto(self):
        # Obter a lista de escala e lista de atracação
        lista_escala = self.acesso_escala()
        lista_atracacao = self.acesso_escala_atracacao()

        # Criar DataFrames do pandas
        df_escala = pd.DataFrame(lista_escala)
        df_atracacao = pd.DataFrame(lista_atracacao)
        # Converta a coluna BRC para o mesmo tipo em ambos os DataFrames
        df_escala['BRC'] = df_escala['BRC'].astype(str)
        df_atracacao['BRC'] = df_atracacao['BRC'].astype(str)
        # Realizar o join dos DataFrames
        df_final = pd.merge(df_escala, df_atracacao, on=['ID', 'BRC', 'NAVIO'], how='outer')

        df_final = self.converter_datas(df_final)
        df_final['Terminal'] = df_final.apply(lambda row: 'VDC' if row['NAVIO'] != '' else "", axis=1)


        return df_final



