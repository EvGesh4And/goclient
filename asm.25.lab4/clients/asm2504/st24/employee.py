class Employee:
    def __init__(self):
        self.id = None
        self.name = ""
        self.age = 0

    def input_data(self):
        self.name = input(f"Имя [{self.name or '—'}]: ") or self.name
        age_input = input(f"Возраст [{self.age}]: ") or str(self.age)
        try:
            self.age = int(age_input)
        except ValueError:
            pass

    def input_data_from_dict(self, data):
        self.name = data.get("name", self.name)
        age = data.get("age")
        if age is not None:
            try:
                self.age = int(age)
            except:
                pass

    def __str__(self):
        return f"{self.name}, {self.age} лет"