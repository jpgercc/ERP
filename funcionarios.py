import customtkinter as ctk
import sqlite3
from tkinter import messagebox
import pyperclip
import subprocess
import sys

class EmployeeApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("system")  # Modos: "dark", "light", "system"
        ctk.set_default_color_theme("green")  # Temas: "blue", "green", "dark-blue"

        self.title("Biss Manager - Funcionários")
        self.geometry("1000x500")
        self.iconbitmap('finalizado.ico')

        # Connect to the database
        self.conn = sqlite3.connect("employees.db")
        self.cursor = self.conn.cursor()
        self.create_table()

        #BUTTON MAIN
#        self.main = ctk.CTkButton(self, text="Voltar ao Início", command=self.button_main)
#        self.main.pack(side="right", pady=10)

        # Create the add employee button
        self.add_employee_button = ctk.CTkButton(self, text="Adicionar Funcionário", command=self.show_add_employee_form)
        self.add_employee_button.pack(pady=10)

        # Create a scrollable frame for employee listing
        self.scrollable_frame = ctk.CTkScrollableFrame(self)
        self.scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Display all employees initially
        self.display_employees()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY,
                name TEXT,
                cpf TEXT,
                rg TEXT,
                address TEXT,
                start_date TEXT,
                cash_allowance REAL,
                transport_allowance REAL,
                food_allowance REAL,
                salary REAL,
                job_role TEXT,
                work_days_week TEXT,
                vacation_start_date TEXT,
                vacation_end_date TEXT,
                working_hours REAL,
                overtime_hours REAL
            )
        """)
        self.conn.commit()


#    def button_main(self):
#        root = self.winfo_toplevel()
#        subprocess.Popen([sys.executable, "main.py"])
#        root.destroy()

    def show_add_employee_form(self):
        self.add_employee_window = ctk.CTkToplevel(self)
        self.add_employee_window.attributes('-topmost', True)
        self.add_employee_window.title("Biss Manager - Adicionar Funcionário")
        self.add_employee_window.geometry("1000x500")
        #self.add_employee_window.iconbitmap('beaver.ico')


        # Create a scrollable frame inside the add employee window
        self.add_employee_scrollable_frame = ctk.CTkScrollableFrame(self.add_employee_window)
        self.add_employee_scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Employee Name
        self.name_label = ctk.CTkLabel(self.add_employee_scrollable_frame, text="Nome:")
        self.name_label.pack(pady=5)
        self.name_entry = ctk.CTkEntry(self.add_employee_scrollable_frame)
        self.name_entry.pack(pady=5)

        # CPF
        self.cpf_label = ctk.CTkLabel(self.add_employee_scrollable_frame, text="CPF:")
        self.cpf_label.pack(pady=5)
        self.cpf_entry = ctk.CTkEntry(self.add_employee_scrollable_frame)
        self.cpf_entry.pack(pady=5)

        # RG
        self.rg_label = ctk.CTkLabel(self.add_employee_scrollable_frame, text="RG:")
        self.rg_label.pack(pady=5)
        self.rg_entry = ctk.CTkEntry(self.add_employee_scrollable_frame)
        self.rg_entry.pack(pady=5)

        # Address
        self.address_label = ctk.CTkLabel(self.add_employee_scrollable_frame, text="Endereço:")
        self.address_label.pack(pady=5)
        self.address_entry = ctk.CTkEntry(self.add_employee_scrollable_frame)
        self.address_entry.pack(pady=5)

        # Start Date
        self.start_date_label = ctk.CTkLabel(self.add_employee_scrollable_frame, text="Data de Início:")
        self.start_date_label.pack(pady=5)
        self.start_date_entry = ctk.CTkEntry(self.add_employee_scrollable_frame)
        self.start_date_entry.pack(pady=5)

        # Cash Allowance
        self.cash_allowance_label = ctk.CTkLabel(self.add_employee_scrollable_frame, text="Vale em Dinheiro:")
        self.cash_allowance_label.pack(pady=5)
        self.cash_allowance_entry = ctk.CTkEntry(self.add_employee_scrollable_frame)
        self.cash_allowance_entry.pack(pady=5)

        # Transport Allowance
        self.transport_allowance_label = ctk.CTkLabel(self.add_employee_scrollable_frame, text="Vale Transporte:")
        self.transport_allowance_label.pack(pady=5)
        self.transport_allowance_entry = ctk.CTkEntry(self.add_employee_scrollable_frame)
        self.transport_allowance_entry.pack(pady=5)

        # Food Allowance
        self.food_allowance_label = ctk.CTkLabel(self.add_employee_scrollable_frame, text="Vale Alimentação:")
        self.food_allowance_label.pack(pady=5)
        self.food_allowance_entry = ctk.CTkEntry(self.add_employee_scrollable_frame)
        self.food_allowance_entry.pack(pady=5)

        # Salary
        self.salary_label = ctk.CTkLabel(self.add_employee_scrollable_frame, text="Salário:")
        self.salary_label.pack(pady=5)
        self.salary_entry = ctk.CTkEntry(self.add_employee_scrollable_frame)
        self.salary_entry.pack(pady=5)

        # Job Role
        self.job_role_label = ctk.CTkLabel(self.add_employee_scrollable_frame, text="Função:")
        self.job_role_label.pack(pady=5)
        self.job_role_entry = ctk.CTkEntry(self.add_employee_scrollable_frame)
        self.job_role_entry.pack(pady=5)

        # Work Days per Week
        self.work_days_week_label = ctk.CTkLabel(self.add_employee_scrollable_frame, text="Dias de Serviço por Semana:")
        self.work_days_week_label.pack(pady=5)
        self.work_days_week_entry = ctk.CTkEntry(self.add_employee_scrollable_frame)
        self.work_days_week_entry.pack(pady=5)

        # Vacation Start Date
        self.vacation_start_date_label = ctk.CTkLabel(self.add_employee_scrollable_frame, text="Início das Férias:")
        self.vacation_start_date_label.pack(pady=5)
        self.vacation_start_date_entry = ctk.CTkEntry(self.add_employee_scrollable_frame)
        self.vacation_start_date_entry.pack(pady=5)

        # Vacation End Date
        self.vacation_end_date_label = ctk.CTkLabel(self.add_employee_scrollable_frame, text="Fim das Férias:")
        self.vacation_end_date_label.pack(pady=5)
        self.vacation_end_date_entry = ctk.CTkEntry(self.add_employee_scrollable_frame)
        self.vacation_end_date_entry.pack(pady=5)

        # Working Hours
        self.working_hours_label = ctk.CTkLabel(self.add_employee_scrollable_frame, text="Carga Horária:")
        self.working_hours_label.pack(pady=5)
        self.working_hours_entry = ctk.CTkEntry(self.add_employee_scrollable_frame)
        self.working_hours_entry.pack(pady=5)

        # Overtime Hours
        self.overtime_hours_label = ctk.CTkLabel(self.add_employee_scrollable_frame, text="Horas Extras:")
        self.overtime_hours_label.pack(pady=5)
        self.overtime_hours_entry = ctk.CTkEntry(self.add_employee_scrollable_frame)
        self.overtime_hours_entry.pack(pady=5)

        # Add Employee Button
        self.add_employee_button = ctk.CTkButton(self.add_employee_scrollable_frame, text="Adicionar", command=self.add_employee)
        self.add_employee_button.pack(pady=20)

    def show_edit_employee_form(self, employee):
        self.edit_employee_window = ctk.CTkToplevel(self)
        self.edit_employee_window.attributes('-topmost', True)
        self.edit_employee_window.title("Alterar Funcionário")
        self.edit_employee_window.geometry("1000x800")
        self.edit_employee_window.iconbitmap('beaver.ico')

        # Create a scrollable frame inside the edit employee window
        self.edit_employee_scrollable_frame = ctk.CTkScrollableFrame(self.edit_employee_window)
        self.edit_employee_scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Employee Name
        self.name_label = ctk.CTkLabel(self.edit_employee_scrollable_frame, text="Nome:")
        self.name_label.pack(pady=5)
        self.name_entry = ctk.CTkEntry(self.edit_employee_scrollable_frame)
        self.name_entry.insert(0, employee[1])
        self.name_entry.pack(pady=5)

        # CPF
        self.cpf_label = ctk.CTkLabel(self.edit_employee_scrollable_frame, text="CPF:")
        self.cpf_label.pack(pady=5)
        self.cpf_entry = ctk.CTkEntry(self.edit_employee_scrollable_frame)
        self.cpf_entry.insert(0, employee[2])
        self.cpf_entry.pack(pady=5)

        # RG
        self.rg_label = ctk.CTkLabel(self.edit_employee_scrollable_frame, text="RG:")
        self.rg_label.pack(pady=5)
        self.rg_entry = ctk.CTkEntry(self.edit_employee_scrollable_frame)
        self.rg_entry.insert(0, employee[3])
        self.rg_entry.pack(pady=5)

        # Address
        self.address_label = ctk.CTkLabel(self.edit_employee_scrollable_frame, text="Endereço:")
        self.address_label.pack(pady=5)
        self.address_entry = ctk.CTkEntry(self.edit_employee_scrollable_frame)
        self.address_entry.insert(0, employee[4])
        self.address_entry.pack(pady=5)

        # Start Date
        self.start_date_label = ctk.CTkLabel(self.edit_employee_scrollable_frame, text="Data de Início:")
        self.start_date_label.pack(pady=5)
        self.start_date_entry = ctk.CTkEntry(self.edit_employee_scrollable_frame)
        self.start_date_entry.insert(0, employee[5])
        self.start_date_entry.pack(pady=5)

        # Cash Allowance
        self.cash_allowance_label = ctk.CTkLabel(self.edit_employee_scrollable_frame, text="Vale em Dinheiro:")
        self.cash_allowance_label.pack(pady=5)
        self.cash_allowance_entry = ctk.CTkEntry(self.edit_employee_scrollable_frame)
        self.cash_allowance_entry.insert(0, employee[6])
        self.cash_allowance_entry.pack(pady=5)

        # Transport Allowance
        self.transport_allowance_label = ctk.CTkLabel(self.edit_employee_scrollable_frame, text="Vale Transporte:")
        self.transport_allowance_label.pack(pady=5)
        self.transport_allowance_entry = ctk.CTkEntry(self.edit_employee_scrollable_frame)
        self.transport_allowance_entry.insert(0, employee[7])
        self.transport_allowance_entry.pack(pady=5)

        # Food Allowance
        self.food_allowance_label = ctk.CTkLabel(self.edit_employee_scrollable_frame, text="Vale Alimentação:")
        self.food_allowance_label.pack(pady=5)
        self.food_allowance_entry = ctk.CTkEntry(self.edit_employee_scrollable_frame)
        self.food_allowance_entry.insert(0, employee[8])
        self.food_allowance_entry.pack(pady=5)

        # Salary
        self.salary_label = ctk.CTkLabel(self.edit_employee_scrollable_frame, text="Salário:")
        self.salary_label.pack(pady=5)
        self.salary_entry = ctk.CTkEntry(self.edit_employee_scrollable_frame)
        self.salary_entry.insert(0, employee[9])
        self.salary_entry.pack(pady=5)

        # Job Role
        self.job_role_label = ctk.CTkLabel(self.edit_employee_scrollable_frame, text="Função:")
        self.job_role_label.pack(pady=5)
        self.job_role_entry = ctk.CTkEntry(self.edit_employee_scrollable_frame)
        self.job_role_entry.insert(0, employee[10])
        self.job_role_entry.pack(pady=5)

        # Work Days per Week
        self.work_days_week_label = ctk.CTkLabel(self.edit_employee_scrollable_frame, text="Dias de Serviço por Semana:")
        self.work_days_week_label.pack(pady=5)
        self.work_days_week_entry = ctk.CTkEntry(self.edit_employee_scrollable_frame)
        self.work_days_week_entry.insert(0, employee[11])
        self.work_days_week_entry.pack(pady=5)

        # Vacation Start Date
        self.vacation_start_date_label = ctk.CTkLabel(self.edit_employee_scrollable_frame, text="Início das Férias:")
        self.vacation_start_date_label.pack(pady=5)
        self.vacation_start_date_entry = ctk.CTkEntry(self.edit_employee_scrollable_frame)
        self.vacation_start_date_entry.insert(0, employee[12])
        self.vacation_start_date_entry.pack(pady=5)

        # Vacation End Date
        self.vacation_end_date_label = ctk.CTkLabel(self.edit_employee_scrollable_frame, text="Fim das Férias:")
        self.vacation_end_date_label.pack(pady=5)
        self.vacation_end_date_entry = ctk.CTkEntry(self.edit_employee_scrollable_frame)
        self.vacation_end_date_entry.insert(0, employee[13])
        self.vacation_end_date_entry.pack(pady=5)

        # Working Hours
        self.working_hours_label = ctk.CTkLabel(self.edit_employee_scrollable_frame, text="Carga Horária:")
        self.working_hours_label.pack(pady=5)
        self.working_hours_entry = ctk.CTkEntry(self.edit_employee_scrollable_frame)
        self.working_hours_entry.insert(0, employee[14])
        self.working_hours_entry.pack(pady=5)

        # Overtime Hours
        self.overtime_hours_label = ctk.CTkLabel(self.edit_employee_scrollable_frame, text="Horas Extras:")
        self.overtime_hours_label.pack(pady=5)
        self.overtime_hours_entry = ctk.CTkEntry(self.edit_employee_scrollable_frame)
        self.overtime_hours_entry.insert(0, employee[15])
        self.overtime_hours_entry.pack(pady=5)

        # Edit Employee Button
        self.edit_employee_button = ctk.CTkButton(self.edit_employee_scrollable_frame, text="Salvar",
                                                 command=lambda: self.edit_employee(employee[0]))
        self.edit_employee_button.pack(pady=20)

    def add_employee(self):
        name = self.name_entry.get()
        cpf = self.cpf_entry.get()
        rg = self.rg_entry.get()
        address = self.address_entry.get()
        start_date = self.start_date_entry.get()
        cash_allowance = float(self.cash_allowance_entry.get())
        transport_allowance = float(self.transport_allowance_entry.get())
        food_allowance = float(self.food_allowance_entry.get())
        salary = float(self.salary_entry.get())
        job_role = self.job_role_entry.get()
        work_days_week = self.work_days_week_entry.get()
        vacation_start_date = self.vacation_start_date_entry.get()
        vacation_end_date = self.vacation_end_date_entry.get()
        working_hours = float(self.working_hours_entry.get())
        overtime_hours = float(self.overtime_hours_entry.get())

        self.cursor.execute("""
            INSERT INTO employees (name, cpf, rg, address, start_date, cash_allowance, transport_allowance, food_allowance, salary, job_role, work_days_week, vacation_start_date, vacation_end_date, working_hours, overtime_hours)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (name, cpf, rg, address, start_date, cash_allowance, transport_allowance, food_allowance, salary, job_role, work_days_week, vacation_start_date, vacation_end_date, working_hours, overtime_hours))
        self.conn.commit()
        self.add_employee_window.destroy()
        self.display_employees()

    def edit_employee(self, employee_id):
        new_name = self.name_entry.get()
        new_cpf = self.cpf_entry.get()
        new_rg = self.rg_entry.get()
        new_address = self.address_entry.get()
        new_start_date = self.start_date_entry.get()
        new_cash_allowance = float(self.cash_allowance_entry.get())
        new_transport_allowance = float(self.transport_allowance_entry.get())
        new_food_allowance = float(self.food_allowance_entry.get())
        new_salary = float(self.salary_entry.get())
        new_job_role = self.job_role_entry.get()
        new_work_days_week = self.work_days_week_entry.get()
        new_vacation_start_date = self.vacation_start_date_entry.get()
        new_vacation_end_date = self.vacation_end_date_entry.get()
        new_working_hours = float(self.working_hours_entry.get())
        new_overtime_hours = float(self.overtime_hours_entry.get())

        self.cursor.execute("""
            UPDATE employees
            SET name = ?, cpf = ?, rg = ?, address = ?, start_date = ?, cash_allowance = ?, transport_allowance = ?, food_allowance = ?, salary = ?, job_role = ?, work_days_week = ?, vacation_start_date = ?, vacation_end_date = ?, working_hours = ?, overtime_hours = ?
            WHERE id = ?
        """, (new_name, new_cpf, new_rg, new_address, new_start_date, new_cash_allowance, new_transport_allowance, new_food_allowance, new_salary, new_job_role, new_work_days_week, new_vacation_start_date, new_vacation_end_date, new_working_hours, new_overtime_hours, employee_id))
        self.conn.commit()
        self.edit_employee_window.destroy()
        self.display_employees()

    def display_employees(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        self.cursor.execute("SELECT * FROM employees")
        employees = self.cursor.fetchall()

        for employee in employees:
            employee_info = f"Nome: {employee[1]}, CPF: {employee[2]}, RG: {employee[3]}, Salário: R${employee[9]:.2f}, Função: {employee[10]}"
            employee_label = ctk.CTkLabel(self.scrollable_frame, text=employee_info)
            employee_label.pack(pady=5, anchor="w")

            # Delete Button
            delete_button = ctk.CTkButton(self.scrollable_frame, text="Deletar",
                                          command=lambda id=employee[0]: self.delete_employee(id))
            delete_button.pack(pady=5)

            # Edit Button
            edit_button = ctk.CTkButton(self.scrollable_frame, text="Editar",
                                        command=lambda emp=employee: self.show_edit_employee_form(emp))
            edit_button.pack(pady=5)

    def delete_employee(self, employee_id):
        response = messagebox.askyesno("Confirmação", "Tem certeza que deseja deletar este funcionário?")
        if response:
            self.cursor.execute("DELETE FROM employees WHERE id = ?", (employee_id,))
            self.conn.commit()
            self.display_employees()


if __name__ == "__main__":
    app = EmployeeApp()
    app.mainloop()
