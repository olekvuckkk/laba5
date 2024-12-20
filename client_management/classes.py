import json
import sqlite3


class Client:
    def __init__(self, name, age, discount=0):
        self.name = name
        self.age = age
        self.discount = discount
        self.services_cost = 0.0

    def get_final_cost(self):
        return self.services_cost * (1 - self.discount / 100)


class Operator:
    def __init__(self, db_name="clients.db"):
        self.clients = []
        self.db_name = db_name
        self._initialize_database()

    def _initialize_database(self):
        """Инициализация таблицы в базе данных."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS clients (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    age INTEGER NOT NULL,
                    discount REAL NOT NULL,
                    services_cost REAL NOT NULL
                )
            ''')
            conn.commit()

    def load_from_database(self):
        """Загружает данные клиентов из базы данных."""
        self.clients = []
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name, age, discount, services_cost FROM clients")
            for row in cursor.fetchall():
                client = Client(row[0], row[1], row[2])
                client.services_cost = row[3]
                self.clients.append(client)

    def save_to_database(self):
        """Сохраняет данные клиентов в базу данных."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM clients")  # Удаляем старые записи
            for client in self.clients:
                cursor.execute('''
                    INSERT INTO clients (name, age, discount, services_cost)
                    VALUES (?, ?, ?, ?)
                ''', (client.name, client.age, client.discount, client.services_cost))
            conn.commit()

    def add_client(self, client):
        self.clients.append(client)
        self.save_to_database()

    def remove_client(self, client):
        self.clients.remove(client)
        self.save_to_database()
