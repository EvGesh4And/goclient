from flask import render_template

class Container:
    def __init__(self, storage_strategy):
        self.storage_strategy = storage_strategy
    
    def show_all(self):
        items = self.storage_strategy.get_all_items()
        # Используем полный путь
        return render_template('akm2501/st09/book.html', items=items)
    
    def show_form(self, item_type=1):
        from .person import Guest, Coach
        if item_type == 1:
            item = Guest()
        elif item_type == 2:
            item = Coach()
        else:
            return "Неверный тип объекта!"
        return render_template('akm2501/st09/form.html', it=item, item_type=item_type)
    
    def show_edit_form(self, item_id):
        item = self.storage_strategy.get_item(item_id)
        if not item:
            return "Неверный ID объекта!"
        return render_template('akm2501/st09/form.html', it=item, item_id=item_id)
    
    def add_from_form(self):
        from flask import request, redirect, url_for
        
        item_type = int(request.form.get('item_type', 1))
        
        item_data = {
            'type': 'Guest' if item_type == 1 else 'Coach',
            'name': request.form.get('name', ''),
            'age': int(request.form.get('age', '0'))
        }
        
        if item_type == 1:
            item_data['pass_type'] = request.form.get('pass_type', '')
        elif item_type == 2:
            item_data['training_type'] = request.form.get('training_type', '')
        
        if self.storage_strategy.add_item(item_data):
            return redirect(url_for('st0109.index'))
        else:
            return "Ошибка добавления объекта"
    
    def update_from_form(self, item_id):
        from flask import request, redirect, url_for
        
        current_item = self.storage_strategy.get_item(item_id)
        if not current_item:
            return "Объект не найден"
        
        item_data = {
            'name': request.form.get('name', ''),
            'age': int(request.form.get('age', '0'))
        }
        
        if current_item.type == 'Guest':
            pass_type = request.form.get('pass_type', '')
            if pass_type:
                item_data['pass_type'] = pass_type
        elif current_item.type == 'Coach':
            training_type = request.form.get('training_type', '')
            if training_type:
                item_data['training_type'] = training_type
        
        if self.storage_strategy.update_item(item_id, item_data):
            return redirect(url_for('st0109.index'))
        else:
            return "Ошибка обновления объекта"
    
    def delete_item_web(self, item_id):
        from flask import redirect, url_for
        
        if self.storage_strategy.delete_item(item_id):
            return redirect(url_for('st0109.index'))
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