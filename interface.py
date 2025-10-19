import customtkinter as ctk

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
        self._register_item(self.left_frame)
        
        

        
        # Campos de entrada

        # ====== FRAME DIREITO (LOG / OUTPUT) ====== #
        self.right_frame = ctk.CTkFrame(self.main_frame)
        self.right_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
    

        self.label_log = ctk.CTkLabel(
            self.right_frame,
            text="Action Log",
            font=("Arial", 18, "bold"),
        )
        self.label_log.pack(pady=10)

        self.text_output = ctk.CTkTextbox(self.right_frame, width=500, height=500)
        self.text_output.pack(padx=10, pady=10, fill="both", expand=True)
        self.text_output.insert("0.0", "Log initialized...\n")
        
        
        
        self.transaction_recorder = TransactionRecorder(self.left_frame, self.items, self.text_output)

     
    def _register_item(self, parent):
        
        # Frame Configuration
        
        self.register_frame = ctk.CTkFrame(parent)   # Inherits from main_frame
        self.register_frame.pack(padx=10, pady=(0, 10), fill="x")

        # Subtitle
        label_register = ctk.CTkLabel(self.register_frame, text="Register New Item", font=("Arial", 18, "bold"))
        label_register.grid(row=0, column=0, sticky="w", padx=10, pady=5)

    def clear_log(self):
        self.text_output.delete("0.0", "end")
        self.text_output.insert("0.0", "Log cleared...\n")







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
    
    def _verify_input(self, item, price, amount):
        
        if not item or not price or not amount:
            self.text_output.insert("end", "\n-> Missing fields for purchase entry!")
            return False, None
        if item == "Select Registered Item":
            self.text_output.insert("end", "\n-> No item selected!")
            return False, None
        
        # Eliminate strings        
        try:
            price = price.replace(",", ".")
            price = float(price)
        except:
            self.text_output.insert("end", "\n-> Inserted Price is not a number!")
            return False, None
        try:
            amount = float(amount)
        except:
            self.text_output.insert("end", "\n-> Inserted Amount is not a number!")
            return False, None
        
        # Eliminate float for amount
        if amount.is_integer() == False:
            self.text_output.insert("end", "\n-> Inserted Amount is a float!")
            return False, None

        # Return normalized price (2 -> 2.00, 2,00 -> 2.00)
        return True, price

    def _get_currency(self):
        currency = self.currency_var.get()
        if currency == "USD":
            return '$'
        elif currency == "RMB":
            return '¥'
        else:
            return "R$"
    
    def add_purchase(self):
        
        item = self.entry_item.get()
        price = self.entry_price.get()
        amount = self.entry_amount.get()
        
        valid, price = self._verify_input(item, price, amount)
        if not valid:
            return
        currency_symbol = self._get_currency()

        # chama no main.py e printa o retornado
        self.text_output.insert("end", f"\n-> Purchase Added: {item} - {currency_symbol}{price:.2f} x {amount}")
        self.entry_price.delete(0, "end")
        self.entry_amount.delete(0, "end")


    def add_sale(self):
        
        item = self.entry_item.get()
        price = self.entry_price.get()
        amount = self.entry_amount.get()
        
        valid, price = self._verify_input(item, price, amount)
        if not valid:
            return
        currency_symbol = self._get_currency()

        self.text_output.insert("end", f"\n-> Sale Added: {item} - {currency_symbol}{price:.2f} x {amount}")
        self.entry_price.delete(0, "end")
        self.entry_amount.delete(0, "end")


