if __name__ != '__main__':
    from .entity import Employee, Worker, Manager, Director
    from .console_io import ConsoleIO
    from .pickle_storage import PickleStorage
    from .rest_storage import RestStorage
else:
    from entity import Employee, Worker, Manager, Director
    from console_io import ConsoleIO
    from pickle_storage import PickleStorage
    from rest_storage import RestStorage


class Company:
    def __init__(self, storage=None, io_strategy=None):
        # storage может быть PickleStorage или RestStorage
        self.storage = storage or PickleStorage()
        self.io = io_strategy or ConsoleIO()
        self.employees = []

        # Загрузка данных, если хранилище поддерживает load()
        if hasattr(self.storage, "load"):
            try:
                data = self.storage.load()
                self._load_from_storage(data)
            except Exception:
                pass

    # --- Преобразование словарей REST → объекты ---
    def _load_from_storage(self, data):
        """Перевод полученных словарей из REST в объекты."""
        if not data:
            self.employees = []
            return

        if isinstance(data[0], dict):  # это REST-ответ
            self.employees = []
            for d in data:
                emp_type = d.get("type", "Worker")
                cls_map = {
                    "Worker": Worker,
                    "Manager": Manager,
                    "Director": Director
                }
                cls = cls_map.get(emp_type, Worker)
                obj = cls.from_dict(d)
                self.employees.append(obj)
        else:
            # PickleStorage — сразу список объектов
            self.employees = data

    # --- Добавление ---
    def add_employee(self):
        print("Выберите тип сотрудника:")
        print("1 - Рабочий")
        print("2 - Менеджер")
        print("3 - Директор")
        choice = input("Ваш выбор: ")

        cls_map = {"1": Worker, "2": Manager, "3": Director}
        cls = cls_map.get(choice)

        if not cls:
            print("Неверный выбор.")
            return

        emp = cls(io_strategy=self.io)
        emp.input_fields()
        self.employees.append(emp)

        # REST
        if hasattr(self.storage, "add"):
            r = self.storage.add(emp.to_dict())
            # сохранить id, если REST вернул db_id
            if "id" in r:
                emp.db_id = r["id"]

        print("Карточка сотрудника добавлена.")

    # --- Вывод списка ---
    def display_list(self):
        self.io.display_list(self.employees)

    # --- Загрузка ---
    def load_from_file(self):
        data = self.storage.load()
        self._load_from_storage(data)
        print("Данные загружены.")

    # --- Сохранение ---
    def save_to_file(self):
        if hasattr(self.storage, "save"):
            self.storage.save(self.employees)
            print("Данные сохранены.")
        else:
            print("Это хранилище не поддерживает прямое сохранение.")

    # --- Очистка ---
    def clear_list(self):
        self.employees = []
        if hasattr(self.storage, "clear"):
            self.storage.clear()
        print("Список сотрудников очищен.")

    # --- Редактирование ---
    def edit_employee(self, index):
        if not (0 <= index < len(self.employees)):
            print("Неверный индекс.")
            return

        emp = self.employees[index]
        emp.input_fields()  # перезапись полей

        # REST
        if hasattr(self.storage, "update"):
            emp_id = getattr(emp, "db_id", index + 1)
            self.storage.update(emp_id, emp.to_dict())

        print("Карточка обновлена.")

    # --- Удаление ---
    def delete_employee(self, index):
        if not (0 <= index < len(self.employees)):
            print("Неверный индекс.")
            return

        emp = self.employees[index]
        emp_id = getattr(emp, "db_id", index + 1)

        # REST
        if hasattr(self.storage, "delete"):
            self.storage.delete(emp_id)

        del self.employees[index]
        print("Карточка сотрудника удалена.")
