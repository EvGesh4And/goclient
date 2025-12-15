from typing import Tuple, Any
from .student_base import StudentBase

class StudentBachelor(StudentBase):
    TYPE_NAME = "Бакалавр"
    fields = {
        "full_name": "ФИО",
        "age": "Возраст",
        "group": "Название группы",
        "gpa": "Средний балл",
        "diploma_topic": "Тема дипломной работы"
    }

    def validate_field(self, field_name: str, raw: str) -> Tuple[bool, Any]:
        if field_name == "age":
            if raw == "":
                return (False, "Поле не может быть пустым")
            try:
                val = int(raw)
            except ValueError:
                return (False, "Ожидалось целое число")
            if not (1 <= val <= 150):
                return (False, "Возраст должен быть в диапазоне 1-150")
            return (True, val)

        if field_name == "gpa":
            if raw == "":
                return (False, "Поле не может быть пустым")
            try:
                val = float(raw.replace(",", "."))
            except ValueError:
                return (False, "Ожидалось число")
            if not (0.0 <= val <= 5.0):
                return (False, "Средний балл должен быть в диапазоне 0.0-5.0")
            return (True, val)

        return super().validate_field(field_name, raw)
