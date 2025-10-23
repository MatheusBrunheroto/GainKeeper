import json
from item import Item

class DataManager:
    
    def __init__(self):
        
        self.DATA = None
        self.raw = None
        self.items = []
    
    def _create_instances(self):
        
        items = []  # Instance List
        for name in self.DATA["names"]: 
            item = Item(name, self.DATA["names"][name])
            items.append(item)
        return items      
    
    def _generic_json(self):
        
        try:
            with open("generic_data.json", "r", encoding="utf-8") as file:
                self.raw = file.read()
  
        except Exception as e:
            sys.exit(f"Unable to create \"data.json\". -> {e}")


    def read_json(self):
        
        try:      
            # Try to retreive data.json
            with open("data.json", "r", encoding="utf-8") as file:
                self.raw = file.read()
            
            # If it exists and is empty, create a generic version, so it can run the code
            if not self.raw.strip():
                print("The \"data.json\" file is empty!\n Creating Generic \"data.json\"...")
                self._generic_json()
                
            self.DATA = json.loads(self.raw)
            return self._create_instances()
        
        # If it doesn't exist, creates and 
        except:
            
            print("The \"data.json\" file doesn't exist!\n Creating Generic \"data.json\"...")
            with open("data.json", "w", encoding="utf-8") as file:
                pass
            
            self._generic_json()
            self.DATA = json.loads(self.raw)
            return self._create_instances()
            
            
    def write_json(self, items):
        
        # Creates the New Dictionary #
        dictionary = {"names": {}}
        for item in items:
            dictionary["names"][item.name] = {
                "purchases": [
                    {"price": price, "amount": amount}
                    for price, amount in item.purchase_prices
                ],
                "sales": [
                    {"price": price, "amount": amount}
                    for price, amount in item.sale_prices
                ]
            }
            
        # Write the new data in data.json, in the same way it was read before
        with open("data.json", "w", encoding="utf-8") as file:
            json.dump(dictionary, file, indent=4, separators=(",", ": "), ensure_ascii=False)
        