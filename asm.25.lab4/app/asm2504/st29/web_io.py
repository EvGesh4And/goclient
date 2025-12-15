class WebIO:
    def __init__(self):
        self.form_data = {}

    def set_form_data(self, form_data):
        self.form_data = form_data

    def input_string(self, field_name):
        return self.form_data.get(field_name, "")

    def input_number(self, field_name):
        try:
            return int(self.form_data.get(field_name, 0))
        except ValueError:
            return 0

    def input_float(self, field_name):
        try:
            return float(self.form_data.get(field_name, 0.0))
        except ValueError:
            return 0.0