import pickle
import os

class PickleStorage:
    def __init__(self, filename: str = "employees.pkl"):
        self.filename = filename

    def save(self, employees: list):
        """Сохраняет список сотрудников в файл pickle."""
        if not employees:
            print("Нет данных для сохранения.")
            return

        try:
            with open(self.filename, "wb") as f:
                pickle.dump(employees, f)
            print(f"Список сотрудников успешно сохранён в '{self.filename}'")
        except Exception as e:
            print(f"Ошибка при сохранении: {e}")

    def load(self):
        """Загружает сотрудников из файла pickle."""
        if not os.path.isfile(self.filename):
            print("Файл с данными не найден.")
            return []

        try:
            with open(self.filename, "rb") as f:

                employees = pickle.load(f)
        except Exception as e:
            print(f"Ошибка при чтении файла: {e}")
            return []

        print(f"Загружено {len(employees)} сотрудников из '{self.filename}'")
        return employees