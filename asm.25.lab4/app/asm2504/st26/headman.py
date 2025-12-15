import re
from typing import Any, Tuple

from .student import *

class Headman(Student):
    """Староста"""
    def __init__(self, io = None):
        super().__init__(io)
        self.meetingsHeld: int = 0
        self.electronicJournal: bool = False

    def setData(self, d):
        super().setData(d)
        if d:
            self.__dict__.update(d)

    def getData(self):
        d = super().getData()
        return {**d, **self.__dict__}

    def input_fields(self):
        super().input_fields()
        self.io.input_field(self, "meetingsHeld")
        self.io.input_field(self, "electronicJournal")

    def edit_fields(self):
        super().edit_fields()
        self.io.input_field(self, "meetingsHeld")
        self.io.input_field(self, "electronicJournal")

    def output_fields(self):
        output =super().output_fields()
        self.io.output_field(self, "meetingsHeld", output)
        self.io.output_field(self, "electronicJournal", output)
        return output
