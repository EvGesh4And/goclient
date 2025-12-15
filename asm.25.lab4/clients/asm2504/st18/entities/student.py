from .person import Person

class Student(Person):
    def __init__(self, name="", age=0, gender="м", faculty="", group="", gpa=0.0, io_strategy=None):
        super().__init__(name, age, gender, io_strategy)
        self.faculty = faculty
        self.group = group
        self.gpa = gpa

    def input_data(self):
        super().input_data()
        if self.io_strategy:
            self.faculty = self.io_strategy.input_field(self, "faculty")
            self.group = self.io_strategy.input_field(self, "group")
            self.gpa = float(self.io_strategy.input_field(self, "gpa"))

    def output_data(self):
        super().output_data()
        if self.io_strategy:
            self.io_strategy.output_field(self, "faculty")
            self.io_strategy.output_field(self, "group")
            self.io_strategy.output_field(self, "gpa")

    def __repr__(self):
        return (f"Student(name={self.name}, age={self.age}, gender={self.gender}, "
                f"faculty={self.faculty}, group={self.group}, gpa={self.gpa})")