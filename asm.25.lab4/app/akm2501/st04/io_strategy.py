# io_strategy.py
from flask import request, flash

class FlaskIO:
    def input(self, field_name, default=""):
        return request.form.get(field_name, default)

    def output_message(self, msg):
        flash(msg)

class IOStrategy:
    def input_field(self, obj, field_name):
        raise NotImplementedError

    def output_field(self, obj, field_name):
        raise NotImplementedError

class ConsoleIO(IOStrategy):
    def input_field(self, obj, field_name):
        return input(f"Enter {field_name}: ")

    def output_field(self, obj, field_name):
        value = getattr(obj, field_name)
        print(f"{field_name.capitalize()}: {value}")