import customtkinter as ctk

class TransactionRecorder:
    
    def __init__(self, parent, items, text_output):
        self.parent = parent
        self.items = items
        self.text_output=text_output
        self._build_ui()
    
    
    def _build_ui(self):
   
        # Frame Configuration
        self.record_frame = ctk.CTkFrame(self.parent)
        self.record_frame.pack(padx=10, pady=(0, 10), fill="x")
    
        # Subtitle
        label_record = ctk.CTkLabel(self.record_frame, text="Record Transaction", font=("Arial", 18, "bold"))
        label_record.grid(row=0, column=0, sticky="w", padx=10, pady=5)
            
        # Select Item Option Menu
        optionmenu_var = ctk.StringVar(value="Select Registered Item")
        self.entry_item = ctk.CTkOptionMenu(self.record_frame, values=[item.name for item in self.items], variable=optionmenu_var, command=self.item_overview) # Output from items.name
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

    def item_overview(self, option):
        
        self.text_output.configure(state="normal")
        self.text_output.delete("0.0", "end")
        
        target_item = self._get_item(option)
        
        self.text_output.insert("end", f"{option} - ")
        if target_item.remaining_amount == 0:
            self.text_output.insert("end", "(Not in Stock)", "1")
        else:
            self.text_output.insert("end", f"x{target_item.remaining_amount} (CURRENT PRICE)")
        self.text_output.insert("end",":\n")    
        
        self.text_output.insert("end", f"│\n├── Purchases: x{target_item.total_purchase_amount} Units (≈ {target_item.average_purchase_price:.2f} each)\n")
        self.text_output.insert("end", f"│        ├── Total Purchase Price = {target_item.total_purchase_price:.2f}\n")
        
        if target_item.total_sale_amount == 0:
            self.text_output.insert("end", "\nNot enough data to calculate ROI", "1")
        else:
            self.text_output.insert("end", f"├── Sales: x{target_item.total_sale_amount} Units (≈ {target_item.average_sale_price:.2f} each)\n")
            self.text_output.insert("end", f"│        ├── Total Purchase Price = {target_item.total_sale_price:.2f}\n")
        
        
        self.text_output.configure(state="disabled")
        
        
        # self.text_output.insert("end", f"x{target_item.total_purchase_amount} Units (≈ {target_item.average_purchase_price:.2f} each)\n")