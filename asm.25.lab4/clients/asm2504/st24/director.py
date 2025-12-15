from .employee import Employee

class Director(Employee):
    def __init__(self):
        super().__init__()
        self.title = ""

    def input_data(self):
        super().input_data()
        self.title = input(f"Титул [{self.title or '—'}]: ") or self.title

    def input_data_from_dict(self, data):
        super().input_data_from_dict(data)
        self.title = data.get("title", self.title)