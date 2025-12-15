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

