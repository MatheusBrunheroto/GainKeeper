
"""
    All variables enumerated, since this object has a lot of maths do realize, every function will have in their upper comments the functions
    they handle:
    
    - (1)  self.name
    
    - (2)  self.purchase_prices                   -> purchase_prices[N][{Price, Amount, Currency}]
    - (3)  self.total_purchase_price              -> total_purchase_price += purchase_prices[0 .. N][0] * purchase_prices[0 .. N][1]
    - (4)  self.total_purchase_amount             -> total_purchase_amount += purchase_prices[0 .. N][1]
    - (5)  self.average_purchase_price            -> average_purchase_price = total_purchase_price / total_purchase_amount

    - (6)  self.sale_prices                       (Same Idea from the Purchase Variables)
    - (7)  self.total_sale_price                  ...
    - (8)  self.total_sale_amount                 ...
    - (9)  self.average_sale_price                ...

    - (10) self.remaining_amount                  
    
    - (11) self.estimated_profit                  -> estimated_profit = total_sale_price - (average_purchase_price * total_sale_amount)
    - (12) self.taxed_estimated_profit            -> taxed_estimated_profit = (total_sale_price * 0.98) - (average_purchase_price * total_sale_amount)
    - (13) self.estimated_ROI                     -> estimated_ROI = taxed_estimated_profit * 100 / total_purchase_price
    - (14) self.worst_profit
    
    - (15) self.is_active
    - (16) self.is_first_purchase
    - (17) self.is_first_sale
"""





class Item:
    # CRIAR UM SELF, COM OS PREÇOS CONVERTIDOS, E UM SEM CONVERTER. OS CONVERTIDOS SERAO OS USADOS PRA CONTAS, E OS NAO CONVERTIDOS SERAO USADOS PARA SALVAR
    # Converting the dictionary entry into an object, with easily accessible attributes for purchases, sales, and financial metrics #
    def __init__(self, name: str, data: dict):
        
        # EU SEI QUE TEM PROBLEMA AQUI AINDA
        self.is_first_purchase = False 
        self.is_first_sale = False     
        if data == {'purchases': [{'price': 0, 'amount': 0, 'currency': 0}],'sales': [{'price': 0, 'amount': 0, 'currency': 0}],'is_active': 0}:
            self.is_first_purchase = True
            self.is_first_sale = True
            
        self.name = name

        ## Purchase Variables ##
        self.purchase_prices = []                    
        self.total_purchase_price = 0                
        self.total_purchase_amount = 0               
        self.average_purchase_price = 0              
        
        ## Sale Variables (Same Idea from the Purchase Variables) ## 
        self.sale_prices = []                        
        self.total_sale_price = 0
        self.total_sale_amount = 0
        self.average_sale_price = 0
        
        self.remaining_amount = 0
        self.estimated_profit = 0                    
        self.worst_profit = 0
        self.taxed_estimated_profit = 0              
        self.estimated_ROI = 0                       
        
        self.is_active = data["is_active"]
        
        
        purchase = data["purchases"]
        for p in purchase:
            self.purchase_prices.append([p["price"], p["amount"], p["currency"]])
            self.total_purchase_amount += p["amount"]
            
        ## Repeat the exact same proccess, but for sales ##
        sale = data["sales"]
        for s in sale:
            self.sale_prices.append([s["price"], s["amount"], s["currency"]])
            self.total_sale_amount += s["amount"]    
        
        self._calculate_metrics()
        self._update_financial_metrics()
        
        
        
        
    def _clear_zeros(self, price, amount, currency):
        if self.is_first_purchase:
            self.purchase_prices = [[price, amount, currency] for price, amount, currency in self.purchase_prices if price != 0 and amount != 0 and amount != 0]
            print(self.purchase_prices)
            self.is_first_purchase = False
        if self.is_first_sale:
            self.sale_prices = [[price, amount, currency] for price, amount, currency in self.sale_prices if price != 0 and amount != 0 and currency != 0]
            print(self.sale_prices)
            self.is_first_sale = False
        
        
        
        
        
    """ Utilizing "(2) purchase_prices", modify:
           - (3) total_purchase_price
        Utilizing "(6) sale_prices", modify:
           - (7) total_sale_price
    """
    def _calculate_metrics(self):
        
        converted_price = 0
        for p in self.purchase_prices:
            converted_price = c.convert(p["price"], p["currency"], 'BRL')
            self.total_purchase_price += converted_price * p["amount"]
            
        if self.total_purchase_amount > 0:  # Avoid division by 0
            self.average_purchase_price = self.total_purchase_price / self.total_purchase_amount
        
        for s in self.sale_prices:
            converted_price = s.convert(s["price"], s["currency"], 'BRL')
            self.total_sale_price += s["price"] * s["amount"]
        if self.total_sale_amount > 0: 
            self.average_sale_price = self.total_sale_price / self.total_sale_amount
    
    
    
    def _update_financial_metrics(self):

        # Stock #        
        self.remaining_amount = self.total_purchase_amount - self.total_sale_amount
        
        if self.remaining_amount > 0 and self.total_sale_amount != 0:
            self.worst_profit = self._worst_profit()
        
        # Financial Performance Metrics # 
        if self.total_sale_amount > 0:
            self.estimated_profit = self.total_sale_price - (self.average_purchase_price * self.total_sale_amount)
            self.taxed_estimated_profit = (self.total_sale_price * 0.98) - (self.average_purchase_price * self.total_sale_amount)
        if self.total_purchase_price > 0:
            self.estimated_ROI = self.taxed_estimated_profit * 100 / self.total_purchase_price    
        
        
    """ The purchased_prices is in decrescent order, and the sale_prices are in crescent order.
        Relating the most expensive purchases with the cheapest sales.
        
        if I bought {"price": 30, "amount": 20}, {"price": 20, "amount": 40} 
            and sold {"price": 100, "amount": 30}, {"price": 110, "amount": 10}
        
        It's necessary, if stock != 0, to calculate how much the total sold amount is related with the worst possible buys
        
            Total Sold                  -              Total Bought
            [($100 * 30) + ($110 * 10)] - [($30 * 20) + ($20 * 20)]
            = ($3000 + $1100) - ($600 + $400)
            = $4100 - $1000
            = $3100 <- WORST PROFIT POSSIBLE
        
        *** In the case of a best profit, it would be ($20 * 40) in Total Bought. ***
    """
    def _worst_profit(self):
        
        amount = self.total_sale_amount
        expensive_purchases = 0
        i = 0
        while amount > 0:      
            # If it's bigger than amount, just use the entire current dictionary amount 
            if  amount > self.purchase_prices[i][1]:
                expensive_purchases += self.purchase_prices[i][1] * self.purchase_prices[i][0]
                amount -= self.purchase_prices[i][1]
                i += 1
            else:
                expensive_purchases += amount * self.purchase_prices[i][0]
                amount = 0
        print(self.total_sale_price * self.total_sale_amount - expensive_purchases)
        return (self.total_sale_price * self.total_sale_amount) - expensive_purchases



    def potential_profit(self, current_price):
        return 1

            
    



    def _get_currency(self, currency):
        if currency == "USD":
            return '$'
        elif currency == "RMB":
            return '¥'
        else:
            return "R$"
        
        
        
    # Searches if the price already exists; if so, its amount is increased. Otherwise, a new price entry is added with the given amount. 
    # "zero" inputs are being handled by interface.py
    def record_purchase(self, price, amount, currency):
        
        price_found = False
        print(len(self.purchase_prices))
        for i in range(len(self.purchase_prices)):
            if self.purchase_prices[i][0] == price:
                self.purchase_prices[i][1] += amount
                price_found = True
                break
        if not price_found:
            self.purchase_prices.append([price, amount, currency])
        
        # Recalculates important data #
        
        self.total_purchase_price += price * amount
        self.total_purchase_amount += amount
        self.average_purchase_price = self.total_purchase_price / self.total_purchase_amount
        
        # CONVERTE ANTES DE FAZER AS CONTAS TODAS
        self._update_financial_metrics()
        self._clear_zeros(price, amount, currency)
        self.purchase_prices = sorted(self.purchase_prices, key=lambda x: x[0], reverse=True)
        
        currency_symbol = self._get_currency(currency)
        if amount == 1:
            return (f"[+] Purchase Recorded: {amount} unit of \"{self.name}\" at {currency_symbol}{price:.2f}.\n"
                    f"-> Updated total bought: {self.total_purchase_amount} units.\n")
        else:
            return (f"[+] Purchase Recorded: {amount} units of \"{self.name}\" at {currency_symbol}{price:.2f} each.\n"
                    f"-> Updated total bought: {self.total_purchase_amount} units.\n")
        
    
    # Same idea as record_purchase()
    def record_sale(self, price, amount, currency):
        
        # Avoiding negative stock
        if amount > self.remaining_amount:
            print("z")
            return f"Specified amount ({amount}x) is higher than your stock ({self.remaining_amount}x)!\n"
            
        price_found = False
        for i in range(len(self.sale_prices)):
            if self.sale_prices[i][0] == price:
                self.sale_prices[i][1] += amount
                price_found = True
                break
        if not price_found:
            self.sale_prices.append([price, amount, currency])
            
        self.total_sale_price += price * amount
        self.total_sale_amount += amount
        self.average_sale_price = self.total_sale_price / self.total_sale_amount
        
        
        self._update_financial_metrics()
        self._clear_zeros(price, amount, currency)
        self.sale_prices = sorted(self.sale_prices, key=lambda x: x[0])
        
        currency_symbol = self._get_currency(currency)
        if amount == 1:
            return (f"[+] Sale Recorded: {amount} unit of \"{self.name}\" at {currency_symbol}{price:.2f}.\n"
                    f"-> Updated total bought: {self.total_sale_amount} units.\n")
        else:
            return (f"[+] Sale Recorded: {amount} units of \"{self.name}\" at {currency_symbol}{price:.2f} each.\n"
                    f"-> Updated total bought: {self.total_sale_amount} units.\n")
        
        
        
        
