from chave import API_ProjectKEY
from alpha_vantage.timeseries import TimeSeries

ts = TimeSeries(key=API_ProjectKEY)
stock = input("Digite a ação que deseja consultar o preço: ") + '.SA'


def info_papel_hoje(papel):
    data = ts.get_quote_endpoint(symbol=papel)
    return data


data = info_papel_hoje(stock)

if data == ({}, None):
    print("Digite um codigo de ação valido! (talvez falte o numero do papel)")
    stock = input("Digite a ação que deseja consultar o preço: ") + '.SA'
#passsar a condição de erro para o arquivo MAIN.PY

#print(data)
info, x = data

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
Informações sobre a ação {stock} (data de atualização: {lastTradingDay}):
-Preço: {price}
-Preço de abertura: {openPrice}
-Preço maximo atingido: {maxPrice}
-Preço minimo atingido: {lowPrice}
-Mudança de valor do dia: R${priceChance}
-Mudança percentual do valor: {pricePercentChange}
'''
print(infoReturn)
# print(symbol)
# print(openPrice)
# print(maxPrice)
# print(lowPrice)
# print(price)
# print(volume)
# print(lastTradingDay)
# print(priceChance)
# print(pricePercentChange)









