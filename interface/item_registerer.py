import customtkinter as ctk
from stock.item import Item

class ItemRegisterer:
    
    def __init__(self, parent, items, text_output):
        self.parent = parent
        self.items = items
        self.text_output = text_output
        
        # Used to "ping" TransactionRecorder when a new item is added, updating the selection list in real time
        self.transaction_recorder = None
        
        self._build_ui()
        
    def _build_ui(self):

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
                self.text_output.insert("end", f"-> {name} is already registered!\n")
                return
            
        new_item = Item(name, {'purchases': [{'price': 0, 'amount': 0, 'currency': 0}],'sales': [{'price': 0, 'amount': 0, 'currency': 0}],'is_active': 0})
        self.items.append(new_item)
        self.transaction_recorder.entry_item.configure(values=[item.name for item in self.items])

        self.entry_name.delete(0, "end")
        self.text_output.insert("end", f"[+] New Item Registered: {name}.\n")