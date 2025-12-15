from .flask_io import FlaskIO


class BaseEntity:
    def __init__(self, io_strategy=None):
        self.io = io_strategy or FlaskIO()
        self.name = ""
        self.age = 0

    def read_fields(self):
        self.name = self.io.input_field("name", self.name).strip()
        self._age_input = self.io.input_field("age", str(self.age)).strip()

    def validate_and_save(self):
        if not self.name:
            raise ValueError("ФИО обязательно")

        if not self._age_input:
            raise ValueError("Возраст обязателен")

        try:
            age = int(self._age_input)
            if not (16 <= age <= 100):
                raise ValueError("Возраст должен быть от 16 до 100")
            self.age = age
        except ValueError:
            raise ValueError("Возраст должен быть числом от 16 до 100")

    def generate_form(self):
        html = self.io.field_html("name", "ФИО", self.name)
        html += self.io.field_html("age", "Возраст", str(self.age))
        return html


class Student(BaseEntity):
    pass


class Starosta(BaseEntity):
    def __init__(self, io_strategy=None):
        super().__init__(io_strategy)
        self.group_role = ""

    def read_fields(self):
        super().read_fields()
        self.group_role = self.io.input_field("group_role", self.group_role).strip()

    def validate_and_save(self):
        super().validate_and_save()

    def generate_form(self):
        html = super().generate_form()
        html += self.io.field_html("group_role", "Роль в группе", self.group_role)
        return html


class Proforg(BaseEntity):
    def __init__(self, io_strategy=None):
        super().__init__(io_strategy)
        self.union_activity = ""

    def read_fields(self):
        super().read_fields()
        self.union_activity = self.io.input_field(
            "union_activity", self.union_activity
        ).strip()

    def validate_and_save(self):
        super().validate_and_save()

    def generate_form(self):
        html = super().generate_form()
        html += self.io.field_html(
            "union_activity", "Число коллаборантов", self.union_activity
        )
        return html
