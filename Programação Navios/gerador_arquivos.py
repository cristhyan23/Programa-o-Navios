from codigo_terminais.btp_programacao import ProgramacaoBTP
from codigo_terminais.dpw_programacao import ProgramacaoDPW
from codigo_terminais.itapoa_programacao import ProgramacaoItapoa
from codigo_terminais.portonave_programacao import ProgramacaoPortonave
from codigo_terminais.salvador_programacao import ProgramacaoTecon
from codigo_terminais.sts_programacao import ProgramacaoSTS
from codigo_terminais.tcp_programacao import ProgramacaoTCP
from codigo_terminais.vdc_programacao import ProgramacaoVDC
from gerador_arquivo_para_otmz import GerarArquivoOtmz
import pandas as pd
from functools import reduce
import os
from datetime import date,datetime


""" Classe resposavel por inicializar as funções de cada terminal tratar os dados para ficares com as mesmas colunas e unir em um relatório"""
class Gerador_Informacoes_Portos:
    def __init__(self):
        self.btp = ProgramacaoBTP()
        self.dpw = ProgramacaoDPW()
        self.itapoa = ProgramacaoItapoa()
        self.portonave = ProgramacaoPortonave()
        self.salvador = ProgramacaoTecon()
        self.sts = ProgramacaoSTS()
        self.tcp = ProgramacaoTCP()
        self.vdc = ProgramacaoVDC()
        #colunas padrão do relatório
        self.dados_relatorio_unificado = ["Terminal", "Navio", "Viagem", "Serviço", "Agencia", "Deadline",
                                     "Previsão Chegada", "Chegada", "Previsão Atracacao", "Atracacao", "Previsão Saída"]
        self.obj_excel = self.unificar_arquivos_e_salvar_em_excel_em_um_caminho()

    # função responsavel por processar o data frame de cada terminal gerar uma copia ja com as colunas novas tratadas
    def processar_dataframe(self, df, dados_desejados):

        # Colunas novo relatório
        de_para_nomes_ = {desejado: unificado for desejado, unificado in
                             zip(dados_desejados, self.dados_relatorio_unificado)}
        base = df[dados_desejados].copy()
        base.rename(columns=de_para_nomes_, inplace=True)
        return base

    # função responsavel de gerar os gatilhos para atualizar cada daframe e atualizar e salvar o arquivo final
    def unificar_arquivos_e_salvar_em_excel_em_um_caminho(self):

        df_btp = self.btp.gerar_informacao_porto()
        df_dpw = self.dpw.gerar_informacao_porto()
        df_itapoa = self.itapoa.gerar_informacao_porto()
        df_salvador = self.salvador.gerar_informacao_porto()
        df_sts = self.sts.gerar_informacao_porto()
        df_tcp = self.tcp.gerar_informacao_porto()
        df_vdc = self.vdc.gerar_informacao_porto()
        df_portonave = self.portonave.gerar_informacao_porto()

        # funções dados desejos e de paras:
        dados_desejados_btp = ['Terminal', 'Navio', 'Viagem', 'Servico', 'Agencia', 'DeadlineCarga',
                               'PrevisaoChegada', 'Chegada', 'PrevisaoAtracacao', 'Atracacao', 'PrevisaoSaida']
        dados_desejados_dpw = ["Terminal", "NAVIO", "VIAGEMIN", "SERVICO", "AGENCIA", "ReeferDeadline",
                                "ETADATA", "ATADATA", "ETA", "AtracacaoDATA", "ETDDATA"]
        dados_desejados_ita = ["Terminal", "Navio", "Viagem", "Serviço", "Armador", "Dealine", "ETA", "ATA",
                               "ETB", "ATB", "ETS"]
        dados_desejados_portonave = ["Terminal", "NOME_NAVIO", "VIAGEM", "SERVICO", "ARMADOR", "DEADLINE",
                                     "CHEGADA_PREVISTA", "CHEGADA", "ATRACACAO_PREVISTA", "ATRACACAO", "SAIDA"]

        dados_desejados_salvador = ["Terminal", "NavioNome", "Viagem", "ServicoNome", "Armador",
                                    "DeadlineDryFormat", "EtaFormat", "ChegadaReal", "Etb", "InicioRealFormat",
                                    "EtdFormat"]
        dados_desejados_sts = ["Terminal", "NAVIO", "VIAGEM", "JOINT", "AGENCIA","LIBERACAO_REEFER",
                               "PREVISAO_CHEGADA", "CHEGADA", "PREVISAO_ATRACACAO", "DATA_ATRACACAO", "PREVISAO_SAIDA"]
        dados_desejados_tcp = ["Terminal", "Navio", "ViagemTcp", "ServiceStr", "ArmadorNome","DeadLine",
                               "ChegadaEstimada", "ChegadaBarra", "PrevisaoAtracacao", "Atracacao", "PrevisaoSaida"]
        dados_desejados_vdc = ["Terminal", "NAVIO", "VIAGEM_ARMADOR", "SRV", "AGENCIA","LIBERACAO_REEFER",
                               "PREVISAO_CHEGADA_y", "CHEGADA", "PREVISAO_ATRACACAO", "DATA_ATRACACAO",
                               "PREVISAO_SAIDA"]
        # Processar DataFrames
        base_btp = self.processar_dataframe(df_btp, dados_desejados_btp)
        base_dpw = self.processar_dataframe(df_dpw, dados_desejados_dpw)
        base_ita = self.processar_dataframe(df_itapoa, dados_desejados_ita)
        base_portonave = self.processar_dataframe(df_portonave, dados_desejados_portonave)
        base_salvador = self.processar_dataframe(df_salvador, dados_desejados_salvador)
        base_sts = self.processar_dataframe(df_sts, dados_desejados_sts)
        base_tcp = self.processar_dataframe(df_tcp, dados_desejados_tcp)
        base_vdc = self.processar_dataframe(df_vdc, dados_desejados_vdc)

        # Unir todos os DataFrames
        dfs = [base_btp, base_dpw, base_ita, base_portonave, base_salvador, base_sts, base_tcp, base_vdc]
        df_resultado = reduce(lambda left, right: pd.merge(left, right, on=self.dados_relatorio_unificado, how="outer"), dfs)


        #salvar dataframa em excel na pasta dentro da pasta arquivo_excel dentro da pasta que esta salvo o codigo
        data_atualizacao = date.today()
        data_formatada = datetime.strftime(data_atualizacao,'%d-%m-%Y')
        caminho_pasta = os.path.abspath(os.path.dirname(__file__))
        nome_arquivo = f'schedule_navios_{data_formatada}.xlsx'
        caminho_sub_pasta = Path(caminho_pasta) /'arquivos_excel'
        caminho_completo = os.path.join(caminho_sub_pasta, nome_arquivo)
        df_resultado.to_excel(caminho_completo, index=False)
        print(f"Arquivo salvo em: {caminho_completo}")
        #GERAR BASE PARA OTIMIZADOR
        Executar = GerarArquivoOtmz(caminho_completo)

if __name__ == "__main__":
    gerador = Gerador_Informacoes_Portos()




