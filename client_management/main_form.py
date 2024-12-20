import tkinter as tk
from tkinter import ttk, messagebox
from client_management.classes import Operator
from client_management.client_form import ClientForm


class MainForm(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Управление клиентами")
        self.geometry("800x600")
        self.operator = Operator()
        self.create_widgets()

    def create_widgets(self):
        # Кнопки управления
        button_frame = tk.Frame(self)
        button_frame.pack(fill=tk.X, side=tk.TOP)

        tk.Button(button_frame, text="Добавить клиента", command=self.add_client).pack(side=tk.LEFT)
        tk.Button(button_frame, text="Редактировать клиента", command=self.edit_client).pack(side=tk.LEFT)
        tk.Button(button_frame, text="Удалить клиента", command=self.delete_client).pack(side=tk.LEFT)
        tk.Button(button_frame, text="Сохранить данные", command=self.save_to_file).pack(side=tk.LEFT)
        tk.Button(button_frame, text="Загрузить данные", command=self.load_from_file).pack(side=tk.LEFT)

        # Таблица TreeView
        columns = ("Name", "Age", "Discount", "ServicesCost", "FinalCost")
        self.client_table = ttk.Treeview(self, columns=columns, show="headings", height=20)

        # Заголовки столбцов
        for col in columns:
            self.client_table.heading(col, text=col, command=lambda c=col: self.sort_table(c))
            self.client_table.column(col, width=150)

        self.client_table.pack(fill=tk.BOTH, expand=True)

    def refresh_table(self):
        """Обновляет таблицу, отображая текущих клиентов."""
        for row in self.client_table.get_children():
            self.client_table.delete(row)

        for client in self.operator.clients:
            self.client_table.insert(
                "", "end",
                values=(
                    client.name,
                    client.age,
                    client.discount,
                    client.services_cost,
                    client.get_final_cost()
                ),
            )

    def add_client(self):
        form = ClientForm(self, mode="add")
        self.wait_window(form)

        if form.client:
            self.operator.add_client(form.client)
            self.refresh_table()

    def edit_client(self):
        selected_item = self.client_table.selection()
        if not selected_item:
            messagebox.showerror("Ошибка", "Выберите клиента для редактирования.")
            return

        client_index = self.client_table.index(selected_item[0])
        client = self.operator.clients[client_index]

        form = ClientForm(self, client=client, mode="edit")
        self.wait_window(form)

        if form.client:
            self.operator.clients[client_index] = form.client
            self.refresh_table()

    def delete_client(self):
        selected_item = self.client_table.selection()
        if not selected_item:
            messagebox.showerror("Ошибка", "Выберите клиента для удаления.")
            return

        client_index = self.client_table.index(selected_item[0])
        del self.operator.clients[client_index]
        self.operator.save_to_database()
        self.refresh_table()

    def save_to_file(self):
        try:
            self.operator.save_to_database()
            messagebox.showinfo("Сохранение", "Данные успешно сохранены в базу данных.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить данные: {e}")

    def load_from_file(self):
        try:
            self.operator.load_from_database()
            self.refresh_table()
            messagebox.showinfo("Загрузка", "Данные успешно загружены из базы данных.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить данные: {e}")

    def sort_table(self, col):
        """Сортирует таблицу по указанной колонке."""
        reverse = getattr(self, "_reverse_sort", {}).get(col, False)

        # Определяем ключ сортировки
        if col == "FinalCost":
            key_func = lambda client: client.get_final_cost()
        elif col == "ServicesCost":
            key_func = lambda client: client.services_cost
        elif col == "Age":
            key_func = lambda client: client.age
        elif col == "Discount":
            key_func = lambda client: client.discount
        else:
            return  # Никакой сортировки для поля "Name"

        # Сортируем клиентов
        self.operator.clients.sort(
            key=lambda client: key_func(client),
            reverse=reverse
        )

        # Переключение направления сортировки
        if not hasattr(self, "_reverse_sort"):
            self._reverse_sort = {}
        self._reverse_sort[col] = not reverse

        # Обновление таблицы
        self.refresh_table()
