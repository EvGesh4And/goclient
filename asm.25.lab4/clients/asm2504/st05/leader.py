from dataclasses import dataclass

from .io_handler import IOHandler
from .student import Student


@dataclass
class Leader(Student):
    group: str = ""

    def get_data(self):
        d = super().get_data()
        d.update({'cls_id': 2})
        return d

    def input(self):
        super().input()
        self.group = self.io_handler.read("group")

    def output(self):
        super().output()
        self.io_handler.write("Группа", self.group)

    def load(self, row):
        self.id = row['id']
        self.name = row['name']
        self.age = row['age']
        self.group = row['group_name']

    def store(self, db):
        if not self.id or int(self.id) == 0:
            db.execute("insert into students values(NULL, ?, ?, ?, ?)",
                       (self.age, self.name, self.group, self.__class__.__name__.lower()))
        else:
            db.execute("update students set age=?, name=?, group_name=?, type=? where id=?",
                       (self.age, self.name, self.group, self.__class__.__name__.lower(), self.id))

    def __str__(self):
        return f"Староста \nИмя:{self.name}\nВозраст:{self.age}\nГрупп:{self.group}"

    def to_dict(self):
        base = super().to_dict()
        base.update({'type': 'leader'})
        base.update({'group': self.group})
        return base