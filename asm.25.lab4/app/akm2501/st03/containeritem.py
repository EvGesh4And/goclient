from .io_strategies import WebIO

class Container:
    def __init__(self, storage_strategy):
        self.storage_strategy = storage_strategy
        self.web_io = WebIO()
    
    def show_all(self):
        items = self.storage_strategy.get_all_items()
        return self.web_io.render_template('book.html', items=items)
    
    def show_form(self, item_type=1):
        from .person import Person, Worker, Hobby
        if item_type == 1:
            item = Person()
        elif item_type == 2:
            item = Worker()
        elif item_type == 3:
            item = Hobby()
        else:
            return "Неверный тип объекта!"
        return self.web_io.render_template('form.html', it=item, item_type=item_type)
    
    def show_edit_form(self, item_id):
        item = self.storage_strategy.get_item(item_id)
        if not item:
            return "Неверный ID объекта!"
        return self.web_io.render_template('form.html', it=item, item_id=item_id)
    
    def add_from_form(self):
        item_type = int(self.web_io.input('item_type', 1))
        type_map = {1: 'Person', 2: 'Worker', 3: 'Hobby'}
        item_data = {
            'type': type_map.get(item_type, 'Person'),
            'name': self.web_io.input('name', ''),
            'age': int(self.web_io.input('age', '0'))
        }
        if item_type == 2:
            item_data['occupation'] = self.web_io.input('occupation', '')
        elif item_type == 3:
            item_data['hobby'] = self.web_io.input('hobby', '')
        if self.storage_strategy.add_item(item_data):
            return self.web_io.redirect('st0103.index')
        else:
            return "Ошибка добавления объекта"
    
    def update_from_form(self, item_id):
        item_data = {
            'name': self.web_io.input('name', ''),
            'age': int(self.web_io.input('age', '0'))
        }
        
        occupation = self.web_io.input('occupation', '')
        hobby = self.web_io.input('hobby', '')
        
        if occupation:
            item_data['occupation'] = occupation
        if hobby:
            item_data['hobby'] = hobby
        
        print(f"DEBUG: Updating item {item_id} with data: {item_data}")
        
        if self.storage_strategy.update_item(item_id, item_data):
            return self.web_io.redirect('st0103.index')
        else:
            return "Ошибка обновления объекта"
    
    def delete_item_web(self, item_id):
        if self.storage_strategy.delete_item(item_id):
            return self.web_io.redirect('st0103.index')
        else:
            return "Ошибка удаления объекта"
    
    def clear_list(self):
        if self.storage_strategy.clear_all():
            return "Картотека очищена!"
        else:
            return "Ошибка очистки картотеки"
    
    def save_to_file(self):
        success, message = self.storage_strategy.save_to_file()
        return message
    
    def load_from_file(self):
        success, message = self.storage_strategy.load_from_file()
        return message