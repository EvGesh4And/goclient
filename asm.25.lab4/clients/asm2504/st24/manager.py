from .employee import Employee

class Manager(Employee):
    def __init__(self):
        super().__init__()
        self.department = ""

    def input_data(self):
        super().input_data()
        self.department = input(f"Департамент [{self.department or '—'}]: ") or self.department

    def input_data_from_dict(self, data):
        super().input_data_from_dict(data)
        self.department = data.get("department", self.department)