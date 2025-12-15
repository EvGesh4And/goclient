from .person import Person

class Teacher(Person):
    def __init__(self, name="", age=0, gender="м", department="", position="", salary=0.0, io_strategy=None):
        super().__init__(name, age, gender, io_strategy)
        self.department = department
        self.position = position
        self.salary = salary

    def input_data(self):
        super().input_data()
        if self.io_strategy:
            self.department = self.io_strategy.input_field(self, "department")
            self.position = self.io_strategy.input_field(self, "position")
            self.salary = float(self.io_strategy.input_field(self, "salary"))

    def __repr__(self):
        return (f"Teacher(name={self.name}, age={self.age}, gender={self.gender}, "
                f"department={self.department}, position={self.position}, salary={self.salary})")
