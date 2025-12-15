class ConsoleIO:
    def input_field(self, obj, field_name):
        return input(f"Введите {field_name} для {obj.__class__.__name__}: ")

    def output_field(self, obj, field_name):
        return f"{field_name}: {getattr(obj, field_name)}"