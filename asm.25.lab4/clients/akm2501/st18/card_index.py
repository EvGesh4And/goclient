from typing import Dict, Type

from app.akm2501.st18.models import Employee, Item, Student


class CardIndex:
    def __init__(self, storage, io):
        self.storage = storage
        self.io = io

        self.__types: Dict[int, Type[Item]] = {
            1: Student,
            2: Employee
        }

    def load(self):
        self.storage.load()

    def store(self):
        max_id, items = self.storage.load()
        self.storage.store(max_id, items)

    def clean(self):
        self.storage.clear()

    def output(self):
        return self.io.output(self.storage.get_items())

    def get_item(self, id):
        return self.io.output_item(self.storage.get(id))

    def edit_item(self, id):
        return self.io.edit_item(self.storage.get(id))

    def process_item(self, id=None, item_type=None):
        if id is None:
            id = self.io.input("id", 0)
            if isinstance(id, str) and id.isdigit():
                id = int(id)
            else:
                id = 0

        item = self.storage.get(id)

        if not item:
            if item_type == 'student':
                item = Student()
            elif item_type == 'employee':
                item = Employee()
            else:
                return self.io.default_output(self)

        item.input(self.io)
        self.storage.add(item) if id == 0 else self.storage.update(item)
        return self.io.default_output(self)

    def delete_item(self, id=None):
        if id is None:
            id = self.io.input("id", 0)
            if isinstance(id, str) and id.isdigit():
                id = int(id)
        self.storage.delete(id)
        return self.io.default_output(self)

    # Методы для консольного интерфейса
    def add(self):
        item = self.__create_item()
        io = self.io
        item.input(io)

        new_id = self.storage.add(item)

        if new_id:
            io.print('Элемент добавлен')
        else:
            io.print('Ошибка добавления элемента')

    def delete(self):
        self.show()

        io = self.io
        io.print('Выберите ID для удаления')

        id_info = io.input('ID')
        id = None

        if id_info.isdigit():
            id = int(id_info)

        items = self.storage.get_items()
        if items.get(id):
            if self.storage.delete(id):
                io.print('Объект успешно удалён')
            else:
                io.print('Ошибка удаления элемента')
        else:
            io.print('Объект с таким ID не найден')

    def show(self) -> None:
        items = self.storage.get_items()
        io = self.io

        if len(items) == 0:
            io.print('Картотека пуста')
        else:
            io.print('---------- ЭЛЕМЕНТЫ ----------')

            for _, item in sorted(items.items()):
                item.output(io)
                io.print('------------------------------')

    def clear(self):
        items = self.storage.get_items()
        io = self.io

        if len(items) == 0:
            io.print('Картотека пуста')
        else:
            if self.storage.clear():
                io.print('Картотека очищена')
            else:
                io.print('Ошибка очистки картотеки')

    def __create_item(self):
        io = self.io
        io.print('Выберите номер типа объекта: ')

        for type_number, item_type in sorted(self.__types.items()):
            io.print(f'{type_number}: {item_type.__name__}')

        user_type_number = int(input())

        item = self.__types[user_type_number]()
        return item
