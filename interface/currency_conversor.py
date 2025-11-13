import customtkinter as ctk

class CurrencyConversor:
    
    def __init__(self, parent):
        self.parent = parent
        self._build_ui()
    
    def _build_ui(self):
        


        
        currency_frame = ctk.CTkFrame(self.parent, fg_color="transparent")    # Inherits from record_frame

        # Currency options
        self.currency_var = ctk.StringVar(value="USD")  
        self.radio_usd = ctk.CTkRadioButton(currency_frame, text="USD ($)", variable=self.currency_var, value="USD")
        self.radio_rmb = ctk.CTkRadioButton(currency_frame, text="RMB (¥)", variable=self.currency_var, value="RMB")
        self.radio_brl = ctk.CTkRadioButton(currency_frame, text="BRL (R$)", variable=self.currency_var, value="BRL")
        self.radio_usd.grid(row=1, column=0, padx=(10, 5), pady=0, sticky="e") 
        self.radio_rmb.grid(row=1, column=1, padx=5, pady=0, sticky="e")
        self.radio_brl.grid(row=1, column=2, padx=5, pady=0, sticky="e")

