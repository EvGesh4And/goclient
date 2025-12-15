import pickle
import os

class PickleStorage:
    def __init__(self, filename):
        self.filename = filename
        self.items_data = []
        self.max_id = 0
    
    def load_from_file(self):
        try:
            if os.path.exists(self.filename):
                with open(self.filename, 'rb') as file:
                    data = pickle.load(file)
                    self.items_data = data.get('items_data', [])
                    self.max_id = data.get('max_id', 0)
                return True, f"Загружено {len(self.items_data)} записей из Pickle"
            return False, "Файл Pickle не существует"
        except Exception as e:
            return False, f"Ошибка загрузки из Pickle: {e}"
    
    def save_to_file(self):
        try:
            data = {'items_data': self.items_data, 'max_id': self.max_id}
            with open(self.filename, 'wb') as file:
                pickle.dump(data, file)
            return True, f"Сохранено {len(self.items_data)} записей в Pickle"
        except Exception as e:
            return False, f"Ошибка сохранения в Pickle: {e}"
    
    def get_all_items(self):
        from .person import Person, Worker, Hobby
        items = []
        for item_data in self.items_data:
            if item_data['type'] == 'Person':
                item = Person.from_dict(item_data)
            elif item_data['type'] == 'Worker':
                item = Worker.from_dict(item_data)
            elif item_data['type'] == 'Hobby':
                item = Hobby.from_dict(item_data)
            else:
                continue
            items.append(item)
        return items
    
    def get_item(self, item_id):
        for item_data in self.items_data:
            if item_data.get('id') == item_id:
                from .person import Person, Worker, Hobby
                if item_data['type'] == 'Person':
                    return Person.from_dict(item_data)
                elif item_data['type'] == 'Worker':
                    return Worker.from_dict(item_data)
                elif item_data['type'] == 'Hobby':
                    return Hobby.from_dict(item_data)
        return None
    
    def add_item(self, item_data):
        try:
            item_data['id'] = self.max_id
            self.items_data.append(item_data)
            self.max_id += 1
            return True
        except Exception as e:
            print(f"DEBUG: Exception in add_item: {e}")
            return False
    
    def update_item(self, item_id, item_data):
        for i, existing_data in enumerate(self.items_data):
            if existing_data.get('id') == item_id:
                for key, value in item_data.items():
                    self.items_data[i][key] = value
                return True
        return False
    
    def delete_item(self, item_id):
        for i, item_data in enumerate(self.items_data):
            if item_data.get('id') == item_id:
                del self.items_data[i]
                return True
        return False
    
    def clear_all(self):
        self.items_data = []
        self.max_id = 0
        return True