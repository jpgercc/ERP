import customtkinter as ctk
import sqlite3
from tkinter import messagebox
import pyperclip

class CustomerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("green")

        self.title("Biss Manager - Clientes")
        self.geometry("1000x600")
        self.iconbitmap('finalizado.ico')

        # Connect to the database
        self.conn = sqlite3.connect("customers.db")
        self.cursor = self.conn.cursor()
        self.create_tables()

        # Create the add customer button
        self.add_customer_button = ctk.CTkButton(self, text="Adicionar Cliente", command=self.show_add_customer_form)
        self.add_customer_button.pack(pady=10)

        # Create search bar
        self.search_entry = ctk.CTkEntry(self, placeholder_text="Pesquisar Nome")
        self.search_entry.pack(pady=10)
        self.search_button = ctk.CTkButton(self, text="Pesquisar", command=self.search_customers)
        self.search_button.pack(pady=10)

        # Create a scrollable frame for listing customers
        self.scrollable_frame = ctk.CTkScrollableFrame(self)
        self.scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Display customers initially
        self.display_customers()

    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY,
                name TEXT,
                address TEXT,
                birth_date TEXT,
                cep TEXT,
                rg TEXT,
                cpf TEXT,
                ticket REAL,
                whatsapp TEXT,
                phone TEXT,
                email TEXT,
                last_purchases TEXT,
                balance REAL
            )
        """)
        self.conn.commit()

    def show_add_customer_form(self):
        self.add_customer_window = ctk.CTkToplevel(self)
        self.add_customer_window.attributes('-topmost', True)
        self.add_customer_window.title("Biss Manager - Adicionar Cliente")
        self.add_customer_window.geometry("400x600")
        self.after(200, lambda: self.add_customer_window.iconbitmap("finalizado.ico"))

        self.add_customer_frame = ctk.CTkScrollableFrame(self.add_customer_window)
        self.add_customer_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.customer_name_label = ctk.CTkLabel(self.add_customer_frame, text="Nome:")
        self.customer_name_label.pack(pady=5)
        self.customer_name_entry = ctk.CTkEntry(self.add_customer_frame)
        self.customer_name_entry.pack(pady=5)

        self.customer_address_label = ctk.CTkLabel(self.add_customer_frame, text="Endereço:")
        self.customer_address_label.pack(pady=5)
        self.customer_address_entry = ctk.CTkEntry(self.add_customer_frame)
        self.customer_address_entry.pack(pady=5)

        self.customer_birth_date_label = ctk.CTkLabel(self.add_customer_frame, text="Data de Nascimento:")
        self.customer_birth_date_label.pack(pady=5)
        self.customer_birth_date_entry = ctk.CTkEntry(self.add_customer_frame)
        self.customer_birth_date_entry.pack(pady=5)

        self.customer_cep_label = ctk.CTkLabel(self.add_customer_frame, text="CEP:")
        self.customer_cep_label.pack(pady=5)
        self.customer_cep_entry = ctk.CTkEntry(self.add_customer_frame)
        self.customer_cep_entry.pack(pady=5)

        self.customer_rg_label = ctk.CTkLabel(self.add_customer_frame, text="RG:")
        self.customer_rg_label.pack(pady=5)
        self.customer_rg_entry = ctk.CTkEntry(self.add_customer_frame)
        self.customer_rg_entry.pack(pady=5)

        self.customer_cpf_label = ctk.CTkLabel(self.add_customer_frame, text="CPF:")
        self.customer_cpf_label.pack(pady=5)
        self.customer_cpf_entry = ctk.CTkEntry(self.add_customer_frame)
        self.customer_cpf_entry.pack(pady=5)

        self.customer_ticket_label = ctk.CTkLabel(self.add_customer_frame, text="Ticket Médio:")
        self.customer_ticket_label.pack(pady=5)
        self.customer_ticket_entry = ctk.CTkEntry(self.add_customer_frame)
        self.customer_ticket_entry.pack(pady=5)

        self.customer_whatsapp_label = ctk.CTkLabel(self.add_customer_frame, text="WhatsApp (link):")
        self.customer_whatsapp_label.pack(pady=5)
        self.customer_whatsapp_entry = ctk.CTkEntry(self.add_customer_frame)
        self.customer_whatsapp_entry.pack(pady=5)

        self.customer_phone_label = ctk.CTkLabel(self.add_customer_frame, text="Telefone:")
        self.customer_phone_label.pack(pady=5)
        self.customer_phone_entry = ctk.CTkEntry(self.add_customer_frame)
        self.customer_phone_entry.pack(pady=5)

        self.customer_email_label = ctk.CTkLabel(self.add_customer_frame, text="Email (link):")
        self.customer_email_label.pack(pady=5)
        self.customer_email_entry = ctk.CTkEntry(self.add_customer_frame)
        self.customer_email_entry.pack(pady=5)

        self.customer_balance_label = ctk.CTkLabel(self.add_customer_frame, text="Saldo Devedor:")
        self.customer_balance_label.pack(pady=5)
        self.customer_balance_entry = ctk.CTkEntry(self.add_customer_frame)
        self.customer_balance_entry.pack(pady=5)

        self.add_customer_button = ctk.CTkButton(self.add_customer_frame, text="Adicionar", command=self.add_customer)
        self.add_customer_button.pack(pady=20)

    def add_customer(self):
        name = self.customer_name_entry.get()
        address = self.customer_address_entry.get()
        birth_date = self.customer_birth_date_entry.get()
        cep = self.customer_cep_entry.get()
        rg = self.customer_rg_entry.get()
        cpf = self.customer_cpf_entry.get()
        ticket = float(self.customer_ticket_entry.get())
        whatsapp = self.customer_whatsapp_entry.get()
        phone = self.customer_phone_entry.get()
        email = self.customer_email_entry.get()
        balance = float(self.customer_balance_entry.get())

        self.cursor.execute(
            "INSERT INTO customers (name, address, birth_date, cep, rg, cpf, ticket, whatsapp, phone, email, balance) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (name, address, birth_date, cep, rg, cpf, ticket, whatsapp, phone, email, balance))
        self.conn.commit()
        self.add_customer_window.destroy()
        self.display_customers()

    def show_edit_customer_form(self, customer_id):
        self.cursor.execute("SELECT * FROM customers WHERE id=?", (customer_id,))
        customer = self.cursor.fetchone()

        self.edit_customer_window = ctk.CTkToplevel(self)
        self.edit_customer_window.attributes('-topmost', True)
        self.edit_customer_window.title("Biss Manager - Editar Cliente")
        self.edit_customer_window.geometry("400x600")
        self.after(200, lambda: self.edit_customer_window.iconbitmap("finalizado.ico"))

        self.edit_customer_frame = ctk.CTkScrollableFrame(self.edit_customer_window)
        self.edit_customer_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.edit_customer_name_label = ctk.CTkLabel(self.edit_customer_frame, text="Nome:")
        self.edit_customer_name_label.pack(pady=5)
        self.edit_customer_name_entry = ctk.CTkEntry(self.edit_customer_frame)
        self.edit_customer_name_entry.insert(0, customer[1])
        self.edit_customer_name_entry.pack(pady=5)

        self.edit_customer_address_label = ctk.CTkLabel(self.edit_customer_frame, text="Endereço:")
        self.edit_customer_address_label.pack(pady=5)
        self.edit_customer_address_entry = ctk.CTkEntry(self.edit_customer_frame)
        self.edit_customer_address_entry.insert(0, customer[2])
        self.edit_customer_address_entry.pack(pady=5)

        self.edit_customer_birth_date_label = ctk.CTkLabel(self.edit_customer_frame, text="Data de Nascimento:")
        self.edit_customer_birth_date_label.pack(pady=5)
        self.edit_customer_birth_date_entry = ctk.CTkEntry(self.edit_customer_frame)
        self.edit_customer_birth_date_entry.insert(0, customer[3])
        self.edit_customer_birth_date_entry.pack(pady=5)

        self.edit_customer_cep_label = ctk.CTkLabel(self.edit_customer_frame, text="CEP:")
        self.edit_customer_cep_label.pack(pady=5)
        self.edit_customer_cep_entry = ctk.CTkEntry(self.edit_customer_frame)
        self.edit_customer_cep_entry.insert(0, customer[4])
        self.edit_customer_cep_entry.pack(pady=5)

        self.edit_customer_rg_label = ctk.CTkLabel(self.edit_customer_frame, text="RG:")
        self.edit_customer_rg_label.pack(pady=5)
        self.edit_customer_rg_entry = ctk.CTkEntry(self.edit_customer_frame)
        self.edit_customer_rg_entry.insert(0, customer[5])
        self.edit_customer_rg_entry.pack(pady=5)

        self.edit_customer_cpf_label = ctk.CTkLabel(self.edit_customer_frame, text="CPF:")
        self.edit_customer_cpf_label.pack(pady=5)
        self.edit_customer_cpf_entry = ctk.CTkEntry(self.edit_customer_frame)
        self.edit_customer_cpf_entry.insert(0, customer[6])
        self.edit_customer_cpf_entry.pack(pady=5)

        self.edit_customer_ticket_label = ctk.CTkLabel(self.edit_customer_frame, text="Ticket Médio:")
        self.edit_customer_ticket_label.pack(pady=5)
        self.edit_customer_ticket_entry = ctk.CTkEntry(self.edit_customer_frame)
        self.edit_customer_ticket_entry.insert(0, customer[7])
        self.edit_customer_ticket_entry.pack(pady=5)

        self.edit_customer_whatsapp_label = ctk.CTkLabel(self.edit_customer_frame, text="WhatsApp (link):")
        self.edit_customer_whatsapp_label.pack(pady=5)
        self.edit_customer_whatsapp_entry = ctk.CTkEntry(self.edit_customer_frame)
        self.edit_customer_whatsapp_entry.insert(0, customer[8])
        self.edit_customer_whatsapp_entry.pack(pady=5)

        self.edit_customer_phone_label = ctk.CTkLabel(self.edit_customer_frame, text="Telefone:")
        self.edit_customer_phone_label.pack(pady=5)
        self.edit_customer_phone_entry = ctk.CTkEntry(self.edit_customer_frame)
        self.edit_customer_phone_entry.insert(0, customer[9])
        self.edit_customer_phone_entry.pack(pady=5)

        self.edit_customer_email_label = ctk.CTkLabel(self.edit_customer_frame, text="Email (link):")
        self.edit_customer_email_label.pack(pady=5)
        self.edit_customer_email_entry = ctk.CTkEntry(self.edit_customer_frame)
        self.edit_customer_email_entry.insert(0, customer[10])
        self.edit_customer_email_entry.pack(pady=5)

        self.edit_customer_balance_label = ctk.CTkLabel(self.edit_customer_frame, text="Saldo Devedor:")
        self.edit_customer_balance_label.pack(pady=5)
        self.edit_customer_balance_entry = ctk.CTkEntry(self.edit_customer_frame)
        self.edit_customer_balance_entry.insert(0, customer[12])
        self.edit_customer_balance_entry.pack(pady=5)

        self.edit_customer_button = ctk.CTkButton(self.edit_customer_frame, text="Salvar", command=lambda: self.save_customer_edit(customer_id))
        self.edit_customer_button.pack(pady=20)

    def save_customer_edit(self, customer_id):
        name = self.edit_customer_name_entry.get()
        address = self.edit_customer_address_entry.get()
        birth_date = self.edit_customer_birth_date_entry.get()
        cep = self.edit_customer_cep_entry.get()
        rg = self.edit_customer_rg_entry.get()
        cpf = self.edit_customer_cpf_entry.get()
        ticket = float(self.edit_customer_ticket_entry.get())
        whatsapp = self.edit_customer_whatsapp_entry.get()
        phone = self.edit_customer_phone_entry.get()
        email = self.edit_customer_email_entry.get()
        balance = float(self.edit_customer_balance_entry.get())

        self.cursor.execute(
            "UPDATE customers SET name=?, address=?, birth_date=?, cep=?, rg=?, cpf=?, ticket=?, whatsapp=?, phone=?, email=?, balance=? WHERE id=?",
            (name, address, birth_date, cep, rg, cpf, ticket, whatsapp, phone, email, balance, customer_id))
        self.conn.commit()
        self.edit_customer_window.destroy()
        self.display_customers()

    def search_customers(self):
        search_query = self.search_entry.get()
        self.cursor.execute("SELECT * FROM customers WHERE name LIKE ?", ('%' + search_query + '%',))
        customers = self.cursor.fetchall()
        self.display_customers(customers)

    def delete_customer(self, customer_id):
        self.cursor.execute("DELETE FROM customers WHERE id=?", (customer_id,))
        self.conn.commit()
        self.display_customers()

    def display_customers(self, customers=None):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        if customers is None:
            self.cursor.execute("SELECT * FROM customers")
            customers = self.cursor.fetchall()

        for customer in customers:
            customer_frame = ctk.CTkFrame(self.scrollable_frame)
            customer_frame.pack(pady=5, fill="x", expand=True)

            customer_button = ctk.CTkButton(customer_frame, text=customer[1],
                                            command=lambda cust_id=customer[0]: self.show_customer_details(cust_id))
            customer_button.pack(side='left', padx=5, pady=5)

            edit_button = ctk.CTkButton(customer_frame, text="Editar",
                                        command=lambda cust_id=customer[0]: self.show_edit_customer_form(cust_id))
            edit_button.pack(side='left', padx=5, pady=5)

            delete_button = ctk.CTkButton(customer_frame, text="Excluir",
                                          command=lambda cust_id=customer[0]: self.delete_customer(cust_id))
            delete_button.pack(side='left', padx=5, pady=5)

    def show_customer_details(self, customer_id):
        self.cursor.execute("SELECT * FROM customers WHERE id=?", (customer_id,))
        customer = self.cursor.fetchone()
        details = f"Nome: {customer[1]}\nEndereço: {customer[2]}\nData de Nascimento: {customer[3]}\nCEP: {customer[4]}\nRG: {customer[5]}\nCPF: {customer[6]}\nTicket Médio: {customer[7]}\nWhatsApp: {customer[8]}\nTelefone: {customer[9]}\nEmail: {customer[10]}\nÚltimas Compras: {customer[11]}\nSaldo Devedor: {customer[12]}"
        messagebox.showinfo("Detalhes do Cliente", details)


if __name__ == "__main__":
    app = CustomerApp()
    app.mainloop()
