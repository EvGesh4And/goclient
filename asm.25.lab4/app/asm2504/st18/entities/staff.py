from ..entities.person import Person

class Staff(Person):
    def __init__(self, name="", age=0, department="", position="", experience=0, io_strategy=None, salary=None):
        super().__init__(name, age, io_strategy)
        self.department = department      
        self.position = position         
        self.experience = experience     
        self.salary = salary     
