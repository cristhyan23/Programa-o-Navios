# Programa de Geração de Programação de Navios

Este programa em Python foi desenvolvido para gerar a programação de navios de diversos portos do Brasil, incluindo Navegantes, Paranaguá, Itapoá, BTP, Santos Brasil, DPW, Salvador e Vila do Conde.

## Estrutura do Projeto

O arquivo base para gerar o relatório, que é retornado em formato Excel e salvo na pasta `arquivos_excel`, é o `gerador_arquivos.py`. Este script aciona as demais classes de cada terminal, que estão armazenadas na pasta `codigo_terminais`. Essas classes manipulam os dados utilizando a biblioteca Pandas e geram um arquivo Excel único com informações detalhadas sobre a programação dos navios.

## Execução do Programa

Para utilizar o programa, siga os passos abaixo:

1. Clone o repositório:

   ```bash
   git clone https://github.com/cristhyan23/Programa-o-Navios.git
   ```

2. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

3. Execute o script `gerador_arquivos.py`:

   ```bash
   python gerador_arquivos.py
   ```

O relatório gerado será salvo na pasta `arquivos_excel` com informações detalhadas sobre os terminais, navios, viagens, serviços, agências, deadlines, previsão de chegada, chegada, previsão de atracação, atracação, previsão de saída, entre outros.


## Contato

Para qualquer dúvida ou sugestão, sinta-se à vontade para entrar em contato:

- Cristhyan ((https://github.com/cristhyan23))
  - Email: cristhyan.alves1@gmail.com


Agradecemos pelo interesse e contribuição para o projeto!
