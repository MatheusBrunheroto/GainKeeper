import customtkinter as ctk



class Log:
    
    def __init__(self, parent, items):
        
        self.parent = parent
        self.items = items
        self._build_ui()
    
    
    def _build_ui(self):

        self.label_log = ctk.CTkLabel(self.parent, text="Action Log", font=("Arial", 18, "bold"))
        self.label_log.pack(pady=10)

        
        self.text_output = ctk.CTkTextbox(self.parent, width=500, height=450)
        self.text_output.rowconfigure(1, weight=0)
        # self.text_output.pack(padx=10, pady=10, fill="both", expand=True)
        self.text_output.insert("0.0", "Log initialized...\n\n")
        self.text_output.pack(padx=10, pady=10, fill="both", expand=True)
        self.text_output.tag_config("bad", foreground="red")
        self.text_output.tag_config("good", foreground="green")
        self.text_output.tag_config("neutral", foreground="orange")
        
        self.text_output.configure(state="disabled")
        
    def overview(self):
        print("X")