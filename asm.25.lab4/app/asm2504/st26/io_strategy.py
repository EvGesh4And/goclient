import datetime

from flask import Flask, render_template, request, redirect, url_for, flash
from typing import Callable, Dict, Tuple, Any, Optional
import re


class IOStrategy:
    """Интерфейс для ввода/вывода."""
    def input_field(self, obj: object, field_name: str):
        """Ввод поля."""
        raise NotImplementedError

    def output_field(self, obj: object, field_name: str):
        """Вывод поля."""
        raise NotImplementedError

    def output_message(self, message):
        """Вывод сообщения"""
        raise NotImplementedError

    def input(self, prompt):
        """Ввод"""
        raise NotImplementedError

    def output(self, message):
        """Вывод"""
        raise NotImplementedError

    # def input_number(self, prompt: str, num_type: type = int, min_val = None, max_val = None, ignore_empty: bool = False):
    #     """Ввод и валидация числа"""
    #     raise NotImplementedError
    #
    # def input_string(self, prompt):
    #     """Ввод строки"""
    #     raise NotImplementedError
    #
    # def input_string_regex(self, prompt: str = "", pattern: str = "", error_message: str = None):
    #     """Ввод и валидация строки по регулярному выражению"""
    #     raise NotImplementedError

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class ConsoleIO(IOStrategy):
    def input_field(self, obj: object, field_name: str):
        current = obj.__getattribute__(field_name)
        prompt = f"Enter field '{field_name}' [{current}]: " if current else f"Enter field '{field_name}': "

        def validator(string: str):
            return obj.validate_field(field_name, string)

        value = self.__input_loop(prompt, validator, current)
        # if value is current:
        #     return
        obj.__setattr__(field_name, value)

    def output_field(self, obj: object, field_name: str):
        if hasattr(obj, field_name):
            self.output(f"Field {field_name}: {obj.__getattribute__(field_name)}")
        else:
            raise AttributeError(f"Object {obj} has no attribute {field_name}")

    @classmethod
    def input(cls, prompt: str = ""):
        return input(prompt)

    @classmethod
    def output(cls, message):
        print(message)

    @classmethod
    def __input_loop(cls, prompt: str, validator: Callable[[str], Tuple[bool, Any]], current: Optional[Any] = None):
        while True:
            raw = input(prompt)
            if current is not None and raw == "":
                return current
            raw = raw.strip()
            ok, res = validator(raw)
            if ok:
                return res
            print(f"Error: {res}. Try again.")



    def input_number(self, prompt: str, num_type: type = int, min_val: int | float = None, max_val: int | float = None, ignore_empty: bool = False) :
        if num_type not in (int, float):
                raise AttributeError("Incorrect type")

        raw_value = ""
        while True:
            try:
                raw_value = self.input(prompt)
                value = num_type(raw_value)
                if min_val is not None and value < min_val:
                    self.output(f"The value should be greater than {min_val}")
                    continue
                if max_val is not None and value > max_val:
                    self.output(f"The value should be less than {max_val}")
                    continue
                return value
            except ValueError:
                if raw_value  == "" and ignore_empty:
                        return None
                if num_type == int:
                    self.output("Enter integer number")
                else:
                    self.output("Enter number")

    def input_string(self, prompt: str):
        return self.input(prompt)

    def input_string_regex(self, prompt: str = "", pattern: str = "", error_message: str = None):
        regex = re.compile(pattern)
        if error_message is None:
            error_message = f"String must match pattern: {pattern}"

        while True:
            value = self.input_string(prompt.strip())
            if regex.match(value):
                return value
            else:
                self.output(error_message)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class FlaskIO(IOStrategy):
    def __init__(self):
        super().__init__()

    def input_field(self, obj: object, field_name: str, hint=None):
        value = request.form.get(field_name)
        # if value == '':
        #     value = None
        # if value is not None:
        #     field = obj.__getattribute__(field_name)
        #     match field:
        #         case int():
        #             try:
        #                 value = int(value)
        #             except ValueError:
        #                 value = None
        #         case float():
        #             try:
        #                 value = float(value)
        #             except ValueError:
        #                 value = None
        #         case bool():
        #             try:
        #                 value = float(value)
        #             except ValueError:
        #                 value = None
        #         case datetime.datetime():
        #             try:
        #                 value = datetime.datetime.fromisoformat(value)
        #             except ValueError:
        #                 value = None
        #         case _:
        #             pass
        obj.__setattr__(field_name, value)

    def output_field(self, obj: object, field_name: str, output: Dict[Any, Any]):
        output.update({field_name: getattr(obj, field_name)})

    def output_message(self, message):
        flash(message)

    @classmethod
    def input(cls, prompt: str = ""):
        raise NotImplementedError
        pass

    @classmethod
    def output(cls, message):
        raise NotImplementedError
        pass

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class RESTIO(IOStrategy):
    def __init__(self):
        super().__init__()

    def input_field(self, obj: object, field_name: str, hint=None):
        value = request.form.get(field_name)
        obj.__setattr__(field_name, value)

    def output_field(self, obj: object, field_name: str, output: Dict[Any, Any]):
        output.update({field_name: getattr(obj, field_name)})

    @classmethod
    def input(cls, prompt: str = ""):
        raise NotImplementedError
        pass

    @classmethod
    def output(cls, message):
        raise NotImplementedError
        pass
