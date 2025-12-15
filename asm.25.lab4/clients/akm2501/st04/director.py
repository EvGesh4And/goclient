from .employee import Employee

class Director(Employee):
    def __init__(self):
        super().__init__()
        self.title = ""

    def input_data(self):
        super().input_data()
        self.title = input("Титул: ") or self.title

    def __str__(self):
        return f"{super().__str__()}, Титул: {self.title}"