import customtkinter as ctk
from item import Item
# Configuração inicial da janela
ctk.set_appearance_mode("dark")      # "light", "dark", ou "system"
ctk.set_default_color_theme("dark-blue")  # "blue", "green", "dark-blue"
# TATLVEZ ADICIONAR HORARIOS NO LOG

class App(ctk.CTk):
    
    def __init__(self, items):
        super().__init__()

        self.items = items
        # Main window configuration
        self.title("GainKeeper")
        self.geometry("1200x700")
        self.resizable(False, False)
        # Title
        self.label_title = ctk.CTkLabel(self, text="📊 GainKeeper - Financial Overview", font=("Arial", 24, "bold"))
        self.label_title.pack(pady=20)
        # Main frame
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(padx=20, pady=10, fill="both", expand=True)
        self.main_frame.columnconfigure(0, weight=0)  # Esquerda - conteúdo fixo
        self.main_frame.columnconfigure(1, weight=1)  # Direita - expansível
   # Columns amount
        # Três linhas na coluna esquerda (ajuste conforme necessário)


        self.left_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="n")
        # ====== FRAMES ESQUERDA ====== #
        
        

        
        # Campos de entrada

        # ====== FRAME DIREITO (LOG / OUTPUT) ====== #
        self.right_frame = ctk.CTkFrame(self.main_frame)
        self.right_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew",)
    

        self.label_log = ctk.CTkLabel(
            self.right_frame,
            text="Action Log",
            font=("Arial", 18, "bold"),
        )
        self.label_log.pack(pady=10)

        self.text_output = ctk.CTkTextbox(self.right_frame, width=500, height=500)
        self.text_output.pack(padx=10, pady=10, fill="both", expand=True)
        self.text_output.insert("0.0", "Log initialized...\n")
        
        
        self.item_registerer = ItemRegisterer(self.left_frame, self.items, self.text_output)
        
        self.transaction_recorder = TransactionRecorder(self.left_frame, self.items, self.text_output)
        # Reference of "transaction_recorder" inside of "item_registerer", so "item_registerer" can update the list in "transaction_recorder"
        self.item_registerer.transaction_recorder = self.transaction_recorder
     

    def clear_log(self):
        self.text_output.delete("0.0", "end")
        self.text_output.insert("0.0", "Log cleared...\n")




class ItemRegisterer:
    
    def __init__(self, parent, items, text_output):
        self.parent = parent
        self.items = items
        self.text_output = text_output
        
        # Used to "ping" TransactionRecorder when a new item is added, updating the selection list in real time
        self.transaction_recorder = None
        
        self._register_item()
        
    def _register_item(self):

        # Frame Configuration
        self.register_frame = ctk.CTkFrame(self.parent)   # Inherits from main_frame
        self.register_frame.pack(padx=10, pady=(0, 10), fill="x")
        self.register_frame.columnconfigure(0, weight=1)
        
        # Subtitle
        label_register = ctk.CTkLabel(self.register_frame, text="Register New Item", font=("Arial", 18, "bold"))
        label_register.grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.entry_name = ctk.CTkEntry(self.register_frame, placeholder_text="Name")
        self.entry_name.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        self.btn_new_item = ctk.CTkButton(self.register_frame, text="Add Item", command=self._add_item)
        self.btn_new_item.grid(row=1, column=2, padx=10, pady=5, sticky="ew")


    def _add_item(self):

        name = self.entry_name.get()
        name = name.strip()
        for item in self.items:
            if item.name == name:
                self.text_output.insert("end", f"\n-> {name} is already registered!")
                return
            
        new_item = Item(name, {'purchases': [{'price': 0, 'amount': 0, 'currency': 0}],'sales': [{'price': 0, 'amount': 0, 'currency': 0}],'is_active': 0})
        self.items.append(new_item)
        self.transaction_recorder.entry_item.configure(values=[item.name for item in self.items])

# CRIAR O OBJETO STOCK QUE VAI GUARDAR DADOS GERAIS


class TransactionRecorder:
    
    def __init__(self, parent, items, text_output):
        self.parent = parent
        self.items = items
        self.text_output=text_output
        self._record_transaction()
    
    
    def _record_transaction(self):
   
        # Frame Configuration
        self.record_frame = ctk.CTkFrame(self.parent)
        self.record_frame.pack(padx=10, pady=(0, 10), fill="x")
    
        # Subtitle
        label_record = ctk.CTkLabel(self.record_frame, text="Record Transaction", font=("Arial", 18, "bold"))
        label_record.grid(row=0, column=0, sticky="w", padx=10, pady=5)
            
        # Select Item Option Menu
        optionmenu_var = ctk.StringVar(value="Select Registered Item")
        self.entry_item = ctk.CTkOptionMenu(self.record_frame, values=[item.name for item in self.items], variable=optionmenu_var) # Output from items.name
        self.entry_item.grid(row=1, column=0, padx=10, pady=5, columnspan=2, sticky="ew")
        
        # Amount and Price Input
        self.entry_price = ctk.CTkEntry(self.record_frame, placeholder_text="Price")
        self.entry_price.grid(row=2, column=0, padx=10, pady=5, sticky="ew")
        self.entry_amount = ctk.CTkEntry(self.record_frame, placeholder_text="Amount")
        self.entry_amount.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
        
        # Register Purchase and Register Sale Button
        self.btn_add_purchase = ctk.CTkButton(self.record_frame, text="Add Purchase", command=self.add_purchase)
        self.btn_add_purchase.grid(row=1, column=2, padx=10, pady=5, sticky="ew")
        
        self.btn_add_sale = ctk.CTkButton(self.record_frame, text="Add Sale", command=self.add_sale)
        self.btn_add_sale.grid(row=2, column=2, padx=10, pady=5, sticky="ew")
        
        # Custom Frame to fit 3 options in 2 columns
        currency_frame = ctk.CTkFrame(self.record_frame, fg_color="transparent")    # Inherits from record_frame
        currency_frame.grid(row=3, column=0, columnspan=3, pady=5, sticky="w")    # Third row
        currency_frame.columnconfigure(4, weight=1)
        # Currency options
        self.currency_var = ctk.StringVar(value="USD")  
        self.radio_usd = ctk.CTkRadioButton(currency_frame, text="USD ($)", variable=self.currency_var, value="USD")
        self.radio_rmb = ctk.CTkRadioButton(currency_frame, text="RMB (¥)", variable=self.currency_var, value="RMB")
        self.radio_brl = ctk.CTkRadioButton(currency_frame, text="BRL (R$)", variable=self.currency_var, value="BRL")
        self.radio_usd.grid(row=1, column=0, padx=(10, 5), pady=0, sticky="e") 
        self.radio_rmb.grid(row=1, column=1, padx=5, pady=0, sticky="e")
        self.radio_brl.grid(row=1, column=2, padx=5, pady=0, sticky="e")
     
     
    # The function _verify_input(), handles the cases that don't depend on item.variables
    def _verify_input(self, item, price, amount):
        
        # Verify if everything was correctly written / selected
        if not item or not price or not amount:
            self.text_output.insert("end", "\n-> Missing fields for entry!")
            return False, None, None
        if item == "Select Registered Item":
            self.text_output.insert("end", "\n-> No item selected!")
            return False, None, None
        
        # Eliminate unexpected values
        try:
            price = price.replace(",", ".")
            price = float(price)
        except:
            self.text_output.insert("end", "\n-> Inserted Price is not a number!")
            return False, None, None
        try:
            amount = int(amount)
        except:
            self.text_output.insert("end", "\n-> Inserted Amount is not an integer!")
            return False, None, None
        
        # Avoid zeros going into the .json
        if price == 0:
            self.text_output.insert("end", "\n-> Inserted Price is 0")
            return False, None, None
        if amount == 0:
            self.text_output.insert("end", "\n-> Inserted Amount is 0")
            return False, None, None
        
        # Return normalized price (2 -> 2.00, 2,00 -> 2.00)
        return True, price, amount
    
    # Searches for the selected item on items, that is the dictionary with "item" objects
    def _get_item(self, item):
        for target_item in self.items:
            if item == target_item.name:
                return target_item 
        
    
    def add_purchase(self):
        
        item = self.entry_item.get()
        currency = self.currency_var.get()
        
        valid, price, amount = self._verify_input(item, self.entry_price.get(), self.entry_amount.get())
        if not valid:
            return
        
        target_item = self._get_item(item)
        status = target_item.record_purchase(price, amount, currency)
        if status:
            self.text_output.insert("end", f"{status}")
            
        self.entry_price.delete(0, "end")
        self.entry_amount.delete(0, "end")

    def add_sale(self):
        
        item = self.entry_item.get()
        currency = self.currency_var.get()
        
        valid, price, amount = self._verify_input(item, self.entry_price.get(), self.entry_amount.get())
        if not valid:
            return
        
        target_item = self._get_item(item)
        status = target_item.record_sale(price, amount, currency)
        if status:
            self.text_output.insert("end", status)
            
        self.entry_price.delete(0, "end")
        self.entry_amount.delete(0, "end")

