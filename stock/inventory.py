

class Inventory:
    
    def __init__(self, items):
        
        self.items = items
        
        self.total_items = 0
        
        # Current Inventory Price
        for item in self.items:
            item.remaining_amount
        
        # Total Purchases
        for item in self.items:
            
            self.total_purchase_amount += item.total_purchase_amount
            self.total_purchase_price += item.total_purchase_price
            
            self.total_sale_amount += item.total_sale_amount
            self.total_sale_price += item.total_sale_price
            
            self.total_estimated_profit += item.taxed_estimated_profit
            
            self.estimated_inventory_price +=  
            
        # Total Sales
        for item in self.items:
            item.
            
        # Total Profit O TANTO QUE EU VENDI NAO IMPORTA, MAS COMO CALCULAR O PREÇO DO RESTANTE NO INVENTARIO?
        # a MELHOR FORMA SERIA ACHAR O WORST PROFIT_ TAXAR ELE E SOMAR
        # REMAINING AMOUNT, eu teria que ordenar a lista por preços e somar pelos remaining amount, gerando o worst profit