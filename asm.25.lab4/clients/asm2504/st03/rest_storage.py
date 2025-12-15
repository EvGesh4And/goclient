import os
import requests

class RestStorage:
    def __init__(self):
        base = os.environ.get("LAB4_API_BASE", "http://127.0.0.1:5000/st12/")
        self.BASE_URL = base.rstrip("/") + "/api"
    
    def get_all(self):
        r = requests.get(f"{self.BASE_URL}/dishes")
        r.raise_for_status()
        return r.json()

    def add(self, dish_dict):
        r = requests.post(f"{self.BASE_URL}/dishes", json=dish_dict)
        r.raise_for_status()
        return r.json()

    def update(self, dish_id, dish_dict):
        r = requests.put(f"{self.BASE_URL}/dishes/{dish_id}", json=dish_dict)
        r.raise_for_status()

    def delete(self, dish_id):
        r = requests.delete(f"{self.BASE_URL}/dishes/{dish_id}")
        r.raise_for_status()

    def clear(self):
        r = requests.delete(f"{self.BASE_URL}/dishes")
        r.raise_for_status()

    def save(self, dishes):
        """Очистить и записать заново (для совместимости с ЛР1)"""
        self.clear()
        for dish in dishes:
            self.add(dish.to_dict())

    def load(self):
        """Получить список блюд"""
        data = self.get_all()
        return data