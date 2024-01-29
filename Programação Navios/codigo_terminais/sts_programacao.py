import pandas as pd
from playwright.sync_api import sync_playwright
import json
from datetime import datetime


"""Classe que contem a geração de um Datframe com os dados do terminal portuário de Santos Brasil"""
class ProgramacaoSTS:

    # Função para consultar via playwright a escala do terminal previsto chegada
    def acesso_escala(self):
        data_inicial = datetime.today()
        data_inicial_str = data_inicial.strftime('%Y-%m-%d')
        url = f"https://www.santosbrasil.com.br/v2021/lista-de-atracacao/pesquisa?unidade=tecon-santos&lista=lista-de-atracacao&atracadouro=TECON&pesquisa=&dataInicial={data_inicial_str}&dataFinal=&statusNavio="

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
                pesquisa = json.loads(dados_como_string).get('VAtracacao', [])

                # Aplicar a função de conversão de datas
                pesquisa = self.converter_datas(pesquisa)

                # envia os dados para excel
                return pesquisa

            except Exception as e:
                print(f"Erro: {e}")

            finally:
                # Fechar o navegador
                browser.close()

    # função que faz ajuste das datas
    def converter_datas(self, pesquisa):
        # Função para converter datas no formato \/Date(1706198400000)\/ para DD/MM/AAAA
        def converter_data(data):
            if data:
                data_em_milissegundos = int(data.replace("/Date(", "").replace(")/", ""))
                data_em_segundos = data_em_milissegundos / 1000
                data_real = datetime.utcfromtimestamp(data_em_segundos)
                return data_real.strftime('%d/%m/%Y')
            else:
                return ''

        # Aplicar a função de conversão aos campos relevantes
        for item in pesquisa:
            campos_para_converter = ['PREVISAO_CHEGADA','CHEGADA', 'PREVISAO_ATRACACAO', 'DATA_ATRACACAO',
                                     'PREVISAO_SAIDA', 'SAIDA','INI_OPERA', 'DEADLINE', 'LIBERACAO_DRY', 'LIBERACAO_REEFER']
            for campo in campos_para_converter:
                if campo in item and item[campo]:
                    item[campo] = converter_data(item[campo])

        return pesquisa

    # função que une as acesso escala e a acesso escala atracacao e gera o data frame
    def gerar_informacao_porto(self):
        # Obter a lista de escala
        lista_escala = self.acesso_escala()

        # Verificar se a lista é válida antes de prosseguir
        if lista_escala:
            # Criar um DataFrame do pandas
            df = pd.DataFrame(lista_escala)
            df['Terminal'] = df.apply(lambda row: 'SANTOS BRASIL' if row['NAVIO'] != '' else "", axis=1)

            return df
        else:
            print("Não foi possível obter dados válidos para a lista de escala.")


