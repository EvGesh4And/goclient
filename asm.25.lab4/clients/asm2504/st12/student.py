from .base import BasePerson


class Student(BasePerson):
    FIELDS = {
        "name": str,
        "age": int,
        "group": str,
        "record_book": str,
        "avg_grade": float,
    }

    def __init__(self):
        super().__init__()
        self.group = ""
        self.record_book = ""
        self.avg_grade = 0.0

    def input_fields(self):
        super().input_fields()
        if self.io is None:
            return
        self.io.input_field(self, "group", str)
        self.io.input_field(self, "record_book", str)
        self.io.input_field(self, "avg_grade", float)

    def print_fields(self):
        super().print_fields()
        if self.io is None:
            return
        self.io.print_field(self, "group")
        self.io.print_field(self, "record_book")
        self.io.print_field(self, "avg_grade")

    def edit_single_field(self):
        print("Доступные поля для редактирования:")
        print("1. name")
        print("2. age")
        print("3. group")
        print("4. record_book")
        print("5. avg_grade")
        try:
            choice = int(input("Выберите номер поля: "))
            if choice == 1:
                self.io.input_field(self, "name", str)
            elif choice == 2:
                self.io.input_field(self, "age", int)
            elif choice == 3:
                self.io.input_field(self, "group", str)
            elif choice == 4:
                self.io.input_field(self, "record_book", str)
            elif choice == 5:
                self.io.input_field(self, "avg_grade", float)
            else:
                print("Неверный выбор")
        except Exception:
            print("Ошибка ввода")

    def validate(self, field_name, value):
        if field_name == "age":
            if value < 16 or value > 120:
                raise ValueError("Возраст должен быть от 16 до 120 лет")
        elif field_name == "avg_grade":
            if value < 0.0 or value > 5.0:
                raise ValueError("Средний балл должен быть от 0 до 5")
        elif field_name in {"group", "record_book", "name"}:
            if len(str(value).strip()) == 0:
                raise ValueError("Поле не может быть пустым")
        return value

