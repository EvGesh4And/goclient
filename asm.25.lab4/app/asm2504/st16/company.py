from .employee import Employee
from .director import Director
from .manager import Manager
from .strategy_io import Flask_IO

class Company:

    def __init__(self, strategy_io, storage_strategy):
        self.io = strategy_io
        self.storage = storage_strategy

    def add_element(self, employee_type):
        match employee_type:
            case 'Employee':
                person = Employee(self.io)
            case 'Manager':
                person = Manager(self.io)
            case 'Director':
                person = Director(self.io)
        person.set_data()
        self.storage.add_element(person)

    def get_employees(self):
        return self.storage.get_employees()

    def get_employee_by_id(self, emp_id):
        return self.storage.get_by_id(emp_id)

    def update_employee(self, emp_id, form_data):
        emp = self.storage.get_by_id(emp_id)
        if emp:
            emp.update_data(form_data)
            self.storage.update(emp)

    def delete_element(self, emp_id):
        self.storage.delete_employee(emp_id)

    def delete_all_elements(self):
        self.storage.delete_all_employees()

    def save_elements(self):
        all_data = self.get_employees()
        self.storage.save_data(all_data)

    def load_elements(self):
        self.storage.load_data()

    def init_storage(self):
        self.storage.init_storage()






