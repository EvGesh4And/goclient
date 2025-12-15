from .io_strategies import WebIO

class Container:
    def __init__(self, storage_strategy):
        self.storage_strategy = storage_strategy
        self.web_io = WebIO()
    
    def show_all(self):
        items = self.storage_strategy.get_all_items()
        return self.web_io.render_template('medical_list.html', items=items)
    
    def show_form(self, staff_type):
        from .medical import Nurse, Doctor
        
        if staff_type == 'nurse':
            item = Nurse()
        elif staff_type == 'doctor':
            item = Doctor()
        else:
            return "Неверный тип сотрудника!"
        
        return self.web_io.render_template('medical_form.html', item=item, staff_type=staff_type)
    
    def show_edit_form(self, item_id):
        item = self.storage_strategy.get_item(item_id)
        if not item:
            return "Сотрудник не найден!"
        
        return self.web_io.render_template('medical_form.html', item=item, item_id=item_id)
    
    def add_from_form(self):
        staff_type = self.web_io.input('staff_type', 'nurse')
        
        item_data = {
            'type': staff_type,
            'name': self.web_io.input('name', ''),
            'specialty': self.web_io.input('specialty', ''),
            'category': self.web_io.input('category', ''),
            'schedule': self.web_io.input('schedule', ''),
            'staff_type': staff_type
        }
        
        if staff_type == 'nurse':
            item_data['procedure_room'] = self.web_io.input('procedure_room', '')
            item_data['shift'] = self.web_io.input('shift', '')
        elif staff_type == 'doctor':
            item_data['license'] = self.web_io.input('license', '')
            item_data['specialization'] = self.web_io.input('specialization', '')
        
        if self.storage_strategy.add_item(item_data):
            return self.web_io.redirect('st0120.index')
        else:
            return "Ошибка добавления сотрудника"
    
    def update_from_form(self, item_id):
        existing_item = self.storage_strategy.get_item(item_id)
        if not existing_item:
            return "Сотрудник не найден!"
        
        updated_data = {
            'name': self.web_io.input('name', existing_item.name),
            'specialty': self.web_io.input('specialty', existing_item.specialty),
            'category': self.web_io.input('category', existing_item.category),
            'schedule': self.web_io.input('schedule', existing_item.schedule),
        }
        
        if hasattr(existing_item, 'procedure_room'):
            updated_data['procedure_room'] = self.web_io.input('procedure_room', existing_item.procedure_room)
        if hasattr(existing_item, 'shift'):
            updated_data['shift'] = self.web_io.input('shift', existing_item.shift)
        if hasattr(existing_item, 'license'):
            updated_data['license'] = self.web_io.input('license', existing_item.license)
        if hasattr(existing_item, 'specialization'):
            updated_data['specialization'] = self.web_io.input('specialization', existing_item.specialization)
        
        if self.storage_strategy.update_item(item_id, updated_data):
            return self.web_io.redirect('st0120.index')
        else:
            return "Ошибка обновления сотрудника"
    
    def delete_item_web(self, item_id):
        if self.storage_strategy.delete_item(item_id):
            return self.web_io.redirect('st0120.index')
        else:
            return "Ошибка удаления сотрудника"
    
    def save_to_file(self):
        success, message = self.storage_strategy.save_to_file()
        return message
    
    def load_from_file(self):
        success, message = self.storage_strategy.load_from_file()
        return message