import json
import sys


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
def read_json():
    
    try:
        
        with open("dict.json") as f:
            raw = f.read()
            
        if raw:
            DATA = json.loads(raw) # pra finalizar é json.dumps
            # DUPLICA PRO BACKUP
            
            # Create Instances #
            items = []  # Instance List
            for name in DATA["names"]: 
                item = Item(name, DATA["names"][name])
                items.append(item)
            return items


        else:
            # PRIMEIRA VEZ, adiciona dicionario vazio
            print("The \"dict.json\" file is empty!")
            
        # transofmra em objeto
        
        
    except Exception as e:
        
        print(f"Failed to find \"dict.json\"! ({e})...")
        # CRIA SE NAO EXISTIR
        sys.exit("\"dict.json\" was created!")
def write_json():
    return 1
    
   
   




    
    # Converting the dictionary entry into an object, with easily accessible attributes for purchases, sales, and financial metrics #
    def __init__(self, name: str, data: dict):
        
        self.name = name
        
        ## Purchase Variables ##
        self.purchase_prices = []                    # purchase_prices[N][{Price, Amount}]
        self.total_purchase_price = 0                # total_purchase_price += purchase_prices[0 .. N][0] * purchase_prices[0 .. N][1
        self.total_purchase_amount = 0               # total_purchase_amount += purchase_prices[0 .. N][1]
        self.average_purchase_price = 0              # average_purchase_price = total_purchase_price / total_purchase_amoun
        
        ## Sale Variables (Same Idea from the Purchase Variables) ## 
        self.sale_prices = []                        # sale_prices[N][{Price, Amount}]
        self.total_sale_price = 0
        self.total_sale_amount = 0
        self.average_sale_price = 0
        
        self.remaining_amount = 0
        self.estimated_profit = 0                    # estimated_profit = total_sale_price - (average_purchase_price * total_sale_amount)
        self.taxed_estimated_profit = 0              # taxed_estimated_profit = (total_sale_price * 0.98) - (average_purchase_price * total_sale_amount)
        self.estimated_ROI = 0                       # estimated_ROI = taxed_estimated_profit * 100 / total_purchase_price
        
        
        purchase = data["purchases"]
        for p in purchase:
            self.purchase_prices.append([p["price"], p["amount"]])
            self.total_purchase_price += p["price"] * p["amount"]
            self.total_purchase_amount += p["amount"]        
        if self.total_purchase_amount > 0:  # Avoid division by 0
            self.average_purchase_price = self.total_purchase_price / self.total_purchase_amount

        ## Repeat the exact same proccess, but for sales ##
        sale = data["sales"]
        for s in sale:
            self.sale_prices.append([s["price"], s["amount"]])
            self.total_sale_price += s["price"] * s["amount"]
            self.total_sale_amount += s["amount"]    
        if self.total_sale_amount > 0: 
            self.average_sale_price = self.total_sale_price / self.total_sale_amount


        self._update_financial_metrics()
        
        

    def potential_profit(self, current_price):
        return 1
    
    
    
    def _update_financial_metrics(self):

        # Stock # RISCO DE ALGUEM COLOCAR SALE > AMOUNT, corrigir isso no record_sale, na hora de verificar o total sale amount
        self.remaining_amount = self.total_purchase_amount - self.total_sale_amount
        
        # Financial Performance Metrics # 
        self.estimated_profit = self.total_sale_price - (self.average_purchase_price * self.total_sale_amount)
        self.taxed_estimated_profit = (self.total_sale_price * 0.98) - (self.average_purchase_price * self.total_sale_amount)
        self.estimated_ROI = self.taxed_estimated_profit * 100 / self.total_purchase_price
    
    
    # Searches if the price already exists; if so, its amount is increased. Otherwise, a new price entry is added with the given amount. 
    def record_purchase(self, price, amount):
        price_found = False
        for i in range(len(self.purchase_prices)):
            if self.purchase_prices[i][0] == price:
                self.purchase_prices[i][1] += amount
                price_found = True
                break
        if price_found == False:
            self.purchase_prices.append([price, amount])
        
        # Recalculates important data #
        self.total_purchase_price += price * amount
        self.total_purchase_amount += amount
        self.average_purchase_price = self.total_purchase_price / self.total_purchase_amount
        self._update_financial_metrics()
        
    def record_sale(self, price, amount):
        price_found = False
        for i in range(len(self.sale_prices)):
            if self.sale_prices[i][0] == price:
                self.sale_prices[i][1] += amount
                price_found = True
                break
        if price_found == False:
            self.sale_prices.append([price, amount])
            
        self.total_sale_price += price * amount
        self.total_sale_amount += amount
        self.average_sale_price = self.total_sale_price / self.total_sale_amount
        self._update_financial_metrics()
        
        

def menu():
    return 1
        
        
if __name__ == "__main__":
    
    items = read_json()
  
    # menu
    # após tudo, deve ser criado um novo dicionario, com os novos objetos, processo reverso
    
    print("=== Financial Overview ===")
    for item in items:
        print(f"Item: {item.name}")
        print(f"item {item.purchase_prices[0]}")
        print(f"  Total Purchased: {item.total_purchase_amount} units for {item.total_purchase_price}")
        print(f"  Total Sold: {item.total_sale_amount} units for {item.total_sale_price}")
        print(f"  Remaining Units: {item.remaining_amount}")
        print(f"  Average Purchase Price: {item.average_purchase_price}")
        print(f"  Average Sale Price: {item.average_sale_price}")
        print(f"  Estimated Profit: {item.taxed_estimated_profit}")
        print(f"  Estimated ROI: {item.estimated_ROI:.2f}%")
        print("-" * 40)
   
   
   # fazer um arquivo com a data que itens foram adicionados, lucro, etc... pra fazer o grafico