if __name__ == 'main':
    from employee import Employee
else:
    from .employee import Employee

class Director(Employee):
    def __init__(self, io):
        super().__init__(io)
        self.assistant = "" # Есть персональный ассистент или нет

    def get_editable_fields(self):
        return super().get_editable_fields() + ['assistant']

    def set_data(self):
        super().set_data()
        self.assistant = self.io.input_field(self, 'assistant', 'Has assistant? (Yes/No)')

    def get_data(self):
        super().get_data()
        self.io.output_field(self, 'assistant')

