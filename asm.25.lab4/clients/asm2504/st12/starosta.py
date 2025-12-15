from .student import Student


class Starosta(Student):
    FIELDS = {
        "name": str,
        "age": int,
        "group": str,
        "record_book": str,
        "avg_grade": float,
        "phone": str,
        "duties": str,
    }

    def __init__(self):
        super().__init__()
        self.phone = ""
        self.duties = ""

    def input_fields(self):
        super().input_fields()
        if self.io is None:
            return
        self.io.input_field(self, "phone", str)
        self.io.input_field(self, "duties", str)

    def print_fields(self):
        super().print_fields()
        if self.io is None:
            return
        self.io.print_field(self, "phone")
        self.io.print_field(self, "duties")

    def edit_single_field(self):
        print("Доступные поля для редактирования:")
        print("1. name")
        print("2. age")
        print("3. group")
        print("4. record_book")
        print("5. avg_grade")
        print("6. phone")
        print("7. duties")
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
            elif choice == 6:
                self.io.input_field(self, "phone", str)
            elif choice == 7:
                self.io.input_field(self, "duties", str)
            else:
                print("Неверный выбор")
        except Exception:
            print("Ошибка ввода")

    def validate(self, field_name, value):
        value = super().validate(field_name, value)
        if field_name == "phone" and len(str(value).strip()) < 7:
            raise ValueError("Телефон слишком короткий")
        return value

