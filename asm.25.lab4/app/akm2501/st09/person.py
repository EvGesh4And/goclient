class Person:
    def __init__(self):
        self.id = 0
        self.name = ""
        self.age = 0
        self.type = 'Person'
    
    def to_dict(self):
        return {
            'id': self.id,
            'type': self.type,
            'name': self.name,
            'age': self.age
        }
    
    @classmethod
    def from_dict(cls, data):
        obj = cls()
        obj.id = data.get('id', 0)
        obj.name = data.get('name', '')
        obj.age = data.get('age', 0)
        return obj

class Guest(Person):
    def __init__(self):
        super().__init__()
        self.pass_type = ""
        self.type = 'Guest'
    
    def to_dict(self):
        data = super().to_dict()
        data['pass_type'] = self.pass_type
        return data
    
    @classmethod
    def from_dict(cls, data):
        obj = super().from_dict(data)
        obj.pass_type = data.get('pass_type', '')
        return obj

class Coach(Person):
    def __init__(self):
        super().__init__()
        self.training_type = ""
        self.type = 'Coach'
    
    def to_dict(self):
        data = super().to_dict()
        data['training_type'] = self.training_type
        return data
    
    @classmethod
    def from_dict(cls, data):
        obj = super().from_dict(data)
        obj.training_type = data.get('training_type', '')
        return obj