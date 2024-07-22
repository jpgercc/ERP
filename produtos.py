import customtkinter as ctk
import sqlite3
from tkinter import messagebox
import pyperclip
import subprocess
import sys

class InventoryApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("system")  # Modos: "dark", "light", "system"
        ctk.set_default_color_theme("green")  # Temas: "blue", "green", "dark-blue"

        self.title("Biss Manager - Produtos")
        self.geometry("1000x500")
        self.iconbitmap('beaver.ico')


        # Connect to the database
        self.conn = sqlite3.connect("products.db")
        self.cursor = self.conn.cursor()
        self.create_table()

        #BUTTOM MAIN
        self.main = ctk.CTkButton(self, text="Voltar ao Início", command=self.button_main)
        self.main.pack(side="right", pady=10)

        # Create the add product button
        self.add_product_button = ctk.CTkButton(self, text="Adicionar Produto", command=self.show_add_product_form)
        self.add_product_button.pack(pady=10)

        # Create a scrollable frame for product listing
        self.scrollable_frame = ctk.CTkScrollableFrame(self)
        self.scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Display all products initially
        self.display_products()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY,
                product_id TEXT,
                name TEXT,
                brand TEXT,
                price REAL,
                supplier_price REAL,
                quantity INTEGER,
                supplier_contact TEXT
            )
        """)
        self.conn.commit()

    def button_main(self):
        root = self.winfo_toplevel()
        subprocess.Popen([sys.executable, "main.py"])
        root.destroy()


    def show_add_product_form(self):

        self.add_product_window = ctk.CTkToplevel(self)
        self.add_product_window.attributes('-topmost', True)
        self.add_product_window.title("Biss Manager - Adicionar Produto")
        self.add_product_window.geometry("1000x500")

        # Product ID
        self.product_id_label = ctk.CTkLabel(self.add_product_window, text="ID do Produto:")
        self.product_id_label.pack(pady=5)
        self.product_id_entry = ctk.CTkEntry(self.add_product_window)
        self.product_id_entry.pack(pady=5)

        # Product Name
        self.product_name_label = ctk.CTkLabel(self.add_product_window, text="Nome do Produto:")
        self.product_name_label.pack(pady=5)
        self.product_name_entry = ctk.CTkEntry(self.add_product_window)
        self.product_name_entry.pack(pady=5)

        # Brand
        self.brand_label = ctk.CTkLabel(self.add_product_window, text="Marca:")
        self.brand_label.pack(pady=5)
        self.brand_entry = ctk.CTkEntry(self.add_product_window)
        self.brand_entry.pack(pady=5)

        # Price do fornecedor
        self.supplier_price_label = ctk.CTkLabel(self.add_product_window, text="Preço do Fonecedor:")
        self.supplier_price_label.pack(pady=5)
        self.supplier_price_entry = ctk.CTkEntry(self.add_product_window)
        self.supplier_price_entry.pack(pady=5)

        # Price
        self.price_label = ctk.CTkLabel(self.add_product_window, text="Preço:")
        self.price_label.pack(pady=5)
        self.price_entry = ctk.CTkEntry(self.add_product_window)
        self.price_entry.pack(pady=5)

        # Quantity
        self.quantity_label = ctk.CTkLabel(self.add_product_window, text="Quantidade em Estoque:")
        self.quantity_label.pack(pady=5)
        self.quantity_entry = ctk.CTkEntry(self.add_product_window)
        self.quantity_entry.pack(pady=5)

        # Supplier Contact
        self.supplier_contact_label = ctk.CTkLabel(self.add_product_window, text="Contato do Fornecedor:")
        self.supplier_contact_label.pack(pady=5)
        self.supplier_contact_entry = ctk.CTkEntry(self.add_product_window)
        self.supplier_contact_entry.pack(pady=5)

        # Add Product Button
        self.add_product_button = ctk.CTkButton(self.add_product_window, text="Adicionar", command=self.add_product)
        self.add_product_button.pack(pady=20)

    def show_edit_product_form(self, product):
        self.edit_product_window = ctk.CTkToplevel(self)
        self.edit_product_window.attributes('-topmost', True)
        self.edit_product_window.title("Alterar Produto")
        self.edit_product_window.geometry("1000x800")

        # Product ID
        self.product_id_label = ctk.CTkLabel(self.edit_product_window, text="ID do Produto:")
        self.product_id_label.pack(pady=5)
        self.product_id_entry = ctk.CTkEntry(self.edit_product_window)
        self.product_id_entry.insert(0, product[1])
        self.product_id_entry.pack(pady=5)

        # Product Name
        self.product_name_label = ctk.CTkLabel(self.edit_product_window, text="Nome do Produto:")
        self.product_name_label.pack(pady=5)
        self.product_name_entry = ctk.CTkEntry(self.edit_product_window)
        self.product_name_entry.insert(0, product[2])
        self.product_name_entry.pack(pady=5)

        # Brand
        self.brand_label = ctk.CTkLabel(self.edit_product_window, text="Marca:")
        self.brand_label.pack(pady=5)
        self.brand_entry = ctk.CTkEntry(self.edit_product_window)
        self.brand_entry.insert(0, product[3])
        self.brand_entry.pack(pady=5)

        # Price do fornecedor
        self.supplier_price_label = ctk.CTkLabel(self.edit_product_window, text="Preço do Fornecedor:")
        self.supplier_price_label.pack(pady=5)
        self.supplier_price_entry = ctk.CTkEntry(self.edit_product_window)
        self.supplier_price_entry.insert(0, product[5])
        self.supplier_price_entry.pack(pady=5)

        # Price
        self.price_label = ctk.CTkLabel(self.edit_product_window, text="Preço:")
        self.price_label.pack(pady=5)
        self.price_entry = ctk.CTkEntry(self.edit_product_window)
        self.price_entry.insert(0, product[4])
        self.price_entry.pack(pady=5)

        # Margin
        margin = ((product[4] - product[5]) / product[5]) * 100 if product[5] != 0 else 0

        # Calculate the profit in reais
        profit = product[4] - product[5]

        # Create and pack the margin label
        self.margin_label = ctk.CTkLabel(self.edit_product_window, text=f"Margem de Lucro: {margin:.2f}%")
        self.margin_label.pack(pady=5)

        # Create and pack the profit label
        self.profit_label = ctk.CTkLabel(self.edit_product_window, text=f"Lucro: R${profit:.2f}")
        self.profit_label.pack(pady=5)

        # Quantity
        self.quantity_label = ctk.CTkLabel(self.edit_product_window, text="Quantidade em Estoque:")
        self.quantity_label.pack(pady=5)
        self.quantity_entry = ctk.CTkEntry(self.edit_product_window)
        self.quantity_entry.insert(0, product[6])
        self.quantity_entry.pack(pady=5)

        # Supplier Contact
        self.supplier_contact_label = ctk.CTkLabel(self.edit_product_window, text="Contato do Fornecedor (Telefone):")
        self.supplier_contact_label.pack(pady=5)
        self.supplier_contact_entry = ctk.CTkEntry(self.edit_product_window)
        self.supplier_contact_entry.insert(0, product[7])
        self.supplier_contact_entry.pack(pady=5)

        # Edit Product Button
        self.edit_product_button = ctk.CTkButton(self.edit_product_window, text="Salvar",
                                                 command=lambda: self.edit_product(product[0]))
        self.edit_product_button.pack(pady=20)

    def add_product(self):
        product_id = self.product_id_entry.get()
        name = self.product_name_entry.get()
        brand = self.brand_entry.get()  # Novo
        price = float(self.price_entry.get())
        supplier_price = float(self.supplier_price_entry.get())
        quantity = int(self.quantity_entry.get())
        supplier_contact = self.supplier_contact_entry.get()

        self.cursor.execute(
            "INSERT INTO products (product_id, name, brand, price, supplier_price, quantity, supplier_contact) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (product_id, name, brand, price, supplier_price, quantity, supplier_contact))
        self.conn.commit()
        self.add_product_window.destroy()
        self.display_products()

    def edit_product(self, product_id):
        new_product_id = self.product_id_entry.get()
        new_name = self.product_name_entry.get()
        new_brand = self.brand_entry.get()  # Novo
        new_price = float(self.price_entry.get())
        new_supplier_price = float(self.supplier_price_entry.get())
        new_quantity = int(self.quantity_entry.get())
        new_supplier_contact = self.supplier_contact_entry.get()

        self.cursor.execute("""
            UPDATE products
            SET product_id = ?, name = ?, brand = ?, price = ?, supplier_price = ?, quantity = ?, supplier_contact = ?
            WHERE id = ?
        """, (new_product_id, new_name, new_brand, new_price, new_supplier_price, new_quantity, new_supplier_contact,
              product_id))
        self.conn.commit()
        self.edit_product_window.destroy()
        self.display_products()

    def display_products(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        self.cursor.execute("SELECT * FROM products")
        products = self.cursor.fetchall()

        for product in products:
            product_info = f"ID: {product[1]}, Nome: {product[2]}, Marca: {product[3]}, Preço: R${product[4]:.2f}, Quantidade: {product[6]}"
            product_label = ctk.CTkLabel(self.scrollable_frame, text=product_info)
            product_label.pack(pady=5, anchor="w")

            # Delete Button
            delete_button = ctk.CTkButton(self.scrollable_frame, text="Excluir",
                                          command=lambda product_id=product[0]: self.delete_product(product_id))
            delete_button.pack(side='left', padx=5, pady=2)

            # Edit Button
            edit_button = ctk.CTkButton(self.scrollable_frame, text="Alterar Informações",
                                        command=lambda product=product: self.show_edit_product_form(product))
            edit_button.pack(side='left', padx=5, pady=2)

            # Supplier Contact Button
            contact_button = ctk.CTkButton(self.scrollable_frame, text="Contato Fornecedor",
                                           command=lambda contact=product[7]: self.copy_to_clipboard(contact))
            contact_button.pack(side='left', padx=5, pady=2)

    def delete_product(self, product_id):
        if messagebox.askquestion("Confirmar exclusão", "Deseja mesmo excluir este produto?") == 'yes':
            self.cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
            self.conn.commit()
            self.display_products()

    def copy_to_clipboard(self, contact):
        pyperclip.copy(contact)
        messagebox.showinfo("Contato Copiado", f"O contato {contact} foi copiado para a área de transferência.")


if __name__ == "__main__":
    app = InventoryApp()
    app.mainloop()
