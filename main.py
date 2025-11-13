
from interface.interface_main import App, TransactionRecorder, ItemRegisterer
from data_manager import DataManager
# from inventory import Inventory

# FAZER UM CONFIG FILE PRA SALVAR PREFERENCIAS, LER ELE ANTES TAMBEM
"""
The dict.json file is structured in the following way:

{
    "names": {
        "First Item Name":{
            "purchases": [  {"amount": AMOUNT1, "price": PRICE1},
                            {"amount": AMOUNT2, "price": PRICE2}   ],
            "sales": [  {"amount": AMOUNT1, "price": PRICE1},
                        {"amount": AMOUNT2, "price": PRICE2}   ]
        }, 
        "Second Item Name":{
            "purchases": [  {"amount": AMOUNT1, "price": PRICE1},
                            {"amount": AMOUNT2, "price": PRICE2},
                            {"amount": AMOUNT3, "price": PRICE3}   ],1,46
            "sales": [  {"amount": AMOUNT1, "price": PRICE1}   ]
        }
        ...
    }
}

USAGE EXAMPLES : 

dict["names"] -> "First Item Name":{"purchases": [{...}, {...}], "sales": [{...}]}, "Second Item Name":{"purchases": [{...}, {...}, {...}], "sales": [{...}]}

    dict["names"]["First Item Name"] -> {"purchases": [{...}, {...}], "sales": [{...}, {...}]}
    -   dict["names"]["First Item Name"]["purchases"] -> [{...}, {...}]
    
    -   -   dict["names"]["First Item Name"]["purchases"][0] -> {"amount": AMOUNT1, "price": PRICE1}
    -   -   -   dict["names"]["First Item Name"]["purchases"][0]["amount"] -> AMOUNT1
    
    -   -   dict["names"]["First Item Name"]["purchases"][1] -> {"amount": AMOUNT2, "price": PRICE2}
    -   -   -   dict["names"]["First Item Name"]["purchases"][1]["price"] -> PRICE2
    ...

    dict["names"]["Second Item Name"] -> {"purchases": [{...}, {...}, {...}], "sales": [{...}]}
    -   dict["names"]["Second Item Name"]["sales"] -> [{...}]
    -   -   dict["names"]["Second Item Name"]["sales"][0] -> {"amount": AMOUNT1, "price": PRICE1}
    
    -   dict["names"]["Second Item Name"]["purchases"][2] -> {"amount": AMOUNT3, "price": PRICE3}
    -   -   dict["names"]["Second Item Name"]["purchases"][2]["price"] -> PRICE3
    ...
"""
        # Criar tela para ativar / desativar
        # FILTRAR O IS ACTIVE NO INTERFACE, PRA A PARECER OU NAO. CRIAR UM LUGAR COM UMA LISTA DOS ITEM NAO ATIVOS, USAR ELES NO GRAFICO MESMO ASSIM
if __name__ == "__main__":
    
    data_manager = DataManager()
    items = data_manager.read_json()    # List of objects, returned by read_json()
    # inventory = Inventory(items)
    
    """ It's mandatory to have the "items" defined before calling App(), because it could be an empty value and
        mess up the "SELECT ITEM" option, because it uses "values=[item.name for item in self.items]", and
        if there is no object with parameter "name", it won't work """
        

    app = App(items)
    app.mainloop()

    for item in items:
        print(item.name)
        
    items = [item for item in items if item.name != "placeholder"]   # Remove placeholder in a data.json that was inexistent or empty
    data_manager.write_json(items)


   # fazer um arquivo com a data que itens foram adicionados, lucro, etc... pra fazer o grafico