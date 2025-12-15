from .employee import Employee

class Manager(Employee):
    def __init__(self):
        super().__init__()
        self.department = ""

    def input_data(self):
        super().input_data()
        self.department = input("Департамент: ") or self.department

    def __str__(self):
        return f"{super().__str__()}, Департамент: {self.department}"