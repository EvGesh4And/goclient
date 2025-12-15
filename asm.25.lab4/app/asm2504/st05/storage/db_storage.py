import os
import sqlite3
from ..models.leader import Leader
from ..models.student import Student

selfpath = 'data/asm2504/st05/sql/'

class DBStorage:
    def __init__(self, name):
        print(os.getcwd())
        self.group = None
        self.load()

    def select_type(self, row):
        if row["type"] == "leader":
            return Leader(io_handler=self.group.io_handler)
        else:
            return Student(io_handler=self.group.io_handler)

    def load(self):
        if not os.path.exists(selfpath):
            os.mkdir(selfpath)
        self.db = sqlite3.connect(selfpath+'students.sqlite', detect_types=sqlite3.PARSE_DECLTYPES)
        self.db.execute("""
				   create table if not exists students(
					   id integer primary key autoincrement,
					   age integer,
					   name text,
					   group_name text,
					   type text
					   )""")
        self.db.row_factory = sqlite3.Row
        self.cursor = self.db.cursor()

    def store(self):
        self.db.commit()
        self.db.close()

    def get_item(self, id):
        if id > 0:
            self.cursor.execute("select * from students where id=?", (id,))
            row = self.cursor.fetchone()
            if not row:
                return None
            item = self.select_type(row)
            item.load(row)
            return item
        return None

    def add(self, item):
        item.store(self.db)
        self.db.commit()

    def edit(self, item):
        item.store(self.db)
        self.db.commit()

    def delete(self, id):
        self.db.execute("delete from students where id=?", (id,))
        self.db.commit()

    def get_items(self):
        self.cursor.execute("select * from students order by id desc")
        for row in self.cursor:
            item = self.select_type(row)
            item.load(row)
            yield item

    def size(self):
        self.cursor.execute("select count(*) from students order by id desc")
        n = self.cursor.fetchone()
        return n[0]

    def clear(self):
        self.cursor.execute("delete from students")
        self.db.commit()
