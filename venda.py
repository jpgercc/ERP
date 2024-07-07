import customtkinter as ctk
import sqlite3
import subprocess
from tkinter import messagebox
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


class CashierApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Cashier App")
        self.geometry("400x600")

        self.items = []

        # Create a scrollable frame
        self.scrollable_frame = ctk.CTkScrollableFrame(self)
        self.scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Initialize the database
        self.init_db()

        # Create UI components within the scrollable frame
        self.create_widgets()

    def init_db(self):
        # Connect to the database (or create it if it doesn't exist)
        self.conn = sqlite3.connect("sales.db")
        self.cursor = self.conn.cursor()

        # Create a table for sales
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY,
            client_name TEXT,
            client_cpf TEXT,
            company_cnpj TEXT,
            items TEXT,
            total_amount REAL,
            payment_method TEXT,
            installments INTEGER,
            invoice TEXT
        )''')
        self.conn.commit()

    def create_widgets(self):
        # Input fields for item details
        self.item_name_label = ctk.CTkLabel(self.scrollable_frame, text="Item Name:")
        self.item_name_label.pack(pady=5)

        self.item_name_entry = ctk.CTkEntry(self.scrollable_frame)
        self.item_name_entry.pack(pady=5)

        self.item_price_label = ctk.CTkLabel(self.scrollable_frame, text="Item Price:")
        self.item_price_label.pack(pady=5)

        self.item_price_entry = ctk.CTkEntry(self.scrollable_frame)
        self.item_price_entry.pack(pady=5)

        self.item_quantity_label = ctk.CTkLabel(self.scrollable_frame, text="Quantity:")
        self.item_quantity_label.pack(pady=5)

        self.item_quantity_entry = ctk.CTkEntry(self.scrollable_frame)
        self.item_quantity_entry.pack(pady=5)

        # Button to add item
        self.add_item_button = ctk.CTkButton(self.scrollable_frame, text="Add Item", command=self.add_item)
        self.add_item_button.pack(pady=10)

        # Textbox to display added items
        self.item_textbox = ctk.CTkTextbox(self.scrollable_frame, height=200)
        self.item_textbox.pack(pady=10, fill="both", expand=True)

        # Label to display total amount
        self.total_label = ctk.CTkLabel(self.scrollable_frame, text="Total: $0.00")
        self.total_label.pack(pady=10)

        # Payment options
        self.payment_label = ctk.CTkLabel(self.scrollable_frame, text="Payment Method:")
        self.payment_label.pack(pady=5)

        self.payment_method = ctk.CTkComboBox(self.scrollable_frame, values=["Cash", "Debit", "Credit"],
                                              state="readonly")
        self.payment_method.pack(pady=5)

        # Credit installments
        self.installments_label = ctk.CTkLabel(self.scrollable_frame, text="Installments (for credit):")
        self.installments_label.pack(pady=5)

        self.installments_entry = ctk.CTkEntry(self.scrollable_frame)
        self.installments_entry.pack(pady=5)

        # Client information
        self.client_label = ctk.CTkLabel(self.scrollable_frame, text="Client Name:")
        self.client_label.pack(pady=5)

        self.client_entry = ctk.CTkEntry(self.scrollable_frame)
        self.client_entry.pack(pady=5)

        self.client_cpf_label = ctk.CTkLabel(self.scrollable_frame, text="Client CPF:")
        self.client_cpf_label.pack(pady=5)

        self.client_cpf_entry = ctk.CTkEntry(self.scrollable_frame)
        self.client_cpf_entry.pack(pady=5)

        self.company_cnpj_label = ctk.CTkLabel(self.scrollable_frame, text="Company CNPJ:")
        self.company_cnpj_label.pack(pady=5)

        self.company_cnpj_entry = ctk.CTkEntry(self.scrollable_frame)
        self.company_cnpj_entry.pack(pady=5)

        # Button to calculate total and issue invoice
        self.calculate_button = ctk.CTkButton(self.scrollable_frame, text="Calculate Total and Issue Invoice",
                                              command=self.calculate_total_and_invoice)
        self.calculate_button.pack(pady=10)

        # Button to view all sales
        self.view_sales_button = ctk.CTkButton(self.scrollable_frame, text="View All Sales",
                                               command=self.open_historico_de_vendas)
        self.view_sales_button.pack(pady=10)

    def add_item(self):
        name = self.item_name_entry.get()
        try:
            price = float(self.item_price_entry.get())
            quantity = int(self.item_quantity_entry.get())
            total_price = price * quantity
            item_details = f"{name} - ${price:.2f} x {quantity} = ${total_price:.2f}\n"
            self.items.append((name, price, quantity, total_price))
            self.item_textbox.insert("end", item_details)
            self.clear_entries()
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter valid price and quantity.")

    def clear_entries(self):
        self.item_name_entry.delete(0, "end")
        self.item_price_entry.delete(0, "end")
        self.item_quantity_entry.delete(0, "end")

    def calculate_total_and_invoice(self):
        total_amount = sum(item[3] for item in self.items)
        payment_method = self.payment_method.get()

        if payment_method == "Credit":
            try:
                installments = int(self.installments_entry.get())
                if installments <= 4:
                    total_with_interest = total_amount
                else:
                    total_with_interest = total_amount * (1 + 0.05 * (installments - 4))
                total_amount = total_with_interest
                invoice = f"Total: ${total_amount:.2f} in {installments} installments of ${total_amount / installments:.2f} each."
            except ValueError:
                messagebox.showerror("Invalid input", "Please enter valid number of installments.")
                return
        else:
            invoice = f"Total: ${total_amount:.2f} paid by {payment_method}."

        self.total_label.configure(text=f"Total: ${total_amount:.2f}")
        self.generate_invoice_pdf(invoice)
        self.save_sale(total_amount, payment_method, installments if payment_method == "Credit" else 1, invoice)
        self.items.clear()
        self.item_textbox.delete("1.0", "end")

    def generate_invoice_pdf(self, invoice):
        client_name = self.client_entry.get()
        client_cpf = self.client_cpf_entry.get()
        company_cnpj = self.company_cnpj_entry.get()

        if not client_name or not client_cpf or not company_cnpj:
            messagebox.showerror("Missing Information", "Please enter client name, client CPF, and company CNPJ.")
            return

        c = canvas.Canvas("invoice.pdf", pagesize=letter)
        width, height = letter

        c.drawString(100, height - 50, f"Client Name: {client_name}")
        c.drawString(100, height - 70, f"Client CPF: {client_cpf}")
        c.drawString(100, height - 90, f"Company CNPJ: {company_cnpj}")

        c.drawString(100, height - 130, "Items:")
        y_position = height - 150
        for item in self.items:
            c.drawString(100, y_position, f"{item[0]} - ${item[1]:.2f} x {item[2]} = ${item[3]:.2f}")
            y_position -= 20

        c.drawString(100, y_position - 20, invoice)

        c.save()
        messagebox.showinfo("Invoice Generated", "The invoice has been generated as invoice.pdf")

    def save_sale(self, total_amount, payment_method, installments, invoice):
        client_name = self.client_entry.get()
        client_cpf = self.client_cpf_entry.get()
        company_cnpj = self.company_cnpj_entry.get()
        items_str = "\n".join([f"{item[0]} - ${item[1]:.2f} x {item[2]} = ${item[3]:.2f}" for item in self.items])

        self.cursor.execute('''INSERT INTO sales (client_name, client_cpf, company_cnpj, items, total_amount, payment_method, installments, invoice)
                               VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                            (client_name, client_cpf, company_cnpj, items_str, total_amount, payment_method,
                             installments, invoice))
        self.conn.commit()

    def open_historico_de_vendas(self):
        subprocess.Popen(['python', 'historico_de_vendas.py'])

if __name__ == "__main__":
    app = CashierApp()
    app.mainloop()
