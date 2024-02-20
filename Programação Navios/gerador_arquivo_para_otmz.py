import pandas as pd
import os
from datetime import date, datetime

class GerarArquivoOtmz:
    def __init__(self, arquivo_base):
        self.arquivo_base = pd.read_excel(arquivo_base)
        self.obj = self.executar_deve_arquivo()

    def ler_e_mesclar(self,arquivo_analise,nome_aba,coluna_mesclagem):
        arquivo_de_para = "./arquivos_excel/base_de-para-schedule.xlsx"
        dados = pd.read_excel(arquivo_de_para, sheet_name=nome_aba)
        if arquivo_analise is None:
            return dados
        else:
            df_atual = pd.merge(arquivo_analise,dados,how='left',on=coluna_mesclagem)
            return df_atual

    def executar_deve_arquivo(self):
        infos_leitura_mesclagem = [
            ('DE PARA TERMINAL', 'Terminal'),
            ('DE  - PARA SERVIÇOS', 'Serviço'),
            ('Servicos-e-Armador', 'SERVIÇO OTIMIZADOR'),
            ('CODIGO NAVIO ARMADOR', ['Cod Armador', 'Navio'])
        ]
        #loop de execução para gerar mesclar os arquivos com a base do de para
        for nome_aba, coluna_mesclagem  in infos_leitura_mesclagem:
            arquivo_novo = self.ler_e_mesclar(self.arquivo_base,nome_aba,coluna_mesclagem)
            self.arquivo_base = arquivo_novo


        # filtra e classifica informações necessárias
        if self.arquivo_base is not None:
            arquivo_final = self.arquivo_base[['codigo terminal','Terminal','cod_navio','Navio',
            'Viagem','Cod Armador','Armador','SERVIÇO OTIMIZADOR','ROTA','Deadline','Previsão Saída']]

            # Verificar se a coluna 'SERVIÇO OTIMIZADOR' não contém 'NÃO OPERA MINERVA'
            filtro = arquivo_final['SERVIÇO OTIMIZADOR'] != 'NÃO OPERA MINERVA'

            # Aplicar o filtro para manter apenas as linhas que satisfazem a condição
            arquivo_final = arquivo_final[filtro]

            #remove todas as duplicadas
            arquivo_final = arquivo_final.drop_duplicates()
            # Se desejar redefinir os índices após a remoção das linhas, você pode usar reset_index
            arquivo_final = arquivo_final.reset_index(drop=True)


            # ----------- SALVAR ARQUIVO FINAL -----------------
            data_formatada = datetime.strftime(date.today(), '%d-%m-%Y')
            caminho_pasta = os.path.abspath(os.path.dirname(__file__))
            nome_arquivo = f'Schedule_Para_Otimizador_{data_formatada}.xlsx'
            caminho_sub_pasta = os.path.join(caminho_pasta, 'arquivos_excel')
            caminho_completo = os.path.join(caminho_sub_pasta, nome_arquivo)
            arquivo_final.to_excel(caminho_completo, index=False)
            print(f"Arquivo salvo em: {caminho_completo}")
        else:
            print("Não foi possível criar o arquivo final, pois não houve mesclagem de dados.")

if __name__ == "__main__":
    arquivo_base = './arquivos_excel/schedule_navios_20-02-2024.xlsx'
    teste = GerarArquivoOtmz(arquivo_base)
