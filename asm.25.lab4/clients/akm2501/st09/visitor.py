class Visitor:
    def __init__(self, io_strategy=None):
        self.name = ""
        self.age = 0
        self.io_strategy = io_strategy
        self.type = 'Visitor'
    
    def set_io_strategy(self, io_strategy):
        self.io_strategy = io_strategy
    
    def input(self):
        if self.io_strategy:
            self.name = self.io_strategy.input("Введите имя: ")
            self.age = int(self.io_strategy.input("Введите возраст: "))
    
    def output(self, field_name):
        if self.io_strategy:
            if field_name == "name":
                self.io_strategy.output(f"Имя: {self.name}")
            elif field_name == "age":
                self.io_strategy.output(f"Возраст: {self.age}")
    
    def to_dict(self):
        return {
            'type': self.type,
            'name': self.name,
            'age': self.age
        }
    
    @classmethod
    def from_dict(cls, data, io_strategy=None):
        obj = cls(io_strategy)
        obj.name = data.get('name', '')
        obj.age = data.get('age', 0)
        return obj
    
    def __str__(self):
        return f"Посетитель: {self.name}, Возраст: {self.age}"

class Guest(Visitor):
    def __init__(self, io_strategy=None):
        super().__init__(io_strategy)
        self.pass_type = ""
        self.type = 'Guest'
    
    def input(self):
        super().input()
        if self.io_strategy:
            self.pass_type = self.io_strategy.input("Введите тип абонемента: ")
    
    def output(self, field_name):
        if field_name == "pass_type":
            if self.io_strategy:
                self.io_strategy.output(f"Тип абонемента: {self.pass_type}")
        else:
            super().output(field_name)
    
    def to_dict(self):
        data = super().to_dict()
        data['pass_type'] = self.pass_type
        return data
    
    @classmethod
    def from_dict(cls, data, io_strategy=None):
        obj = super().from_dict(data, io_strategy)
        obj.pass_type = data.get('pass_type', '')
        return obj
    
    def __str__(self):
        return f"Гость: {self.name}, Возраст: {self.age}, Тип абонемента: {self.pass_type}"

class Coach(Visitor):
    def __init__(self, io_strategy=None):
        super().__init__(io_strategy)
        self.training_type = ""
        self.type = 'Coach'
    
    def input(self):
        super().input()
        if self.io_strategy:
            self.training_type = self.io_strategy.input("Введите тип тренировок: ")
    
    def output(self, field_name):
        if field_name == "training_type":
            if self.io_strategy:
                self.io_strategy.output(f"Тип тренировок: {self.training_type}")
        else:
            super().output(field_name)
    
    def to_dict(self):
        data = super().to_dict()
        data['training_type'] = self.training_type
        return data
    
    @classmethod
    def from_dict(cls, data, io_strategy=None):
        obj = super().from_dict(data, io_strategy)
        obj.training_type = data.get('training_type', '')
        return obj
    
    def __str__(self):
        return f"Тренер: {self.name}, Возраст: {self.age}, Тип тренировок: {self.training_type}"