class Person:
    def __init__(self, io_strategy=None):
        self.name = ""
        self.age = 0
        self.io_strategy = io_strategy
        self.type = 'Person'
    
    def set_io_strategy(self, io_strategy):
        self.io_strategy = io_strategy
    
    def input_fields(self):
        if self.io_strategy:
            self.name = self.io_strategy.input("Введите имя: ")
            self.age = int(self.io_strategy.input("Введите возраст: "))
    
    def output_fields(self):
        if self.io_strategy:
            self.io_strategy.output(f"Имя: {self.name}")
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

class Worker(Person):
    def __init__(self, io_strategy=None):
        super().__init__(io_strategy)
        self.occupation = ""
        self.type = 'Worker'
    
    def input_fields(self):
        super().input_fields()
        if self.io_strategy:
            self.occupation = self.io_strategy.input("Введите род деятельности: ")
    
    def output_fields(self):
        super().output_fields()
        if self.io_strategy:
            self.io_strategy.output(f"Род деятельности: {self.occupation}")
    
    def to_dict(self):
        data = super().to_dict()
        data['occupation'] = self.occupation
        return data
    
    @classmethod
    def from_dict(cls, data, io_strategy=None):
        obj = super().from_dict(data, io_strategy)
        obj.occupation = data.get('occupation', '')
        return obj

class Hobby(Person):
    def __init__(self, io_strategy=None):
        super().__init__(io_strategy)
        self.hobby = ""
        self.type = 'Hobby'
    
    def input_fields(self):
        super().input_fields()
        if self.io_strategy:
            self.hobby = self.io_strategy.input("Введите хобби: ")
    
    def output_fields(self):
        super().output_fields()
        if self.io_strategy:
            self.io_strategy.output(f"Хобби: {self.hobby}")
    
    def to_dict(self):
        data = super().to_dict()
        data['hobby'] = self.hobby
        return data
    
    @classmethod
    def from_dict(cls, data, io_strategy=None):
        obj = super().from_dict(data, io_strategy)
        obj.hobby = data.get('hobby', '')
        return obj