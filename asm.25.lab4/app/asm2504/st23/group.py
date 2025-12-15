import os
from flask import render_template
from .dish import MainDish, Dessert
from .console_io import ConsoleIO
from .flask_io import FlaskIOStrategy


class Group:
    def f(self):
        print("asm2504.st23.group.f()")

    def __init__(self, storage=None, io_strategy=None):
        self.storage = storage
        self.io_strategy = io_strategy or ConsoleIO()

    @property
    def items(self):
        return self.storage.get_items()

    @property
    def current_filename(self):
        return "menu.pkl"

    def add(self, dish_type=None, form_data=None):
        """Добавление блюда"""
        if isinstance(self.io_strategy, ConsoleIO):
            return self._add_console()
        elif isinstance(self.io_strategy, FlaskIOStrategy):
            return self._add_web(dish_type, form_data)
        return False

    def _add_console(self):
        print("\nВыберите тип блюда:")
        print("1. Основное блюдо")
        print("2. Десерт")
        choice = input("\nВаш выбор: ")

        if choice == "1":
            dish = MainDish(self.io_strategy)
        elif choice == "2":
            dish = Dessert(self.io_strategy)
        else:
            print("Неверный выбор")
            return False

        dish.input()
        return self.storage.add_item(dish)

    def _add_web(self, dish_type, form_data):
        if dish_type == "main":
            dish = MainDish(self.io_strategy)
        elif dish_type == "dessert":
            dish = Dessert(self.io_strategy)
        else:
            return False

        errors = self.io_strategy.process_form_data(dish, form_data)
        if errors:
            return False

        return self.storage.add_item(dish)

    def edit(self, index=None, form_data=None):
        if isinstance(self.io_strategy, ConsoleIO):
            return self._edit_console()
        elif isinstance(self.io_strategy, FlaskIOStrategy):
            return self._edit_web(index, form_data)
        return False

    def _edit_console(self):
        self.show_all()
        if not self.items:
            return False

        try:
            idx = int(input("\nВведите номер блюда для редактирования: ")) - 1
            self.items[idx].edit()
            return self.storage.update_item(idx, self.items[idx])
        except (ValueError, IndexError):
            print("Неверный номер.")
            return False

    def _edit_web(self, index, form_data):
        dish_dict = self.storage.get_item(index)
        if not dish_dict:
            return False

        if dish_dict['dish_type'] == 'main':
            dish = MainDish(self.io_strategy)
        else:  # dessert
            dish = Dessert(self.io_strategy)

        dish.name = dish_dict['name']
        dish.cuisine = dish_dict['cuisine']
        dish.calories = dish_dict['calories']

        if hasattr(dish, 'garnish'):
            dish.garnish = dish_dict.get('garnish', '')
        if hasattr(dish, 'sweetness'):
            dish.sweetness = dish_dict.get('sweetness', 5)

        errors = self.io_strategy.process_form_data(dish, form_data)

        if not errors:
            return self.storage.update_item(index, dish)
        return False

    def delete(self, index=None):
        if isinstance(self.io_strategy, ConsoleIO):
            return self._delete_console()
        elif isinstance(self.io_strategy, FlaskIOStrategy):
            return self._delete_web(index)
        return False

    def _delete_console(self):
        self.show_all()
        if not self.items:
            return False

        try:
            idx = int(input("\nВведите номер блюда для удаления: ")) - 1
            removed = self.items[idx]
            if self.storage.delete_item(idx):
                print(f"Удалено блюдо: {removed.name}")
                return True
        except (ValueError, IndexError):
            print("Неверный номер.")
        return False

    def _delete_web(self, index):
        if index is not None and 0 <= index < len(self.items):
            return self.storage.delete_item(index)
        return False

    def show_all(self):
        if isinstance(self.io_strategy, ConsoleIO):
            self._show_all_console()
        elif isinstance(self.io_strategy, FlaskIOStrategy):
            return self._show_all_web()

    def _show_all_console(self):
        if not self.items:
            print("Список пуст.")
            return

        for i, item in enumerate(self.items, 1):
            print(f"\nБлюдо {i}:")
            item.output()

    def _show_all_web(self):
        dishes_data = []
        items = self.storage.get_items()  # Теперь это словари

        for i, dish_dict in enumerate(items):
            if dish_dict['dish_type'] == 'main':
                dish = MainDish(self.io_strategy)
            else:
                dish = Dessert(self.io_strategy)

            dish.name = dish_dict['name']
            dish.cuisine = dish_dict['cuisine']
            dish.calories = dish_dict['calories']

            if 'garnish' in dish_dict and dish_dict['garnish']:
                dish.garnish = dish_dict['garnish']
            if 'sweetness' in dish_dict and dish_dict['sweetness']:
                dish.sweetness = dish_dict['sweetness']

            dish_data = self.io_strategy.prepare_for_display(dish, i)
            if dish_data:
                dishes_data.append(dish_data)

        return dishes_data

    def clear(self):
        self.storage.clear()
        if isinstance(self.io_strategy, ConsoleIO):
            print("Список очищен.")

    def prepare_add_form(self):
        if isinstance(self.io_strategy, FlaskIOStrategy):
            return render_template('asm2504/st23/add_dish.html',
                                   title='Добавить блюдо')
        return None

    def prepare_edit_form(self, index):
        if isinstance(self.io_strategy, FlaskIOStrategy):
            dish_dict = self.storage.get_item(index)
            if not dish_dict:
                return None

            if dish_dict['dish_type'] == 'main':
                dish = MainDish(self.io_strategy)
            else:
                dish = Dessert(self.io_strategy)
            dish.name = dish_dict['name']
            dish.cuisine = dish_dict['cuisine']
            dish.calories = dish_dict['calories']

            if hasattr(dish, 'garnish'):
                dish.garnish = dish_dict.get('garnish', '')
            if hasattr(dish, 'sweetness'):
                dish.sweetness = dish_dict.get('sweetness', 5)

            return render_template('asm2504/st23/edit_dish.html',
                                   dish=dish,
                                   index=index,
                                   dish_type=dish_dict['dish_type'],
                                   title='Редактировать блюдо')
        return None

    def prepare_save_form(self):
        if isinstance(self.io_strategy, FlaskIOStrategy):
            available_files = self.storage.get_available_files()
            return render_template('asm2504/st23/save_data.html',
                                   available_files=available_files,
                                   current_file=self.current_filename,
                                   title='Сохранить в файл')
        return None

    def prepare_load_form(self):
        if isinstance(self.io_strategy, FlaskIOStrategy):
            available_files = self.storage.get_available_files()
            return render_template('asm2504/st23/load_data.html',
                                   available_files=available_files,
                                   title='Загрузить из файла')
        return None

    def load(self, filename=None):
        return self.storage.load(filename)

    def save(self, filename=None):
        return self.storage.save(filename)

    def get_available_files(self):
        return self.storage.get_available_files()