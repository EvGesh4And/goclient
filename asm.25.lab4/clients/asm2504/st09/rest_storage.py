import os
import requests

class RestStorage:
    def __init__(self):
        base = os.environ.get("LAB4_API_BASE", "http://127.0.0.1:5000/st8/")
        self.BASE_URL = base.rstrip("/") + "/api"
    
    def get_all(self):
        r = requests.get(f"{self.BASE_URL}/employees")
        r.raise_for_status()
        return r.json()

    def add(self, emp_dict):
        r = requests.post(f"{self.BASE_URL}/employees", json=emp_dict)
        r.raise_for_status()
        return r.json()

    def update(self, emp_id, emp_dict):
        r = requests.put(f"{self.BASE_URL}/employees/{emp_id}", json=emp_dict)
        r.raise_for_status()

    def delete(self, emp_id):
        r = requests.delete(f"{self.BASE_URL}/employees/{emp_id}")
        r.raise_for_status()

    def clear(self):
        r = requests.delete(f"{self.BASE_URL}/employees")
        r.raise_for_status()

    def save(self, employees):
        """Очистить и записать заново (для совместимости с ЛР1)"""
        self.clear()
        for emp in employees:
            self.add(emp.to_dict())

    def load(self):
        """Получить список сотрудников"""
        data = self.get_all()
        return data
