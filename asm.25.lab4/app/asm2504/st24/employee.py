from .io_strategy import FlaskIO

class Employee:
    def __init__(self, io: FlaskIO):
        self.io = io
        self.id = None
        self.name = ""
        self.age = 0

    def input_data(self):
        self.name = self.io.input('name', self.name)
        age_str = self.io.input('age', str(self.age))
        self.age = int(age_str) if age_str else 0

    def output_data(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age
        }
    
    def input_data_from_dict(self, data: dict):
        self.name = data.get("name", self.name)
        age = data.get("age")
        if age is not None:
            self.age = int(age) if str(age).isdigit() else self.age
        if hasattr(self, "department"):
            self.department = data.get("department", self.department)
        if hasattr(self, "title"):
            self.title = data.get("title", self.title)