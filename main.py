from chave import API_ProjectKEY
from alpha_vantage.timeseries import TimeSeries

ts = TimeSeries(key=API_ProjectKEY)

#                                                                           #
#   Inicio o codigo criando as funções que serão utilizadas pelo codigo     #
#                                                                           #

def geraInfosAcao(acao):
    data = ts.get_quote_endpoint(symbol=acao)

    if data == ({}, None):
        return(0)
    else:
        return data
    

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
    '''
    print(infoReturn)


def toExcel():
    #FALTA DESENVOLVER
    print()


def logicaPrincipal():
    #Para não poluir a logica do codigo e declaro as variaveis e textos aqui
    msgInical = """
BEM VINDO! VOU EXPLICAR RAPIDIN COM FUNCIONA:
-Busque uma ação, cada ação buscada vai ter suas informações de valor exibidas e no fim sera gerado em EXCEL com todos os resultados obtidos
-Todos os valores estão na moeda do país cujo a empresa esta listada na bolsa

JA PODEMOS COMEÇAR:"""

    msgInteracao_um = """
-> Caso queira buscar por uma ação BRASILEIRA, digite seu codigo, como por exemplo VALE3
-> Caso queira buscar por uma ação dos EUA, digite 1
-> Caso queira buscar por uma ação INTERNACIONAL , digite 2
"""
    msgInteracao_dois = """   
    Bacana. Entao me responde:
-> Caso queira buscar por uma ação dos EUA, apenas escreva seu codigo, como por exemplo "NVDA"
-> Caso queira buscar por outras bolsas de valores é necessario colocar a extenção da Bolsa de Valores responsavel. Para mais detalhes digite 2
    """
    msgInteracao_tres = """
    Certo, para pegar informações de ações de outros países é necessario colocar o codigo da bolsas de valores do país!
    Por exemplo, para a empresa CAMECO (cco), que é do canada ficaria: CCO.TO
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
                    condicaoSaida_infosAcaoRecebida = True
        
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
                    condicaoSaida_infosAcaoRecebida = True

        #Caso o primeiro elemento seja Uma ação
        else:
            infosAcao = geraInfosAcao(stock)

            if infosAcao == 0:
                print(f"A ação {stock} não foi encontrada na bolsa de valores BRASILEIRA. Por favor, Tente Novamente")
            else:
                entregaResultadoFormatado(infosAcao)
                condicaoSaida_infosAcaoRecebida = True
        


logicaPrincipal()

print("passou aq")
