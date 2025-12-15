import re
from .strategy_io import Strategy_IO

class Employee:

    def __init__(self, io_strategy=None):
        self.id = None
        self.name = ""
        self.age = 0
        self.sex = ""
        self.department = ""
        self.salary = 0
        self.io = Strategy_IO() if io_strategy is None else io_strategy

    @property
    def title(self):
        return self.__class__.__name__

    def set_data(self):
        self.name = self.io.input_field(self, 'name')
        self.age = self.io.input_field(self, 'age')
        self.sex = self.io.input_field(self, 'sex')
        self.department = self.io.input_field(self, 'department')
        self.salary = self.io.input_field(self, 'salary')

    def get_data(self):
        output = {}
        self.io.output_field(self, 'title', output)
        self.io.output_field(self, 'name', output)
        self.io.output_field(self, 'age', output)
        self.io.output_field(self, 'sex', output)
        self.io.output_field(self, 'department', output)
        self.io.output_field(self, 'salary', output)
        return output

    def get_editable_fields(self):
        return ['name', 'age', 'sex', 'department', 'salary']

    def update_data(self, form_data):
        for field in self.get_editable_fields():
            if field in form_data:
                setattr(self, field, form_data[field])