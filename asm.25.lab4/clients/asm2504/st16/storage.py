import pickle
import os
import requests

if __name__ == '__main__':
    from employee import Employee
    from manager import Manager
    from director import Director
else:
    from .employee import Employee
    from .manager import Manager
    from .director import Director

class Storage:
    def save_data(self, data):
        return NotImplementedError
    def load_data(self):
        return NotImplementedError

class Pickle_Storage(Storage):
    def __init__(self, filename = 'data.pkl'):
        super().__init__()
        current_dir = os.path.dirname(os.path.abspath(__file__))
        student_folder = os.path.basename(current_dir)
        group_folder = os.path.basename(os.path.dirname(current_dir))
        project_root = os.path.abspath(os.path.join(current_dir, '..', '..', '..'))
        target_dir = os.path.join(project_root, 'data', group_folder, student_folder)
        os.makedirs(target_dir, exist_ok=True)
        self.filename = os.path.join(target_dir, filename)

    def save_data(self, data):
        if not data:
            print('There is nothing to save')
            return
        try:
            with open(self.filename, 'wb') as file:
                pickle.dump(data, file)
            print('Data was successfully saved')
        except Exception as e:
            print(f'An unexpected error occurred while saving data: {e}')

    def load_data(self):
        try:
            with open(self.filename, 'rb') as file:
                entities = pickle.load(file)
            print(f"Loading from {self.filename} was successful")
            return entities
        except Exception as e:
            print(f'An unexpected error occurred while loading data: {e}')
            return []


class API_Storage(Storage):
    def __init__(self, base_url):
        self.api_url = base_url.rstrip('/') + '/api/employees'

    def json_to_emp(self, data):
        emp_type = data.get('type')
        if emp_type == 'Manager':
            emp = Manager(None)
        elif emp_type == 'Director':
            emp = Director(None)
        else:
            emp = Employee(None)

        emp.id = data.get('id')
        ignore = ['id', 'type']

        for k, v in data.items():
            if k not in ignore and hasattr(emp, k):
                setattr(emp, k, v)
        return emp

    def emp_to_dict(self, emp):
        data = {
            'type': emp.__class__.__name__,
            'name': emp.name,
            'age': emp.age,
            'sex': emp.sex,
            'department': emp.department,
            'salary': emp.salary
        }
        if hasattr(emp, 'team_size'):
            data['team_size'] = emp.team_size
        if hasattr(emp, 'assistant'):
            data['assistant'] = emp.assistant
        return data

    def get_employees(self):
        try:
            r = requests.get(self.api_url)
            return [self.json_to_emp(i) for i in r.json()] if r.status_code == 200 else []
        except Exception as e:
            print(f"API Get Employees Error: {e}")
            return []

    def add_employee(self, item):
        data = self.emp_to_dict(item)
        try:
            r = requests.post(self.api_url, json=data)
            r.raise_for_status()
            resp = r.json()
            item.id = resp['id']
            return True
        except Exception as e:
            print(f"API Add Error: {e}")
            return False

    def update_employee(self, item):
        if not item.id:
            return False
        data = self.emp_to_dict(item)
        try:
            r = requests.put(f"{self.api_url}/{item.id}", json=data)
            r.raise_for_status()
            return True
        except Exception as e:
            print(f"API Update Error: {e}")
            return False

    def delete_employee(self, item_id):
        try:
            r = requests.delete(f"{self.api_url}/{item_id}")
            r.raise_for_status()
            return True
        except Exception as e:
            print(f"API Delete Error: {e}")
            return False

    def delete_all_employees(self):
        try:
            requests.delete(self.api_url)
            return True
        except Exception as e:
            print(f"API Delete All Error: {e}")
            return False

    def load_data(self):
        helper = Pickle_Storage()
        employees = helper.load_data()

        if employees:
            self.delete_all_employees()
            for item in employees:
                item.id = None
                self.add_employee(item)
        return employees

    def save_data(self, data):
        helper = Pickle_Storage()
        helper.save_data(data)