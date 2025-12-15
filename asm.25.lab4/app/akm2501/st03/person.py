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

class Worker(Person):
    def __init__(self):
        super().__init__()
        self.occupation = ""
        self.type = 'Worker'
    
    def to_dict(self):
        data = super().to_dict()
        data['occupation'] = self.occupation
        return data
    
    @classmethod
    def from_dict(cls, data):
        obj = super().from_dict(data)
        obj.occupation = data.get('occupation', '')
        return obj

class Hobby(Person):
    def __init__(self):
        super().__init__()
        self.hobby = ""
        self.type = 'Hobby'
    
    def to_dict(self):
        data = super().to_dict()
        data['hobby'] = self.hobby
        return data
    
    @classmethod
    def from_dict(cls, data):
        obj = super().from_dict(data)
        obj.hobby = data.get('hobby', '')
        return obj