from .person import Person, Worker, Hobby

class Container:
    def __init__(self, storage_strategy, use_rest=False):
        self.items = []
        self.storage_strategy = storage_strategy
        self.use_rest = use_rest
    
    def add_item(self, item_type, io_strategy):
        if item_type == 1:
            item = Person()
        elif item_type == 2:
            item = Worker()
        elif item_type == 3:
            item = Hobby()
        else:
            print("Неверный тип объекта!")
            return
        
        item.set_io_strategy(io_strategy)
        
        print("\nВведите данные:")
        item.input_fields()
        
        if self.use_rest and hasattr(self.storage_strategy, 'add_item_rest'):
            item_data = {
                'type': item.type,
                'name': item.name,
                'age': item.age
            }
            if hasattr(item, 'occupation'):
                item_data['occupation'] = item.occupation
            if hasattr(item, 'hobby'):
                item_data['hobby'] = item.hobby
            
            if self.storage_strategy.add_item_rest(item_data):
                self.items = self.storage_strategy.read_from_file(None)
                print("Объект успешно добавлен на сервер!")
            else:
                print("Ошибка добавления объекта на сервер!")
        else:
            item.id = len(self.items)
            self.items.append(item)
            print("Объект успешно добавлен!")
    
    def display_list(self, io_strategy):
        if not self.items:
            io_strategy.output("Картотека пуста")
            return
        
        io_strategy.output(f"\nВсего записей: {len(self.items)}")
        for i, item in enumerate(self.items, 1):
            io_strategy.output(f"\n--- Запись {i} ---")
            item.output_fields()
    
    def read_from_file(self, filename):
        loaded_items = self.storage_strategy.read_from_file(filename)
        if loaded_items is not None:
            self.items = loaded_items
            if self.use_rest:
                print(f"Загружено {len(self.items)} записей с сервера")
            else:
                print(f"Загружено {len(self.items)} записей из файла {filename}")
    
    def write_to_file(self, filename):
        if self.storage_strategy.write_to_file(self.items, filename):
            if self.use_rest:
                print(f"Сохранено {len(self.items)} записей на сервер")
            else:
                print(f"Сохранено {len(self.items)} записей в файл {filename}")
    
    def sync_with_server(self):
        if hasattr(self.storage_strategy, 'write_to_file'):
            self.write_to_file(None)
    
    def clear_list(self):
        if self.use_rest:
        # Используем write_to_file с пустым списком для очистки
            self.items.clear()
            if self.storage_strategy.write_to_file(self.items, None):
                print("Данные очищены на сервере и локально!")
            else:
                print("Ошибка очистки данных на сервере!")
        else:
            self.items.clear()
            print("Локальная картотека очищена!")