import customtkinter as ctk

# Configuração inicial
ctk.set_appearance_mode("system")  # Modos: "dark", "light", "system"
ctk.set_default_color_theme("green")  # Temas: "blue", "green", "dark-blue"

# Função de exemplo para os botões
def on_click_Voltar(button_number):
    print(f"Botão {button_number} clicado!")

# Criação da janela principal
root = ctk.CTk()
root.title("Biss Maneger - Início")
root.geometry("800x500")

# Frame no topo da janela para alinhar os botões
top_frame = ctk.CTkFrame(root)
top_frame.pack(side="top", fill="x", pady=10)

# Criação dos botões

button_voltar = ctk.CTkButton(top_frame, text="Voltar ao Início", command=lambda: on_button_click(1))
button_voltar.pack(side="right", padx=30)

#

# Loop principal da aplicação
root.mainloop()
