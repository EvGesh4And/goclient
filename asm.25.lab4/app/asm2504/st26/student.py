import re
from argparse import ArgumentError
from typing import Any, Tuple

from .io_strategy import *

class Student:
    """Студент"""

    def __init__(self, io: IOStrategy = None):
        self.id: int = 0
        self.fio: str = ""
        self.age: int = 0
        self.sex: str = ""
        self.io: FlaskIO = io if io else FlaskIO()

    def setData(self, d):
        if d:
            self.__dict__.update(d)

    def getData(self):
        return self.__dict__

    def input_fields(self):
        self.io.input_field(self, "fio")
        self.io.input_field(self, "age")
        self.io.input_field(self, "sex")

    def edit_fields(self):
        self.io.input_field(self, "fio")
        self.io.input_field(self, "age")
        self.io.input_field(self, "sex")

    def output_fields(self):
        output = {}
        self.io.output_field(self, "id", output)
        self.io.output_field(self, "fio", output)
        self.io.output_field(self, "age", output)
        self.io.output_field(self, "sex", output)
        return output
