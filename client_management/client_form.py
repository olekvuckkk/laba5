import tkinter as tk
from tkinter import messagebox
from client_management.classes import Client


class ClientForm(tk.Toplevel):
    def __init__(self, master, client=None, mode="add"):
        super().__init__(master)
        self.title("Редактирование клиента" if mode == "edit" else "Добавление клиента")
        self.geometry("300x200")
        self.client = None
        self.mode = mode
        self.create_widgets()

        if client:
            self.name_var.set(client.name)
            self.age_var.set(client.age)
            self.discount_var.set(client.discount)
            self.services_cost_var.set(client.services_cost)

    def create_widgets(self):
        self.name_var = tk.StringVar()
        self.age_var = tk.StringVar()
        self.discount_var = tk.StringVar()
        self.services_cost_var = tk.StringVar()

        tk.Label(self, text="Имя:").grid(row=0, column=0, sticky="w")
        tk.Entry(self, textvariable=self.name_var, state="normal" if self.mode == "add" else "disabled").grid(row=0, column=1)

        tk.Label(self, text="Возраст:").grid(row=1, column=0, sticky="w")
        tk.Entry(self, textvariable=self.age_var).grid(row=1, column=1)

        tk.Label(self, text="Скидка (%):").grid(row=2, column=0, sticky="w")
        tk.Entry(self, textvariable=self.discount_var).grid(row=2, column=1)

        tk.Label(self, text="Стоимость услуг:").grid(row=3, column=0, sticky="w")
        tk.Entry(self, textvariable=self.services_cost_var).grid(row=3, column=1)

        tk.Button(self, text="Сохранить", command=self.save_client).grid(row=4, column=0, columnspan=2)

    def save_client(self):
        try:
            name = self.name_var.get().strip()
            age = int(self.age_var.get())
            discount = float(self.discount_var.get())
            services_cost = float(self.services_cost_var.get())
            self.client = Client(name, age, discount)
            self.client.services_cost = services_cost
            self.destroy()
        except ValueError:
            messagebox.showerror("Ошибка", "Некорректные данные. Проверьте ввод.")
