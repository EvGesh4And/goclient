from .storage_strategy import RestStorage


class Company:
    def __init__(self):
        self.storage = RestStorage()
        self.auto_load()

    def auto_load(self):
        if (self.storage.DATA_DIR / "backup_client.pkl").exists():
            print("Автозагрузка данных из backup_client.pkl...")
            self.storage.load_from_file("backup_client.pkl")
        else:
            print("Done...")

    def print_list(self, employees=None):
        employees = employees or self.storage.get_all()
        if not employees:
            print("Список пуст.")
            return

        print("\n" + "═" * 60)
        print("                        СПИСОК СОТРУДНИКОВ")
        print("═" * 60)
        for i, e in enumerate(employees, 1):
            short_id = e['id'][:10] + "..." if len(e['id']) > 10 else e['id']
            print(f"{i:2}. {short_id} | {e['type']:8} | {e.get('name','—'):20} | Возраст: {e.get('age','?')}")
            if e['type'] == 'Manager':
                print(f"    Департамент: {e.get('department','—')}")
            if e['type'] == 'Director':
                print(f"    Должность: {e.get('title','—')}")
            print("─" * 60)

    def add_employee(self):
        from .employee import Employee
        from .manager import Manager
        from .director import Director

        print("\nТип сотрудника:")
        print("  1. Сотрудник")
        print("  2. Менеджер")
        print("  3. Директор")
        ch = input(" → Выбор (1–3): ").strip()
        cls = {"1": Employee, "2": Manager, "3": Director}.get(ch)
        if not cls:
            print("Неверно.")
            return

        emp = cls()
        print("Введите данные (Enter — пропустить):")
        emp.input_data()
        self.storage.add(emp)
        print("Добавлено!")

    def edit_employee(self):
        employees = self.storage.get_all()
        if not employees:
            print("Список пуст.")
            return

        query = input("\nИмя или часть имени (Enter — все): ").strip()
        if query:
            employees = self.storage.search_by_name(query)
            if not employees:
                print("Ничего не найдено.")
                return

        self.print_list(employees)
        try:
            num = int(input(f"\nНомер для редактирования (1–{len(employees)}): "))
            if 1 <= num <= len(employees):
                self.storage.edit_by_id(employees[num-1]["id"])
            else:
                print("Неверный номер.")
        except ValueError:
            print("Введите число.")

    def run(self):
        while True:
            print(" " + "═" * 60)
            print("                           МЕНЮ")
            print(" " + "═" * 60)
            print("  1. Список сотрудников")
            print("  2. Добавить")
            print("  3. Редактировать (по имени → номер)")
            print("  4. Сохранить")
            print("  5. Загрузить")
            print("  6. Очистить список")
            print("  0. Выход")
            print(" " + "═" * 60)

            ch = input("\n → Выбор (1–7): ").strip()

            if ch == "1": self.print_list()
            elif ch == "2": self.add_employee()
            elif ch == "3": self.edit_employee()
            elif ch == "4":
                self.storage.save_to_file("backup_client.pkl")
                print("Сохранено.")
            elif ch == "5":
                self.storage.load_from_file("backup_client.pkl")
            elif ch == "6":
                if input("Очистить всё? (y/N): ").lower() == "y":
                    self.storage.clear()
                    print("Очищено.")
            elif ch == "0":
                self.storage.save_to_file("backup_client.pkl")
                print("\nДо свидания!")
                break

            input("\nНажмите Enter...")