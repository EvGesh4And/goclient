import datetime
import pickle, os, sqlite3

from .io_strategy import *
from .student import *
from .headman import *
from .steward import *


class StorageStrategy:
    def __init__(self):
        pass

    def load(self):
        raise NotImplementedError

    def save(self, rewrite: bool):
        raise NotImplementedError

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class PickleStorage(StorageStrategy):
    def __init__(self, work_dir = "./data/asm2504/st26", filename = "storage.pkl"):
        super().__init__()
        self._filename = f"{work_dir}/{filename}"
        self.students: dict[int, Any] = dict()

    def get_all(self):
        return self.students.values()

    def get_by_id(self, _id):
        return self.students.get(_id)

    def add(self, item):
        self.students.update({item.id: item})

    def delete(self, _id):
        try:
            del self.students[_id]
        except Exception as ex:
            raise ex

    def clear(self):
        self.students.clear()
        Student.reset_max_id()

    def load(self):
        if not os.path.exists(self._filename):
            raise Exception(f"File {self._filename} not found")
        try:
            with open(self._filename, "rb") as file:
                return pickle.load(file)
        except Exception as ex:
            raise Exception(f"Error loading data: {ex}")

    def save(self, data, filename = None, rewrite: bool = False):
        if not rewrite and os.path.exists(self._filename):
            raise Exception(f"File {self._filename} already exists")
        try:
            with open(self._filename, "wb") as file:
                pickle.dump(data, file)
        except Exception as ex:
            raise Exception(f"Error saving data: {ex}")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class DBStorage(StorageStrategy):
    def __init__(self, work_dir = "./data/asm2504/st26", filename="storage.db", io = FlaskIO()):
        super().__init__()
        os.makedirs(work_dir, exist_ok=True)
        self._filename = f"{work_dir}/{filename}"
        self._table_name = "students"
        self._placeholder = "?"
        self.db = sqlite3.connect(self._filename)
        self.db.row_factory = sqlite3.Row
        self.dbc = self.db.cursor()
        self.init_table()
        self.io = io

    def init_table(self):
        items = {**Student().output_fields(), **Headman().output_fields(), **Steward().output_fields()}

        fields = "id INTEGER PRIMARY KEY AUTOINCREMENT"
        fields += ", type TEXT NOT NULL"
        for field, value in items.items():
            if field == "id":
                continue
            fields += f", {field} "
            match value:
                case int():
                    fields += "INTEGER"
                case float():
                    fields += "REAL"
                case bool():
                    fields += "INTEGER"
                case datetime.datetime():
                    fields += "TEXT"
                case _:
                    fields += "TEXT"
        self.dbc.execute(f"CREATE TABLE IF NOT EXISTS {self._table_name}({fields})")
        self.db.commit()

    def _get_max_id(self):
        self.dbc.execute("SELECT MAX(id) FROM {self._table_name}")
        return self.dbc.fetchone()[0]

    def _reconstruct_item(self, row):
        _type = row[1]
        if _type == "Student":
            item = Student(self.io)
        elif _type == "Headman":
            item = Headman(self.io)
        elif _type == "Steward":
            item = Steward(self.io)
        else:
            raise ValueError(f"Unknown type: {_type}")
        item.setData(row)
        return item

    def get_items(self):
        self.dbc.execute(f"SELECT * FROM {self._table_name} ORDER BY id")
        return [self._reconstruct_item(row) for row in self.dbc.fetchall()]

    def get_item(self, _id: int):
        self.dbc.execute(f"SELECT * FROM {self._table_name} WHERE id = {self._placeholder}", (int(_id),))
        row = self.dbc.fetchone()
        if row:
            return self._reconstruct_item(row)
        return None

    def process_item(self, item, rewrite: bool = False):
        names = ""
        values = ""
        params = []
        update = ""
        for field, value in {**{"type": item.__class__.__name__}, **item.output_fields()}.items():
            if field == "id":
                if rewrite:
                    pass
                else:
                    continue
            if names:
                names += f", {field}"
                values += f", {self._placeholder}"
                update += f", {field} = {self._placeholder}"
            else:
                names = field
                values = self._placeholder
                update = f"{field} = {self._placeholder}"
            params.append(value)

        if not item.id or int(item.id) == 0 or rewrite:
            self.dbc.execute(f"INSERT INTO {self._table_name}({names}) VALUES ({values})", params)
        else:
            params.append(int(item.id))
            self.dbc.execute(f"UPDATE {self._table_name} SET {update} WHERE id = {self._placeholder}", params)
        self.db.commit()

    def delete_item(self, _id):
        self.dbc.execute(f"DELETE FROM {self._table_name} WHERE id = {self._placeholder}", (_id,))
        self.db.commit()

    def clear_items(self):
        self.dbc.execute(f"DELETE FROM {self._table_name}")
        self.dbc.execute(f"DELETE FROM sqlite_sequence WHERE name = {self._placeholder}", (self._table_name,))
        self.db.commit()

    def load(self):
        raise NotImplementedError
        pass  # Data is persistent in DB

    def save(self, rewrite: bool = False):
        raise NotImplementedError
        pass  # Commits are done in operations