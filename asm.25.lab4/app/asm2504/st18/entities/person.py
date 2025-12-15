class Person:
    def __init__(self, name="", age=0, gender="", io_strategy=None):
        self.name = name
        self.age = age
        self.gender = gender
        self.io_strategy = io_strategy

    def input_data(self):
        if self.io_strategy:
            self.name = self.io_strategy.input_field(self, "name")
            self.age = int(self.io_strategy.input_field(self, "age"))
            self.gender = self.io_strategy.input_field(self, "gender")

    def output_data(self):
        if self.io_strategy:
            self.io_strategy.output_field(self, "name")
            self.io_strategy.output_field(self, "age")
            self.io_strategy.output_field(self, "gender")

    def edit_field(self, field_name, value):
        if hasattr(self, field_name):
            setattr(self, field_name, value)
        else:
            print("Такого поля нет!")

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name}, age={self.age}, gender={self.gender})"
