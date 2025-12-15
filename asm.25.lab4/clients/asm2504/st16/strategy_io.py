
class Strategy_IO:
    def input_field(self, obj, field_name, hint=None):
        raise NotImplementedError

    def output_field(self, obj, field_name):
        return NotImplementedError

class Console_IO(Strategy_IO):
    def input_field(self, obj, field_name, hint=None):
        return input(f'{field_name} ({hint}) = ')

    def output_field(self, obj, field_name):
        print (f"{field_name} = {getattr(obj, field_name)}")







