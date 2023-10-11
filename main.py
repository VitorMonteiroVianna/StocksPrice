from apiConfig import API_ProjectKEY
from alpha_vantage.timeseries import TimeSeries
import requests
import pandas as pd
import openpyxl

ts = TimeSeries(key=API_ProjectKEY)
nomeTabela_resultAcoes = "infos_acoes"

#                                                                           #
#   Inicio o codigo criando as funções que serão utilizadas pelo codigo     #
#                                                                           #

def geraInfosAcao(acao):
    data = ts.get_quote_endpoint(symbol=acao)

    #Chega se existem informações no retorno
    if data == ({}, None):
        return(0)
    else:
        return data


def geraInfosAcao_formatoCSV(acao):
    data = requests.get("https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=" + acao + "&apikey=" + API_ProjectKEY + "GV&datatype=csv")
    retornoCabecalho = data.text.split()[0]
    retornoConteudo = data.text.split()[1]

    with open(nomeTabela_resultAcoes + ".csv", "a+") as arquivoCsv:
        qntLinhas = 0
        for linhas in open(nomeTabela_resultAcoes + ".csv"):
            qntLinhas += 1

        # Condicao para saber se deve ou nao adicionar a primeira linha de titulo das colunas
        if qntLinhas == 0:
            arquivoCsv.write(retornoCabecalho + '\n')
            arquivoCsv.write(retornoConteudo + '\n')

        else:
            arquivoCsv.write(retornoConteudo + '\n')


def converteParaXlsx():
    df = pd.read_csv(nomeTabela_resultAcoes + ".csv")
    df.to_excel(nomeTabela_resultAcoes + ".xlsx")

def entregaResultadoFormatado(retorno):
    #o retorno da API é em formado de tupla
    info = retorno[0]

    symbol = info['01. symbol']
    openPrice = info['02. open']
    maxPrice = info['03. high']
    lowPrice = info['04. low']
    price = info['05. price']
    volume = info['06. volume']
    lastTradingDay = info['07. latest trading day']
    priceChance = info['09. change']
    pricePercentChange = info['10. change percent']

    infoReturn = f'''
    Informações sobre a ação {symbol} (data de atualização: {lastTradingDay}):
    -Preço: {price}
    -Preço de abertura: {openPrice}
    -Preço maximo atingido: {maxPrice}
    -Preço minimo atingido: {lowPrice}
    -Mudança de valor do dia: R${priceChance}
    -Mudança percentual do valor: {pricePercentChange}
    -Volume de vendas: {volume}

    OBS: Todos os valores estão na moeda do país cujo a empresa esta listada na bolsa
    '''
    print(infoReturn)


def logicaPrincipal():
    #Para não poluir a logica do codigo e declaro as variaveis e textos aqui
    msgInical = """
BEM VINDO! VOU EXPLICAR RAPIDIN COM FUNCIONA:
-Busque uma ação, cada ação buscada vai ter suas informações de valor exibidas
-Ao final é possivel gerar um EXCEL com as ações que foram consultadas 

JA PODEMOS COMEÇAR:"""
    msgInteracao_um = """
----------------------------------------------------------------------------------------
-> Caso queira buscar por uma ação BRASILEIRA, digite seu codigo, como por exemplo VALE3
-> Caso queira buscar por uma ação dos EUA, digite 1
-> Caso queira buscar por uma ação INTERNACIONAL , digite 2

-> Para sair e gerar o EXCEL, digite 3
"""
    msgInteracao_dois = """   
    Bacana. Entao me responde:
-> Caso queira buscar por uma ação dos EUA, apenas escreva seu codigo, como por exemplo "NVDA"
-> Caso queira buscar por outras bolsas de valores é necessario colocar a extenção da Bolsa de Valores responsavel. Para mais detalhes digite 2
    """
    msgInteracao_tres = """
    Certo, para pegar informações de ações de outros países é necessario colocar o codigo da bolsas de valores do país!
    Por exemplo, para a empresa CAMECO (cco), que é do canada ficaria: CCO.TO

    LISTA DAS PRINCIPAIS EXTENÇÕES:

Estados Unidos:
	NYSE (New York Stock Exchange): .NY
	NASDAQ: .OQ
	AMEX (American Stock Exchange): .A

Canadá:
	Toronto Stock Exchange (TSX): .TO
	TSX Venture Exchange: .V

Alemanha:
	Frankfurt Stock Exchange (Xetra): .DE
	Deutsche Boerse (Frankfurt): .F

Japão:
	Tokyo Stock Exchange (TSE): .T

Índia:
	National Stock Exchange of India (NSE): .NS
	Bombay Stock Exchange (BSE): .BO

China:
	Hong Kong Stock Exchange (HKEX): .HK
	Shanghai Stock Exchange (SSE): .SS
	Shenzhen Stock Exchange (SZSE): .SZ

Coreia do Sul:
	Korea Exchange (KRX): .KS
"""


    condicaoSaida_infosAcaoRecebida = False
    condicaoSaida_acaoEUA = False
    condicaoSaida_acaoInternacional = False

    print(msgInical)

    while condicaoSaida_infosAcaoRecebida != True:
        print(msgInteracao_um)
        stock = str(input("==> ")) + '.SA' #.SA é a extenção da bolsa de valores BR
            
        #Caso seja solicitada ação dos EUA
        if stock[0] == '1':
            print(msgInteracao_dois)
            stock = input("==>")

            while condicaoSaida_acaoEUA != True:
                infosAcao = geraInfosAcao(stock)

                if infosAcao == 0:
                    print(f"A ação {stock} não foi encontrada nas bolsas de valores dos EUA. Por favor, Tente Novamente")
                    condicaoSaida_acaoEUA = True
                else:
                    entregaResultadoFormatado(infosAcao)
                    print("SAINDO LOOP - ACAO US")
                    condicaoSaida_acaoEUA = True
        
        #Caso seja uma ação de outro país qualquer
        elif stock[0] == '2':
            print(msgInteracao_tres)
            stock = input("==>")

            while condicaoSaida_acaoInternacional != True:
                infosAcao = geraInfosAcao(stock)

                if infosAcao == 0:
                    print(f"A ação {stock} não foi encontrada. Por favor, Tente Novamente")
                    condicaoSaida_acaoInternacional = True
                else:
                    entregaResultadoFormatado(infosAcao)
                    print("SAINDO LOOP - ACAO INTERNACIONAL")
                    condicaoSaida_acaoInternacional = True
        
        #Caso queira sair e gerar o EXCEL   
        elif stock[0] == '3':
            converteParaXlsx()
            condicaoSaida_infosAcaoRecebida = True


        #Caso o primeiro elemento seja Uma ação - ACAO BR
        else:
            infosAcao = geraInfosAcao(stock)

            if infosAcao == 0:
                print(f"A ação {stock} não foi encontrada na bolsa de valores BRASILEIRA. Por favor, Tente Novamente")
            else:
                entregaResultadoFormatado(infosAcao)
                geraInfosAcao_formatoCSV(stock)


logicaPrincipal()
