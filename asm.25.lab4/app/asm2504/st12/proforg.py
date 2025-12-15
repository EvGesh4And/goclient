from .student import Student


class Proforg(Student):
    FIELDS = {
        "name": str,
        "age": int,
        "group": str,
        "record_book": str,
        "avg_grade": float,
        "union_member": bool,
        "events_count": int,
    }

    def __init__(self):
        super().__init__()
        self.union_member = False
        self.events_count = 0

