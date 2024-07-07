import customtkinter as ctk
import sqlite3


class HistoricoDeVendas(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Histórico de Vendas")
        self.geometry("600x400")

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
        query = self.search_entry.get()
        self.cursor.execute("SELECT * FROM sales WHERE client_name LIKE ? OR client_cpf LIKE ?", (f'%{query}%', f'%{query}%'))
        sales = self.cursor.fetchall()
        self.display_sales(sales)

    def display_sales(self, sales=None):
        # Clear the previous sales
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        if sales is None:
            self.cursor.execute("SELECT * FROM sales")
            sales = self.cursor.fetchall()

        for sale in sales:
            sale_info = (f"Client Name: {sale[1]}\n"
                         f"Client CPF: {sale[2]}\n"
                         f"Company CNPJ: {sale[3]}\n"
                         f"Items:\n{sale[4]}\n"
                         f"Total Amount: ${sale[5]:.2f}\n"
                         f"Payment Method: {sale[6]}\n"
                         f"Installments: {sale[7]}\n"
                         f"Invoice: {sale[8]}\n"
                         "----------------------------------------\n")

            sale_label = ctk.CTkLabel(self.scrollable_frame, text=sale_info)
            sale_label.pack(pady=5, anchor="w")

            # Delete Button (without confirmation dialog)
            delete_button = ctk.CTkButton(self.scrollable_frame, text="Excluir", command=lambda sale_id=sale[0]: self.delete_sale(sale_id))
            delete_button.pack(pady=2)

    def delete_sale(self, sale_id):
        self.cursor.execute("DELETE FROM sales WHERE id = ?", (sale_id,))
        self.conn.commit()
        self.display_sales()  # Update displayed sales

if __name__ == "__main__":
    app = HistoricoDeVendas()
    app.mainloop()