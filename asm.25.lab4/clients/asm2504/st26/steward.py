import re
from typing import Any, Tuple

from .student import Student

class Steward(Student):
    """Профорг"""
    def __init__(self, io = None):
        super().__init__(io)
        self.ticketNumber: int | None = None
        self.specialization: str | None = None

    def input_fields(self):
        super().input_fields()
        # self.ticketNumber = self.io.input_number("Enter ticket number: ", int, 0)
        # self.specialization = self.io.input("Enter specialization: ")

        self.io.input_field(self, "ticketNumber")
        self.io.input_field(self, "specialization")

    def edit_fields(self):
        super().edit_fields()
        # ticketNumber = self.io.input_number(f"Ticket number [{self.ticketNumber}]: ", int, 0, ignore_empty=True)
        # specialization = self.io.input_string(f"Specialization [{self.specialization}]: ")
        # if ticketNumber: self.ticketNumber = ticketNumber
        # if specialization: self.age = specialization

        self.io.input_field(self, "ticketNumber")
        self.io.input_field(self, "specialization")


    def output_fields(self):
        super().output_fields()
        # self.io.output(f"Ticket number: {self.ticketNumber}")
        # self.io.output(f"Specialization: {self.specialization}")
        self.io.output_field(self, "ticketNumber")
        self.io.output_field(self, "specialization")

    def validate_field(self, field_name: str, raw: str) -> Tuple[bool, Any]:
        if field_name == "ticketNumber":
            try:
                value = int(raw)
                if 0 < value:
                    return True, value
                else:
                    return False, "Ticket number should be greater than 0"
            except ValueError:
                return False, "Ticket number should be an integer"
        if field_name == "specialization":
            if not isinstance(raw, str):
                return False, "Ожидалась строка"
            if not raw:
                return False, "Специализация не может быть пустой"
            if len(raw) < 2:
                return False, "Слишком короткая специализация (<2 символов)"
            if len(raw) > 50:
                return False, "Слишком длинная специализация (>50 символов)"
            pattern = r"^[А-Яа-яЁёA-Za-z][А-Яа-яЁёA-Za-z0-9\-_]*$"
            if re.fullmatch(pattern, raw):
                return True, raw
            return False, "Содержит недопустимые символы или начинается не с буквы"
        return super().validate_field(field_name, raw)