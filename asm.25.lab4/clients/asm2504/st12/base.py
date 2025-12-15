class BasePerson:
    io = None

    def __init__(self):
        self.name = ""
        self.age = 0

    def input_fields(self):
        if self.io is None:
            print("Ошибка: не установлена стратегия ввода-вывода")
            return
        self.io.input_field(self, "name", str)
        self.io.input_field(self, "age", int)

    def print_fields(self):
        if self.io is None:
            print("Ошибка: не установлена стратегия ввода-вывода")
            return
        self.io.print_field(self, "name")
        self.io.print_field(self, "age")

    def edit_single_field(self):
        print("Доступные поля для редактирования:")
        print("1. name")
        print("2. age")
        try:
            choice = int(input("Выберите номер поля: "))
            if choice == 1:
                self.io.input_field(self, "name", str)
            elif choice == 2:
                self.io.input_field(self, "age", int)
            else:
                print("Неверный выбор")
        except Exception:
            print("Ошибка ввода")

    def validate(self, field_name, value):
        return value

