if __name__ == 'main':
    from strategy_io import Strategy_IO
else:
    from .strategy_io import Strategy_IO

class Employee:

    def __init__(self, io_strategy=None):
        self.id = None
        self.name = ""
        self.age = 0
        self.sex = ""
        self.department = ""
        self.salary = 0
        self.io = Strategy_IO() if None else io_strategy

    def get_editable_fields(self):
        return ['name', 'age', 'sex', 'department', 'salary']


    def set_data(self):
        self.name = self.io.input_field(self, 'name', 'Type name')

        try:
            self.age = int(self.io.input_field(self, 'age', 'Type age'))
        except ValueError:
            self.age = 0

        self.sex = self.io.input_field(self, 'sex', 'Male/Female')
        self.department = self.io.input_field(self, 'department', '"IT", "Marketing", "Sales", "HR", "Management", "Law"')

        try:
            self.salary = int(self.io.input_field(self, 'salary', 'Type salary'))
        except ValueError:
            self.salary = 0

    def get_data(self):
        self.io.output_field(self, 'id')
        self.io.output_field(self, 'name')
        self.io.output_field(self, 'age')
        self.io.output_field(self, 'sex')
        self.io.output_field(self, 'department')
        self.io.output_field(self, 'salary')
