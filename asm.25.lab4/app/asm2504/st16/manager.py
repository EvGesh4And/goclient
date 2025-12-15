from .employee import Employee


class Manager(Employee):
    def __init__(self, io):
        super().__init__(io)
        self.team_size = 0

    def get_editable_fields(self):
        return super().get_editable_fields() + ['team_size']


    def set_data(self):
        super().set_data()
        self.team_size = self.io.input_field(self, 'team_size')

    def get_data(self):
        output = super().get_data()
        self.io.output_field(self, 'team_size', output)
        return output


