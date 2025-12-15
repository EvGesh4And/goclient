import requests
import json
from .visitor import Guest, Coach

class RESTStorage:
    def __init__(self):
        self.base_url = None
        self.initialized = False
    
    def initialize(self, base_url):
        self.base_url = base_url
        self.initialized = True
    
    def read_from_file(self, filename):
        if not self.initialized:
            print("REST storage not initialized")
            return []
        try:
            response = requests.get(f"{self.base_url}/api/items")
            if response.status_code == 200:
                items_data = response.json()
                from .consoleio import ConsoleIO
                
                console_io = ConsoleIO()
                items = []
                for item_dict in items_data:
                    if item_dict['type'] == 'Guest':
                        item = Guest.from_dict(item_dict, console_io)
                    elif item_dict['type'] == 'Coach':
                        item = Coach.from_dict(item_dict, console_io)
                    else:
                        continue
                    items.append(item)
                return items
            else:
                print(f"Ошибка загрузки данных: {response.status_code}")
                return []
        except Exception as e:
            print(f"Ошибка подключения к серверу: {e}")
            return []
    
    def write_to_file(self, data, filename):
        if not self.initialized:
            print("REST storage not initialized")
            return False
        try:
            items_data = []
            for item in data:
                items_data.append(item.to_dict())
            
            response = requests.post(f"{self.base_url}/api/items/replace", 
                                   json=items_data,
                                   headers={'Content-Type': 'application/json'})
            
            if response.status_code == 200:
                return True
            else:
                print(f"Ошибка сохранения данных: {response.status_code}")
                return False
        except Exception as e:
            print(f"Ошибка подключения к серверу: {e}")
            return False
    
    def add_item_rest(self, item_data):
        if not self.initialized:
            print("REST storage not initialized")
            return False
        try:
            response = requests.post(f"{self.base_url}/api/items", 
                                   json=item_data,
                                   headers={'Content-Type': 'application/json'})
            return response.status_code == 201
        except Exception as e:
            print(f"Ошибка подключения к серверу: {e}")
            return False