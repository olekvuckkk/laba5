from client_management.main_form import MainForm

if __name__ == "__main__":
    app = MainForm()
    app.operator.load_from_database()  # Загружаем данные из базы перед запуском интерфейса
    app.mainloop()
    app.operator.save_to_database()  # Сохраняем данные перед закрытием приложения
