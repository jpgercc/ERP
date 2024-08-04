import customtkinter as ctk
import sqlite3
from tkinter import messagebox
import pyperclip
import os#teste

class InventoryApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("green")

        self.title("Biss Manager - Produtos")
        self.geometry("1000x600")
        self.iconbitmap('finalizado.ico')

        # Connect to the database
        self.conn = sqlite3.connect("products.db")
        self.cursor = self.conn.cursor()
        self.create_tables()

        # Create the add category button
        self.add_category_button = ctk.CTkButton(self, text="Adicionar Categoria", command=self.show_add_category_form)
        self.add_category_button.pack(pady=10)

        # Create the add product button
        self.add_product_button = ctk.CTkButton(self, text="Adicionar Produto", command=self.show_add_product_form)
        self.add_product_button.pack(pady=10)

        # Create a scrollable frame for listing categories or products
        self.scrollable_frame = ctk.CTkScrollableFrame(self)
        self.scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Display categories initially
        self.display_categories()

    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY,
                name TEXT
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY,
                product_id TEXT,
                name TEXT,
                brand TEXT,
                price REAL,
                supplier_price REAL,
                quantity INTEGER,
                supplier_contact TEXT,
                category_id INTEGER,
                FOREIGN KEY (category_id) REFERENCES categories (id)
            )
        """)
        self.conn.commit()

    def show_add_category_form(self):
        self.add_category_window = ctk.CTkToplevel(self)
        self.add_category_window.attributes('-topmost', True)
        self.add_category_window.title("Biss Manager - Adicionar Categoria")
        self.add_category_window.geometry("300x200")
        self.after(200, lambda: self.add_category_window.iconbitmap("finalizado.ico")) #icone funcionando engenbration


        self.category_name_label = ctk.CTkLabel(self.add_category_window, text="Nome da Categoria:")
        self.category_name_label.pack(pady=5)
        self.category_name_entry = ctk.CTkEntry(self.add_category_window)
        self.category_name_entry.pack(pady=5)

        self.add_category_button = ctk.CTkButton(self.add_category_window, text="Adicionar", command=self.add_category)
        self.add_category_button.pack(pady=20)

    def add_category(self):
        category_name = self.category_name_entry.get()
        self.cursor.execute("INSERT INTO categories (name) VALUES (?)", (category_name,))
        self.conn.commit()
        self.add_category_window.destroy()
        self.display_categories()

    def display_categories(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        self.cursor.execute("SELECT * FROM categories")
        categories = self.cursor.fetchall()

        for category in categories:
            category_frame = ctk.CTkFrame(self.scrollable_frame)
            category_frame.pack(pady=5, fill="x", expand=True)

            category_button = ctk.CTkButton(category_frame, text=category[1],
                                            command=lambda cat_id=category[0]: self.display_products(cat_id))
            category_button.pack(side='left', padx=5, pady=5)

            delete_button = ctk.CTkButton(category_frame, text="Excluir",
                                          command=lambda cat_id=category[0]: self.delete_category(cat_id))
            delete_button.pack(side='left', padx=5, pady=5)

    def show_add_product_form(self):
        self.add_product_window = ctk.CTkToplevel(self)
        self.add_product_window.attributes('-topmost', True)
        self.add_product_window.title("Biss Manager - Adicionar Produto")
        self.add_product_window.geometry("500x700")
        self.after(200, lambda: self.add_product_window.iconbitmap("finalizado.ico"))

        self.product_id_label = ctk.CTkLabel(self.add_product_window, text="ID do Produto:")
        self.product_id_label.pack(pady=5)
        self.product_id_entry = ctk.CTkEntry(self.add_product_window)
        self.product_id_entry.pack(pady=5)

        self.product_name_label = ctk.CTkLabel(self.add_product_window, text="Nome do Produto:")
        self.product_name_label.pack(pady=5)
        self.product_name_entry = ctk.CTkEntry(self.add_product_window)
        self.product_name_entry.pack(pady=5)

        self.brand_label = ctk.CTkLabel(self.add_product_window, text="Marca:")
        self.brand_label.pack(pady=5)
        self.brand_entry = ctk.CTkEntry(self.add_product_window)
        self.brand_entry.pack(pady=5)

        self.supplier_price_label = ctk.CTkLabel(self.add_product_window, text="Preço do Fornecedor:")
        self.supplier_price_label.pack(pady=5)
        self.supplier_price_entry = ctk.CTkEntry(self.add_product_window)
        self.supplier_price_entry.pack(pady=5)

        self.price_label = ctk.CTkLabel(self.add_product_window, text="Preço:")
        self.price_label.pack(pady=5)
        self.price_entry = ctk.CTkEntry(self.add_product_window)
        self.price_entry.pack(pady=5)

        self.quantity_label = ctk.CTkLabel(self.add_product_window, text="Quantidade em Estoque:")
        self.quantity_label.pack(pady=5)
        self.quantity_entry = ctk.CTkEntry(self.add_product_window)
        self.quantity_entry.pack(pady=5)

        self.supplier_contact_label = ctk.CTkLabel(self.add_product_window, text="Contato do Fornecedor:")
        self.supplier_contact_label.pack(pady=5)
        self.supplier_contact_entry = ctk.CTkEntry(self.add_product_window)
        self.supplier_contact_entry.pack(pady=5)

        self.category_label = ctk.CTkLabel(self.add_product_window, text="Categoria:")
        self.category_label.pack(pady=5)

        self.cursor.execute("SELECT * FROM categories")
        categories = self.cursor.fetchall()
        self.category_var = ctk.StringVar(self.add_product_window)
        self.category_var.set(categories[0][1])  # default value
        self.category_menu = ctk.CTkOptionMenu(self.add_product_window, variable=self.category_var, values=[cat[1] for cat in categories])
        self.category_menu.pack(pady=5)

        self.add_product_button = ctk.CTkButton(self.add_product_window, text="Adicionar", command=self.add_product)
        self.add_product_button.pack(pady=20)

    def add_product(self):
        product_id = self.product_id_entry.get()
        name = self.product_name_entry.get()
        brand = self.brand_entry.get()
        price = float(self.price_entry.get())
        supplier_price = float(self.supplier_price_entry.get())
        quantity = int(self.quantity_entry.get())
        supplier_contact = self.supplier_contact_entry.get()
        category_name = self.category_var.get()

        self.cursor.execute("SELECT id FROM categories WHERE name=?", (category_name,))
        category_id = self.cursor.fetchone()[0]

        self.cursor.execute(
            "INSERT INTO products (product_id, name, brand, price, supplier_price, quantity, supplier_contact, category_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (product_id, name, brand, price, supplier_price, quantity, supplier_contact, category_id))
        self.conn.commit()
        self.add_product_window.destroy()
        self.display_products(category_id)

    def display_products(self, category_id):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        self.cursor.execute("SELECT * FROM products WHERE category_id=?", (category_id,))
        products = self.cursor.fetchall()

        back_button = ctk.CTkButton(self.scrollable_frame, text="Voltar", command=self.display_categories)
        back_button.pack(pady=5, anchor="w")

        for product in products:
            product_frame = ctk.CTkFrame(self.scrollable_frame)
            product_frame.pack(pady=5, fill="x", expand=True)

            product_info = f"ID: {product[1]}, Nome: {product[2]}, Marca: {product[3]}, Preço: R${product[4]:.2f}, Quantidade: {product[6]}"
            product_label = ctk.CTkLabel(product_frame, text=product_info)
            product_label.pack(pady=5, anchor="w")

            button_frame = ctk.CTkFrame(product_frame)
            button_frame.pack(pady=5, anchor="w")

            delete_button = ctk.CTkButton(button_frame, text="Excluir",
                                          command=lambda product_id=product[0]: self.delete_product(product_id))
            delete_button.pack(side='left', padx=5, pady=2)

            edit_button = ctk.CTkButton(button_frame, text="Alterar Informações",
                                        command=lambda product_id=product[0]: self.show_edit_product_form(product_id))
            edit_button.pack(side='left', padx=5, pady=2)

            contact_button = ctk.CTkButton(button_frame, text="Copiar Contato",
                                           command=lambda contact=product[7]: self.copy_to_clipboard(contact))
            contact_button.pack(side='left', padx=5, pady=2)

    def delete_product(self, product_id):
        self.cursor.execute("DELETE FROM products WHERE id=?", (product_id,))
        self.conn.commit()
        self.display_categories()

    def delete_category(self, category_id):
        # Confirm deletion
        if not messagebox.askyesno("Confirmar Exclusão", "Você tem certeza que deseja excluir esta categoria e todos os produtos atrelados?"):
            return

        # Delete products within the category
        self.cursor.execute("DELETE FROM products WHERE category_id=?", (category_id,))
        self.conn.commit()

        # Delete the category
        self.cursor.execute("DELETE FROM categories WHERE id=?", (category_id,))
        self.conn.commit()

        self.display_categories()

    def show_edit_product_form(self, product_id):
        self.cursor.execute("SELECT * FROM products WHERE id=?", (product_id,))
        product = self.cursor.fetchone()

        self.edit_product_window = ctk.CTkToplevel(self)
        self.edit_product_window.attributes('-topmost', True)
        self.edit_product_window.title("Biss Manager - Alterar Informações do Produto")
        self.edit_product_window.geometry("1000x800")
        self.edit_product_window.iconbitmap("finalizado.ico") #icone funcionando

        self.product_id_label = ctk.CTkLabel(self.edit_product_window, text="ID do Produto:")
        self.product_id_label.pack(pady=5)
        self.product_id_entry = ctk.CTkEntry(self.edit_product_window)
        self.product_id_entry.insert(0, product[1])
        self.product_id_entry.pack(pady=5)

        self.product_name_label = ctk.CTkLabel(self.edit_product_window, text="Nome do Produto:")
        self.product_name_label.pack(pady=5)
        self.product_name_entry = ctk.CTkEntry(self.edit_product_window)
        self.product_name_entry.insert(0, product[2])
        self.product_name_entry.pack(pady=5)

        self.brand_label = ctk.CTkLabel(self.edit_product_window, text="Marca:")
        self.brand_label.pack(pady=5)
        self.brand_entry = ctk.CTkEntry(self.edit_product_window)
        self.brand_entry.insert(0, product[3])
        self.brand_entry.pack(pady=5)

        self.supplier_price_label = ctk.CTkLabel(self.edit_product_window, text="Preço do Fornecedor:")
        self.supplier_price_label.pack(pady=5)
        self.supplier_price_entry = ctk.CTkEntry(self.edit_product_window)
        self.supplier_price_entry.insert(0, product[5])
        self.supplier_price_entry.pack(pady=5)

        self.price_label = ctk.CTkLabel(self.edit_product_window, text="Preço:")
        self.price_label.pack(pady=5)
        self.price_entry = ctk.CTkEntry(self.edit_product_window)
        self.price_entry.insert(0, product[4])
        self.price_entry.pack(pady=5)

        margin = ((product[4] - product[5]) / product[5]) * 100 if product[5] != 0 else 0
        profit = product[4] - product[5]
        self.margin_label = ctk.CTkLabel(self.edit_product_window, text=f"Margem de Lucro: {margin:.2f}%")
        self.margin_label.pack(pady=5)

        self.profit_label = ctk.CTkLabel(self.edit_product_window, text=f"Lucro: R${profit:.2f}")
        self.profit_label.pack(pady=5)

        self.quantity_label = ctk.CTkLabel(self.edit_product_window, text="Quantidade em Estoque:")
        self.quantity_label.pack(pady=5)
        self.quantity_entry = ctk.CTkEntry(self.edit_product_window)
        self.quantity_entry.insert(0, product[6])
        self.quantity_entry.pack(pady=5)

        self.supplier_contact_label = ctk.CTkLabel(self.edit_product_window, text="Contato do Fornecedor (Telefone):")
        self.supplier_contact_label.pack(pady=5)
        self.supplier_contact_entry = ctk.CTkEntry(self.edit_product_window)
        self.supplier_contact_entry.insert(0, product[7])
        self.supplier_contact_entry.pack(pady=5)

        self.edit_product_button = ctk.CTkButton(self.edit_product_window, text="Salvar",
                                                 command=lambda: self.edit_product(product[0]))
        self.edit_product_button.pack(pady=20)

    def edit_product(self, product_id):
        new_product_id = self.product_id_entry.get()
        new_name = self.product_name_entry.get()
        new_brand = self.brand_entry.get()
        new_price = float(self.price_entry.get())
        new_supplier_price = float(self.supplier_price_entry.get())
        new_quantity = int(self.quantity_entry.get())
        new_supplier_contact = self.supplier_contact_entry.get()

        self.cursor.execute("""
            UPDATE products
            SET product_id = ?, name = ?, brand = ?, price = ?, supplier_price = ?, quantity = ?, supplier_contact = ?
            WHERE id = ?
        """, (new_product_id, new_name, new_brand, new_price, new_supplier_price, new_quantity, new_supplier_contact, product_id))
        self.conn.commit()
        self.edit_product_window.destroy()
        self.display_products(None)

    def copy_to_clipboard(self, contact):
        pyperclip.copy(contact)
        messagebox.showinfo("Contato Copiado", f"O contato {contact} foi copiado para a área de transferência.")

if __name__ == "__main__":
    app = InventoryApp()
    app.mainloop()
