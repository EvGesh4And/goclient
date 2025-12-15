# entity.py
from typing import Dict, Any


class Employee:
    def __init__(self, io_strategy=None):
        self.io = io_strategy
        self.name = ""
        self.email = ""
        self.experience = 0  # стаж в годах

    def input_fields(self):
        """Заполнить поля через стратегию IO (ожидается: io.input_field(name, label) -> str)."""
        self.name = self.io.input_field("name", "Имя сотрудника")
        self.email = self.io.input_field("email", "Email сотрудника")

        exp_str = self.io.input_field("experience", "Стаж работы (в годах)")
        try:
            exp = int(exp_str) if exp_str != "" else 0
            if exp >= 0:
                self.experience = exp
            else:
                raise ValueError("Стаж не может быть отрицательным")
        except ValueError as e:
            raise ValueError(f"Некорректный стаж: {e}")

    def generate_form(self) -> str:
        html = ""
        html += self.io.field_html("name", "Имя сотрудника", self.name)
        html += self.io.field_html("email", "Email сотрудника", self.email)
        html += self.io.field_html("experience", "Стаж работы (в годах)", str(self.experience))
        return html

    def display(self) -> str:
        return (
            f"<p><strong>Имя:</strong> {self.name}</p>"
            f"<p><strong>Email:</strong> {self.email}</p>"
            f"<p><strong>Стаж:</strong> {self.experience} лет</p>"
        )

    # --- сериализация ---
    def to_dict(self) -> Dict[str, Any]:
        """Сериализуем поле type, общие поля — без io."""
        return {
            "type": self.__class__.__name__,
            "name": self.name,
            "email": self.email,
            "experience": self.experience,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any], io_strategy=None):
        """Восстановление корректного подкласса по полю 'type'."""
        type_map = {
            "Employee": Employee,
            "Worker": Worker,
            "Manager": Manager,
            "Director": Director,
        }
        t = data.get("type", "Employee")
        if t not in type_map:
            raise ValueError(f"Неизвестный тип сущности: {t}")
        obj = type_map[t](io_strategy)
        obj.name = data.get("name", "")
        obj.email = data.get("email", "")
        obj.experience = data.get("experience", 0)
        # доп. поля у подклассов будут заполнены их from_dict
        if hasattr(type_map[t], "after_from_dict"):
            # вызов для подпclass-специфики
            type_map[t].after_from_dict(obj, data)
        return obj


class Worker(Employee):
    def __init__(self, io_strategy=None):
        super().__init__(io_strategy)
        self.profession = ""

    def input_fields(self):
        super().input_fields()
        prof = self.io.input_field("profession", "Профессия")
        if prof is not None:
            self.profession = prof

    def generate_form(self) -> str:
        return super().generate_form() + self.io.field_html("profession", "Профессия", self.profession)

    def display(self) -> str:
        return super().display() + f"<p><strong>Профессия:</strong> {self.profession}</p>"

    def to_dict(self):
        d = super().to_dict()
        d["profession"] = self.profession
        return d

    @staticmethod
    def after_from_dict(obj, data):
        obj.profession = data.get("profession", "")


class Manager(Employee):
    def __init__(self, io_strategy=None):
        super().__init__(io_strategy)
        self.department = ""

    def input_fields(self):
        super().input_fields()
        dep = self.io.input_field("department", "Отдел")
        if dep is not None:
            self.department = dep

    def generate_form(self) -> str:
        return super().generate_form() + self.io.field_html("department", "Отдел", self.department)

    def display(self) -> str:
        return super().display() + f"<p><strong>Отдел:</strong> {self.department}</p>"

    def to_dict(self):
        d = super().to_dict()
        d["department"] = self.department
        return d

    @staticmethod
    def after_from_dict(obj, data):
        obj.department = data.get("department", "")


class Director(Employee):
    def __init__(self, io_strategy=None):
        super().__init__(io_strategy)
        self.company = ""

    def input_fields(self):
        super().input_fields()
        comp = self.io.input_field("company", "Компания")
        if comp is not None:
            self.company = comp

    def generate_form(self) -> str:
        return super().generate_form() + self.io.field_html("company", "Компания", self.company)

    def display(self) -> str:
        return super().display() + f"<p><strong>Компания:</strong> {self.company}</p>"

    def to_dict(self):
        d = super().to_dict()
        d["company"] = self.company
        return d

    @staticmethod
    def after_from_dict(obj, data):
        obj.company = data.get("company", "")
