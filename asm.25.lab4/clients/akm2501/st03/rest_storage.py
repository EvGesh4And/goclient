import requests
import json

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
                from .person import Person, Worker, Hobby
                from .consoleio import ConsoleIO
                
                console_io = ConsoleIO()
                items = []
                for item_dict in items_data:
                    if item_dict['type'] == 'Person':
                        item = Person.from_dict(item_dict, console_io)
                    elif item_dict['type'] == 'Worker':
                        item = Worker.from_dict(item_dict, console_io)
                    elif item_dict['type'] == 'Hobby':
                        item = Hobby.from_dict(item_dict, console_io)
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
            clear_response = requests.post(f"{self.base_url}/api/clear")
            if clear_response.status_code != 200:
                print("Ошибка очистки данных на сервере")
                return False
            for item in data:
                item_data = item.to_dict()
                response = requests.post(f"{self.base_url}/api/items", 
                                       json=item_data,
                                       headers={'Content-Type': 'application/json'})
                if response.status_code != 201:
                    print(f"Ошибка сохранения элемента: {response.status_code}")
                    return False
            return True
        except Exception as e:
            print(f"Ошибка подключения к серверу: {e}")
            return False
    
    def add_item_rest(self, item_data):
        if not self.initialized:
            print("REST storage not initialized")
            return False
        try:
            print(f"DEBUG: Sending to server: {item_data}")
            response = requests.post(f"{self.base_url}/api/items", 
                                   json=item_data,
                                   headers={'Content-Type': 'application/json'})
            print(f"DEBUG: Server response: {response.status_code} - {response.text}")
            return response.status_code == 201
        except Exception as e:
            print(f"Ошибка подключения к серверу: {e}")
            return False