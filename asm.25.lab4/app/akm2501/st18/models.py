import datetime


class Item:
    def __init__(self):
        self.id = 0
        self.created_at = datetime.datetime.now()

    def get_id(self):
        return self.id

    def get_data(self):
        return self.__dict__

    def set_data(self, data):
        if data:
            self.__dict__.update(data)

    def get_info(self):
        return [self.id, 'Item']

    def input(self, io):
        pass

    def output(self, io):
        io.print(str(self))

    def __str__(self):
        return f"ID: {self.id}\nCreated At: {self.created_at}"


class Student(Item):
    def __init__(self):
        super().__init__()
        self.name = ''
        self.age = 0
        self.group_name = ''

    def get_info(self):
        return [self.id, self.name, 'student']

    def input(self, io):
        super().input(io)
        self.name = io.input('name', '')
        age_value = io.input('age', 0)
        try:
            self.age = int(age_value)
        except (ValueError, TypeError):
            self.age = 0
        self.group_name = io.input('group_name', '')

    def __str__(self):
        return f"{super().__str__()}\nName: {self.name}\nAge: {self.age}\nGroup: {self.group_name}\n--"


class Employee(Item):
    def __init__(self):
        super().__init__()
        self.name = ''
        self.position = ''

    def get_info(self):
        return [self.id, self.name, 'employee']

    def input(self, io):
        super().input(io)
        self.name = io.input('name', '')
        self.position = io.input('position', '')

    def __str__(self):
        return f"{super().__str__()}\nName: {self.name}\nPosition: {self.position}\n--"
