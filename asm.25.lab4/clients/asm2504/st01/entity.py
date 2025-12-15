if __name__ != '__main__':
    from .console_io import ConsoleIO
else:
    from console_io import ConsoleIO

class BaseEntity:
    def __init__(self, io_strategy=None):
        self.io_strategy = io_strategy or ConsoleIO()
        self.name = ""
        self.age = 0
        self.id = None

    def input_fields(self):
        """Ввод полей с использованием стратегии IO."""
        self.name = self.io_strategy.input_field("Введите имя: ")
        while True:
            try:
                age = int(self.io_strategy.input_field("Введите возраст (16-100): "))
                if 16 <= age <= 100:
                    self.age = age
                    break
                else:
                    print("Возраст должен быть от 16 до 100 лет.")
            except ValueError:
                print("Введите корректное целое число для возраста.")

    def output_fields(self):
        """Вывод полей с использованием стратегии IO."""
        self.io_strategy.output_field("Имя", self.name)
        self.io_strategy.output_field("Возраст", self.age)

    def to_dict(self):
        """Сериализация в dict для хранения."""
        return {
            'type': self.__class__.__name__,
            'name': self.name,
            'age': self.age,
            'id': self.id
        }

    @classmethod
    def from_dict(cls, data, io_strategy=None):
        """Десериализация из dict."""
        if data['type'] == 'Student':
            obj = Student(io_strategy)
        elif data['type'] == 'Starosta':
            obj = Starosta(io_strategy)
        else:
            raise ValueError(f"Неизвестный тип: {data['type']}")
        # Заполняем поля из словаря
        obj.name = data.get('name', '')
        obj.age = data.get('age', 0)
        obj.id = data.get('id')
        return obj

class Student(BaseEntity):
    def input_fields(self):
        super().input_fields()

    def output_fields(self):
        super().output_fields()

class Starosta(BaseEntity):
    def __init__(self, io_strategy=None):
        super().__init__(io_strategy)
        self.group_role = ""

    def input_fields(self):
        super().input_fields()
        self.group_role = self.io_strategy.input_field("Введите роль в группе: ")

    def output_fields(self):
        super().output_fields()
        self.io_strategy.output_field("Роль в группе", self.group_role)

    def to_dict(self):
        data = super().to_dict()
        data['group_role'] = self.group_role
        return data

    @classmethod
    def from_dict(cls, data, io_strategy=None):
        obj = super(Starosta, cls).from_dict(data, io_strategy)
        obj.group_role = data.get('group_role', '')
        return obj