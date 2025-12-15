from flask import request

class Strategy_IO:
    def input_field(self, obj, field_name, hint=None):
        raise NotImplementedError

    def output_field(self, obj, field_name, output):
        return NotImplementedError

class Console_IO(Strategy_IO):
    def input_field(self, obj, field_name, hint=None):
        return input(f'{field_name} ({hint}) = ')

    def output_field(self, obj, field_name, output=None):
        print (f"{field_name} = {getattr(obj, field_name)}")

class Flask_IO(Strategy_IO):
    def input_field(self, obj, field_name, hint=None):
        return request.form.get(field_name)

    def output_field(self, obj, field_name, output):
        value = getattr(obj, field_name)
        output.update({field_name: value})
