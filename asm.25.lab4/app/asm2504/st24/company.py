import os
import pickle
from .storage import SQLiteStorage
from .io_strategy import FlaskIO

class Company:
    def __init__(self, storage=None, io=None):
        self.storage = storage or SQLiteStorage()
        self.io = io or FlaskIO()
        self.auto_save_file = "data/asm2504/st24/auto_backup.pkl"

    def add_employee(self, emp_type):
        from .employee import Employee
        from .manager import Manager
        from .director import Director

        classes = {'Employee': Employee, 'Manager': Manager, 'Director': Director}
        cls = classes[emp_type]
        emp = cls(self.io)
        emp.input_data()
        self.storage.add(emp)

    def get_employee_list(self):
        return self.storage.get_all_formatted()

    def delete_employee(self, emp_id):
        return self.storage.delete_by_id(emp_id)

    def clear_list(self):
        self.storage.clear()

    def save_to_file(self, filename):
        path = self.storage.save(filename)
        return path

    def load_from_file(self, filename):
        return self.storage.load(filename)
