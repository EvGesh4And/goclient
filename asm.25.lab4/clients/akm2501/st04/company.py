from .employee import Employee
from .manager import Manager
from .director import Director
from .storage_strategy import RestStorage

class Company:
    def __init__(self):
        self.storage = RestStorage()

    def print_list(self):
        try:
            employees = self.storage.get_all()
            if not employees:
                print("Список пуст")
                return
            for e in employees:
                print(f"{e['id']} | {e['type']:8} | {e.get('name', '—'):20} | Возраст: {e.get('age', '?')}")
                if e['type'] == 'Manager':
                    print(f"   Департамент: {e.get('department', '—')}")
                if e['type'] == 'Director':
                    print(f"   Титул: {e.get('title', '—')}")
                print("—")
        except Exception as e:
            print(f"Ошибка получения данных: {e}")

    def add_employee(self):
        print("1. Сотрудник  2. Менеджер  3. Директор")
        choice = input("Выбор: ").strip()
        classes = {"1": Employee, "2": Manager, "3": Director}
        cls = classes.get(choice)
        if not cls:
            print("Неверный выбор")
            return
        emp = cls()
        print("Введите данные:")
        emp.input_data()
        try:
            self.storage.add(emp)
            print("Добавлено!")
        except Exception as e:
            print(f"Ошибка добавления: {e}")

    def clear_list(self):
        if input("Очистить весь список? (y/n): ").lower() == 'y':
            try:
                self.storage.clear()
                print("Список очищен")
            except Exception as e:
                print(f"Ошибка: {e}")

    def run(self):
        print("Консольный клиент → REST API (st04)")
        while True:
            print("\n" + "="*50)
            print("1. Показать список")
            print("2. Добавить сотрудника")
            print("3. Очистить список")
            print("4. Выход")
            ch = input("→ ").strip()
            if ch == "1": self.print_list()
            elif ch == "2": self.add_employee()
            elif ch == "3": self.clear_list()
            elif ch == "4": break
            else: print("Неверная команда")