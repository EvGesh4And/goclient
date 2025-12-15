import pickle
import os

class PickleStorage:
    def __init__(self, filename):
        self.filename = filename
        self.items = []
        self.max_id = 0
    
    def load_from_file(self):
        try:
            if os.path.exists(self.filename):
                with open(self.filename, 'rb') as file:
                    data = pickle.load(file)
                    self.items = data.get('items', [])
                    self.max_id = data.get('max_id', 0)
                return True, f"Загружено {len(self.items)} медицинских записей"
            return False, "Файл не существует"
        except Exception as e:
            return False, f"Ошибка загрузки: {e}"
    
    def save_to_file(self):
        try:
            data = {'items': self.items, 'max_id': self.max_id}
            with open(self.filename, 'wb') as file:
                pickle.dump(data, file)
            return True, f"Сохранено {len(self.items)} медицинских записей"
        except Exception as e:
            return False, f"Ошибка сохранения: {e}"
    
    def get_all_items(self):
        return self.items
    
    def get_item(self, item_id):
        for item in self.items:
            if item.id == item_id:
                return item
        return None
    
    def add_item(self, item_data):
        try:
            if 'staff_type' in item_data and 'type' not in item_data:
                return self._add_item_web(item_data)
            else:
                return self._add_item_api(item_data)
        except Exception as e:
            print(f"Error adding item: {e}")
            return False
    
    def update_item(self, item_id, item_data):
        try:
            if 'staff_type' in item_data and 'type' not in item_data:
                return self._update_item_web(item_id, item_data)
            else:
                return self._update_item_api(item_id, item_data)
        except Exception as e:
            print(f"Error updating item {item_id}: {e}")
            return False
    
    def delete_item(self, item_id):
        for i, item in enumerate(self.items):
            if item.id == item_id:
                del self.items[i]
                return True
        return False
    
    def clear_all(self):
        self.items = []
        self.max_id = 0
        return True
    
    def _add_item_web(self, item_data):
        from .medical import Nurse, Doctor
        
        staff_type = item_data.get('staff_type', 'nurse')
        
        if staff_type == 'nurse':
            item = Nurse()
        elif staff_type == 'doctor':
            item = Doctor()
        else:
            return False
        
        item.id = self.max_id
        item.name = item_data.get('name', '')
        item.specialty = item_data.get('specialty', '')
        item.category = item_data.get('category', '')
        item.schedule = item_data.get('schedule', '')
        item.staff_type = staff_type
        
        if staff_type == 'nurse':
            item.procedure_room = item_data.get('procedure_room', '')
            item.shift = item_data.get('shift', '')
        elif staff_type == 'doctor':
            item.license = item_data.get('license', '')
            item.specialization = item_data.get('specialization', '')
        
        self.items.append(item)
        self.max_id += 1
        return True
    
    def _update_item_web(self, item_id, item_data):
        item = self.get_item(item_id)
        if not item:
            return False
        
        item.name = item_data.get('name', item.name)
        item.specialty = item_data.get('specialty', item.specialty)
        item.category = item_data.get('category', item.category)
        item.schedule = item_data.get('schedule', item.schedule)
        
        if hasattr(item, 'procedure_room'):
            item.procedure_room = item_data.get('procedure_room', item.procedure_room)
        if hasattr(item, 'shift'):
            item.shift = item_data.get('shift', item.shift)
        if hasattr(item, 'license'):
            item.license = item_data.get('license', item.license)
        if hasattr(item, 'specialization'):
            item.specialization = item_data.get('specialization', item.specialization)
        
        return True
    
    def _add_item_api(self, item_data):
        from .medical import MedicalItem
        
        item = MedicalItem.from_dict(item_data)
        item.id = self.max_id
        self.items.append(item)
        self.max_id += 1
        return True
    
    def _update_item_api(self, item_id, item_data):
        from .medical import MedicalItem
        
        for i, existing_item in enumerate(self.items):
            if existing_item.id == item_id:
                updated_item = MedicalItem.from_dict(item_data)
                updated_item.id = item_id
                self.items[i] = updated_item
                return True
        return False