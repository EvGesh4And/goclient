if __name__ != '__main__':
    from .console_io import ConsoleIO
else:
    from console_io import ConsoleIO

class Employee:
    def __init__(self, io_strategy=None):
        self.io_strategy = io_strategy or ConsoleIO()
        self.name = ""
        self.email = ""
        self.experience = 0  # стаж в годах

    def input_fields(self):
        """Ввод полей с использованием стратегии IO."""
        self.name = self.io_strategy.input_field("Введите имя сотрудника")
        self.email = self.io_strategy.input_field("Введите email сотрудника")

        while True:
            try:
                exp = int(self.io_strategy.input_field("Введите стаж работы"))
                if 0 <= exp:
                    self.experience = exp
                    break
                else:
                    print("Стаж не должен быть отрицательным числом.")
            except ValueError:
                print("Введите корректное целое число для стажа.")

    def output_fields(self):
        """Вывод полей с использованием стратегии IO."""
        self.io_strategy.output_field("Имя", self.name)
        self.io_strategy.output_field("Email", self.email)
        self.io_strategy.output_field("Стаж (лет)", self.experience)

    def to_dict(self):
        """Сериализация в dict для хранения."""
        return {
            "type": self.__class__.__name__,
            "name": self.name,
            "email": self.email,
            "experience": self.experience,
        }

    @classmethod
    def from_dict(cls, data, io_strategy=None):
        """Десериализация из dict."""
        type_map = {
            "Employee": Employee,
            "Worker": Worker,
            "Manager": Manager,
            "Director": Director,
        }
        if data["type"] not in type_map:
            raise ValueError(f"Неизвестный тип: {data['type']}")

        obj = type_map[data["type"]](io_strategy)
        obj.name = data.get("name", "")
        obj.email = data.get("email", "")
        obj.experience = data.get("experience", 0)
        return obj


class Worker(Employee):
    def __init__(self, io_strategy=None):
        super().__init__(io_strategy)
        self.profession = ""

    def input_fields(self):
        super().input_fields()
        self.profession = self.io_strategy.input_field("Введите профессию")

    def output_fields(self):
        super().output_fields()
        self.io_strategy.output_field("Профессия", self.profession)

    def to_dict(self):
        data = super().to_dict()
        data["profession"] = self.profession
        return data

    @classmethod
    def from_dict(cls, data, io_strategy=None):
        obj = super(Worker, cls).from_dict(data, io_strategy)
        obj.profession = data.get("profession", "")
        return obj


class Manager(Employee):
    def __init__(self, io_strategy=None):
        super().__init__(io_strategy)
        self.department = ""

    def input_fields(self):
        super().input_fields()
        self.department = self.io_strategy.input_field("Введите отдел")

    def output_fields(self):
        super().output_fields()
        self.io_strategy.output_field("Отдел", self.department)

    def to_dict(self):
        data = super().to_dict()
        data["department"] = self.department
        return data

    @classmethod
    def from_dict(cls, data, io_strategy=None):
        obj = super(Manager, cls).from_dict(data, io_strategy)
        obj.department = data.get("department", "")
        return obj


class Director(Employee):
    def __init__(self, io_strategy=None):
        super().__init__(io_strategy)
        self.company = ""

    def input_fields(self):
        super().input_fields()
        self.company = self.io_strategy.input_field("Введите название компании")

    def output_fields(self):
        super().output_fields()
        self.io_strategy.output_field("Компания", self.company)

    def to_dict(self):
        data = super().to_dict()
        data["company"] = self.company
        return data

    @classmethod
    def from_dict(cls, data, io_strategy=None):
        obj = super(Director, cls).from_dict(data, io_strategy)
        obj.company = data.get("company", "")
        return obj
