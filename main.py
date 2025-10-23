import sys
from interface import App, TransactionRecorder, ItemRegisterer
from data_manager import DataManager

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
                            {"amount": AMOUNT3, "price": PRICE3}   ],
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
        
        
if __name__ == "__main__":
    
    data_manager = DataManager()
    items = data_manager.read_json()    # List of objects
    
    """ It's mandatory to have the "items" defined before calling App(), because it could be an empty value and
        mess up the "SELECT ITEM" option, because it uses "values=[item.name for item in self.items]", and
        if there is no object with parameter "name", it won't work """
        # É MESMO? talvez definir lista dict com try e except
        
        # A CADA ADIÇÃO EU TERIA QUE LER A LISTA AO VIVO PRA MANTER LÁ, 
    if items:

        app = App(items)
        app.mainloop()

    for item in items:
        print(item.name)
    data_manager.write_json(items)


   # fazer um arquivo com a data que itens foram adicionados, lucro, etc... pra fazer o grafico