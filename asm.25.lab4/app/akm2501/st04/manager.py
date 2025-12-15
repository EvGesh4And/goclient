# manager.py
from .employee import Employee

class Manager(Employee):
    def __init__(self, io):
        super().__init__(io)
        self.department = ""

    def input_data(self):
        super().input_data()
        self.department = self.io.input('department', self.department)

    def output_data(self):
        data = super().output_data()
        data['department'] = self.department
        return data
    def input_data_from_dict(self, data: dict):
        self.name = data.get("name", self.name)
        age = data.get("age")
        if age is not None:
            self.age = int(age) if str(age).isdigit() else self.age
        if hasattr(self, "department"):
            self.department = data.get("department", self.department)
        if hasattr(self, "title"):
            self.title = data.get("title", self.title)