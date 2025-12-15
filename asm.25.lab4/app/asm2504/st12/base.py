class BasePerson:
    FIELDS = {
        "name": str,
        "age": int,
    }

    def __init__(self):
        self.name = ""
        self.age = 0

