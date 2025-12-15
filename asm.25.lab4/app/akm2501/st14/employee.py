class Employee:
    FIELDS = {
        "name": str,
        "age": int
    }

    def __init__(self, io=None):
        self.name = ""
        self.age = 0
        self.io = io

    def input_fields(self):
        if self.io is None:
            return
        for field_name in self.FIELDS.keys():
            self.io.read_field(self, field_name)

    def print_fields(self):
        if self.io is None:
            return
        for field_name in self.FIELDS.keys():
            self.io.write_field(self, field_name)

    def type_name(self):
        return self.__class__.__name__
