import customtkinter as ctk

# Configuração inicial da janela
ctk.set_appearance_mode("dark")      # modos: "light", "dark", "system"
ctk.set_default_color_theme("blue")  # temas: "blue", "green", "dark-blue"

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configuração da janela
        self.title("Financial Dashboard")
        self.geometry("600x400")
        self.resizable(False, False)

        # Título
        self.label_title = ctk.CTkLabel(
            self,
            text="📊 Financial Overview",
            font=("Arial", 24, "bold"),
        )
        self.label_title.pack(pady=20)

        # Frame principal
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(padx=20, pady=10, fill="both", expand=True)

        # Entradas
        self.entry_item = ctk.CTkEntry(self.main_frame, placeholder_text="Item name")
        self.entry_item.grid(row=0, column=0, padx=10, pady=10)

        self.entry_price = ctk.CTkEntry(self.main_frame, placeholder_text="Price")
        self.entry_price.grid(row=0, column=1, padx=10, pady=10)

        self.entry_amount = ctk.CTkEntry(self.main_frame, placeholder_text="Amount")
        self.entry_amount.grid(row=0, column=2, padx=10, pady=10)

        # Botões
        self.btn_add_purchase = ctk.CTkButton(
            self.main_frame,
            text="Add Purchase",
            command=self.add_purchase
        )
        self.btn_add_purchase.grid(row=1, column=0, padx=10, pady=10)

        self.btn_add_sale = ctk.CTkButton(
            self.main_frame,
            text="Add Sale",
            command=self.add_sale
        )
        self.btn_add_sale.grid(row=1, column=1, padx=10, pady=10)

        # Área de saída (resultados)
        self.text_output = ctk.CTkTextbox(self.main_frame, width=540, height=180)
        self.text_output.grid(row=2, column=0, columnspan=3, padx=10, pady=10)
        self.text_output.insert("0.0", "Results will appear here...")

    def add_purchase(self):
        item = self.entry_item.get()
        price = self.entry_price.get()
        amount = self.entry_amount.get()
        self.text_output.insert("end", f"\nPurchase Added: {item} - ${price} x {amount}")

    def add_sale(self):
        item = self.entry_item.get()
        price = self.entry_price.get()
        amount = self.entry_amount.get()
        self.text_output.insert("end", f"\nSale Added: {item} - ${price} x {amount}")


if __name__ == "__main__":
    app = App()
    app.mainloop()
