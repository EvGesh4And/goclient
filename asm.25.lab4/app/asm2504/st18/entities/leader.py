from .student import Student

class Leader(Student):
    def __init__(self, name="", age=0, group="", position="", io_strategy=None):
        super().__init__(name, age, group, io_strategy)
        self.position = position  # например: староста, профорг

    def input_data(self):
        super().input_data()
        if self.io_strategy:
            self.position = self.io_strategy.input_field(self, "position")

    def output_data(self):
        super().output_data()
        if self.io_strategy:
            self.io_strategy.output_field(self, "position")

    def __repr__(self):
        return (f"{self.__class__.__name__}(name={self.name}, age={self.age}, "
                f"group={self.group}, position={self.position})")
