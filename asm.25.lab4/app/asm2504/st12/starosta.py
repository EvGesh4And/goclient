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

