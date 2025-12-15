class Employee:
    def __init__(self):
        self.id = None
        self.name = ""
        self.age = 0

    def input_data(self):
        self.name = input("Имя: ") or self.name
        age = input(f"Возраст [{self.age}]: ") or str(self.age)
        try:
            self.age = int(age)
        except:
            pass

    def __str__(self):
        return f"{self.name}, {self.age} лет"