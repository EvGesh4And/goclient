import re
from argparse import ArgumentError
from typing import Any, Tuple

from .io_strategy import ConsoleIO, IOStrategy


class Student:
    """Студент"""
    __MAX_ID: int = 1

    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        return instance

    def __init__(self, io: IOStrategy = None):
        # print("Student __init__")
        self.id: int = self.increment_id()
        self.fio: str | None = None
        self.age: int | None = None
        self.sex: str | None = None
        self.io: IOStrategy = io if io else ConsoleIO()

    def __getstate__(self):
        return self.__dict__

    def __setstate__(self, state):
        self.__dict__.update(state)
        if self.id >= self.__MAX_ID:
            Student.__MAX_ID = self.id + 1

    @classmethod
    def get_max_id(cls):
        return Student.__MAX_ID

    @classmethod
    def reset_max_id(cls):
        Student.__MAX_ID = 1

    @classmethod
    def increment_id(cls):
        _id = cls.__MAX_ID
        Student.__MAX_ID += 1
        return _id

    def input_fields(self):
        # self.fio = self.io.input_string("Enter FIO: ")
        # self.age = self.io.input_number("Enter age: ", int, 16, 100)
        # self.sex = self.io.input_string_regex("Enter sex (male/female): ", r'^(male|female)$', "Invalid sex. Please try again: ")
        self.io.input_field(self, "fio")
        self.io.input_field(self, "age")
        self.io.input_field(self, "sex")

    def edit_fields(self):
        self.io.output("Leave field empty to keep current value")
        # fio = self.io.input(f"FIO [{self.fio}]: ")
        # age = self.io.input_number(f"Age [{self.age}]: ", int, 16, 100, ignore_empty=True)
        # sex = self.io.input_string_regex(f"Sex (male/female) [{self.sex}]: ", r'^(male|female)?$', "Invalid sex. Please try again: ")
        # if fio: self.fio = fio
        # if age: self.age = age
        # if sex: self.sex = sex

        self.io.input_field(self, "fio")
        self.io.input_field(self, "age")
        self.io.input_field(self, "sex")

    def output_fields(self):
        self.io.output(f"------ {self.__class__.__name__} ID: {self.id} ------")
        # self.io.output(f"FIO: {self.fio}")
        # self.io.output(f"Age: {self.age}")
        # self.io.output(f"Sex: {self.sex}")
        self.io.output_field(self, "fio")
        self.io.output_field(self, "age")
        self.io.output_field(self, "sex")

    def validate_field(self, field_name: str, raw: str) -> Tuple[bool, Any]:
        if field_name == "fio":
            # TODD: Поправить для полного ФИО!!!
            if not isinstance(raw, str):
                return False, "FIO must be a string"
            full_name = ' '.join(raw.strip().split())
            pattern = r"^[А-ЯЁA-Z][а-яёa-z\-']{1,}(?:\s[А-ЯЁA-Z][а-яёa-z\-']{1,}){1,2}$"
            if re.fullmatch(pattern, full_name):
                return True, full_name
            return False, "FIO should be consisted of 2-3 words and each word should start from head letter"
        if field_name == "age":
            try:
                value = int(raw)
                if 16 <= value <= 100:
                    return True, value
                else:
                    return False, "Age must be between 16 and 100"
            except ValueError:
                return False, "Age must be an integer"
        if field_name == "sex":
            if not isinstance(raw, str):
                return False, "Sex must be a string"
            pattern = r"^(male|female)$"
            if re.match(pattern, raw):
                return True, raw
            return False, "Sex should be male or female"
        raise ArgumentError("Invalid field")