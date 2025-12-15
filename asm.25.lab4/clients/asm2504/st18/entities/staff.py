from .person import Person

class Staff(Person):
    def __init__(self, name="", age=0, gender="м", department="", position="", experience=0, salary=0.0, io_strategy=None):
        super().__init__(name, age, gender, io_strategy)
        self.department = department
        self.position = position
        self.experience = experience
        self.salary = salary

    def input_data(self):
        super().input_data()
        if self.io_strategy:
            self.department = self.io_strategy.input_field(self, "department")
            self.position = self.io_strategy.input_field(self, "position")
            self.experience = int(self.io_strategy.input_field(self, "experience"))
            self.salary = float(self.io_strategy.input_field(self, "salary"))

    def output_data(self):
        super().output_data()
        if self.io_strategy:
            self.io_strategy.output_field(self, "department")
            self.io_strategy.output_field(self, "position")
            self.io_strategy.output_field(self, "experience")
            self.io_strategy.output_field(self, "salary")

    def __repr__(self):
        return (f"Staff(name={self.name}, age={self.age}, gender={self.gender}, "
                f"department={self.department}, position={self.position}, "
                f"experience={self.experience}, salary={self.salary})")