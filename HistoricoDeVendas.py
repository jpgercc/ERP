import customtkinter as ctk
import sqlite3
from tkinter import messagebox

class HistoricoDeVendas(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("system")  # Modos: "dark", "light", "system"
        ctk.set_default_color_theme("green")  # Temas: "blue", "green", "dark-blue"

        self.title("Biss Manager - Produtos")
        self.geometry("1000x500")
        self.iconbitmap('beaver.ico')

        # Create a scrollable frame
        self.scrollable_frame = ctk.CTkScrollableFrame(self)
        self.scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Search bar
        self.search_label = ctk.CTkLabel(self.scrollable_frame, text="Buscar por Cliente (Nome ou CPF):")
        self.search_label.pack(pady=5)
        self.search_entry = ctk.CTkEntry(self.scrollable_frame)
        self.search_entry.pack(pady=5)
        self.search_button = ctk.CTkButton(self.scrollable_frame, text="Buscar", command=self.search_sales)
        self.search_button.pack(pady=5)

        # Connect to the database
        self.conn = sqlite3.connect("sales.db")
        self.cursor = self.conn.cursor()

        # Display all sales initially
        self.display_sales()

    def search_sales(self):
        query = f"%{self.search_entry.get()}%"
        self.cursor.execute("SELECT * FROM sales WHERE client_name LIKE ? OR client_cpf LIKE ? OR purchase_date LIKE ?", (query, query, query))
        sales = self.cursor.fetchall()
        self.display_sales(sales)

    def display_sales(self, sales=None):
        # Clear the previous sales except the search widgets
        for widget in self.scrollable_frame.winfo_children():
            if isinstance(widget, ctk.CTkLabel) and widget != self.search_label or isinstance(widget, ctk.CTkButton) and widget != self.search_button:
                widget.destroy()

        if sales is None:
            # Fetch all sales if no search was performed
            self.cursor.execute("SELECT * FROM sales")
            sales = self.cursor.fetchall()

        for sale in sales:
            sale_info = self.format_sale_info(sale)  # Use separate function for formatting
            sale_label = ctk.CTkLabel(self.scrollable_frame, text=sale_info)
            sale_label.pack(pady=5, anchor="w")

            # Delete Button with confirmation
            delete_button = ctk.CTkButton(self.scrollable_frame, text="Excluir",
                                           command=lambda sale_id=sale[0]: self.delete_sale(sale_id))
            delete_button.pack(pady=2)

    def format_sale_info(self, sale):
        # Function to format sale details in a reusable way
        client_name = sale[1]
        client_cpf = sale[2]
        company_cnpj = sale[3]
        items = sale[4]
        total_amount = sale[5]
        payment_method = sale[6]
        installments = sale[7]
        invoice = sale[8]
        purchase_date = sale[9] if len(sale) > 9 else "N/A"  # Handle missing purchase_date

        return (f"Client Name: {client_name}\n"
                f"Client CPF: {client_cpf}\n"
                f"Company CNPJ: {company_cnpj}\n"
                f"Items:\n{items}\n"
                f"Total Amount: ${total_amount:.2f}\n"
                f"Payment Method: {payment_method}\n"
                f"Installments: {installments}\n"
                f"Invoice: {invoice}\n"
                f"Purchase Date: {purchase_date}\n"
                "----------------------------------------\n")

    def delete_sale(self, sale_id):
        if messagebox.askquestion("Confirmar exclusão", "Deseja mesmo excluir esta venda?") == 'yes':
            self.cursor.execute("DELETE FROM sales WHERE id = ?", (sale_id,))
            self.conn.commit()
            self.display_sales()  # Update displayed sales after deletion


if __name__ == "__main__":
    app = HistoricoDeVendas()
    app.mainloop()
