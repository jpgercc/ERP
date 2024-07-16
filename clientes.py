import customtkinter as ctk
import sqlite3
from tkinter import messagebox
import pyperclip
import subprocess
import sys

class Clientes(ctk.CTk):
    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("system")  # Modos: "dark", "light", "system"
        ctk.set_default_color_theme("green")  # Temas: "blue", "green", "dark-blue"

        self.title("Biss Manager - Produtos")
        self.geometry("1000x500")
        self.iconbitmap('beaver.ico')

        #BOTOES CTK
        self.main = ctk.CTkButton(self, text="Voltar ao Início", command=self.button_main)
        self.main.pack(side="right", pady=10)

#DEF BOTOES
    def button_main(self):
        root = self.winfo_toplevel()
        subprocess.Popen([sys.executable, "main.py"])
        root.destroy()

#LOOP
if __name__ == "__main__":
    app = Clientes()
    app.mainloop()