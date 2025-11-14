import customtkinter as ctk

from stock.item import Item

from interface.item_registerer import ItemRegisterer
from interface.transaction_recorder import TransactionRecorder
from interface.log import Log
from interface.currency_conversor import CurrencyConversor


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")
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
        


        # ====== FRAME DIREITO (LOG / OUTPUT) ====== #
        self.right_frame = ctk.CTkFrame(self.main_frame)
        self.right_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.right_frame.rowconfigure(1, weight=1)
        
        
        self.log = Log(self.right_frame, self.items)
        self.currency_conversor = CurrencyConversor(self.right_frame, self.items)
        
        self.item_registerer = ItemRegisterer(self.left_frame, self.items, self.log.text_output)
        self.transaction_recorder = TransactionRecorder(self.left_frame, self.items, self.log.text_output)
        
        # Reference of "transaction_recorder" inside of "item_registerer", so "item_registerer" can update the list in "transaction_recorder"
        self.item_registerer.transaction_recorder = self.transaction_recorder
        








