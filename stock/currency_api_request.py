import requests
import json
# NO INICIO DO PROGRAMA, QUARDAR AS CONVERSOES PRA MOEDA DESEJADA, AS OPCOES PEGAM DO CACHE
def get_rate(inventory_currency, selected_currency):
    
    # if inventory_currency == selected_currency # POR ISSO LA NO BAHGLHYO
    
    url = f"https://api.vatcomply.com/rates?base={inventory_currency}&symbols={selected_currency}"
    response = requests.get(url)
    rate = json.loads(response.content)
    print(rate["rates"][selected_currency])



print(get_rate("USD", "BRL"))
