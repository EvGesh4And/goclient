from .dish import MainDish, Dessert
from .console_io import ConsoleIO
from .pickle_storage import PickleStorage
from .rest_io import RestIO
from .rest_storage import RestStorage


class Group:
    def f(self):
        print("asm2504.st23.group.f()")

    def __init__(self, use_rest=False):
        self.items = []
        self.use_rest = use_rest

        if use_rest:
            self.io = RestIO()
            self.storage = RestStorage()
        else:
            self.io = ConsoleIO()
            self.storage = PickleStorage()

    def _dish_to_dict(self, dish):
        data = {
            'name': dish.name,
            'cuisine': dish.cuisine,
            'calories': dish.calories
        }

        if isinstance(dish, MainDish):
            data['dish_type'] = 'main'
            data['garnish'] = dish.garnish
        else:
            data['dish_type'] = 'dessert'
            data['sweetness'] = dish.sweetness

        return data

    def _dict_to_dish(self, data):
        dish_type = data.get('dish_type', 'main')

        if dish_type == 'main':
            dish = MainDish(self.io)
            dish.garnish = data.get('garnish', '')
        else:
            dish = Dessert(self.io)
            dish.sweetness = int(data.get('sweetness', 5))

        dish.name = data.get('name', '')
        dish.cuisine = data.get('cuisine', '')
        dish.calories = int(data.get('calories', 0))

        return dish

    def add(self):
        print("\nВыберите тип блюда:")
        print("1. Основное блюдо")
        print("2. Десерт")
        choice = input("\nВаш выбор: ")

        if choice == "1":
            dish = MainDish(self.io)
            dish_type = "main"
        elif choice == "2":
            dish = Dessert(self.io)
            dish_type = "dessert"
        else:
            print("Неверный выбор")
            return

        dish.input()

        if self.use_rest:
            dish_data = self._dish_to_dict(dish)
            if self.storage.add_dish(dish_data):
                print("Блюдо добавлено на сервер.")
            else:
                print("Ошибка добавления.")
        else:
            self.items.append(dish)
            print("Блюдо добавлено.")

    def show_all(self):
        if self.use_rest:
            dishes = self.storage.get_all_dishes()
            if not dishes:
                print("Список пуст.")
                return

            for i, data in enumerate(dishes, 1):
                print(f"\nБлюдо {i}:")
                dish = self._dict_to_dish(data)
                dish.output()
                print(f"Тип: {'Основное блюдо' if data.get('dish_type') == 'main' else 'Десерт'}")
        else:
            if not self.items:
                print("Список пуст.")
                return

            for i, dish in enumerate(self.items, 1):
                print(f"\nБлюдо {i}:")
                dish.output()

    def edit(self):
        if not self.use_rest:
            if not self.items:
                print("Список пуст.")
                return

            self.show_all()

            try:
                idx = int(input("\nВведите номер блюда для редактирования: ")) - 1
                self.items[idx].edit()
            except (ValueError, IndexError):
                print("Неверный номер.")
            return

        dishes = self.storage.get_all_dishes()
        if not dishes:
            print("Список пуст.")
            return

        for i, data in enumerate(dishes, 1):
            print(f"\nБлюдо {i}: {data.get('name')}")

        try:
            idx = int(input("\nВведите номер блюда: ")) - 1
            if idx < 0 or idx >= len(dishes):
                print("Неверный номер.")
                return

            dish = self._dict_to_dish(dishes[idx])
            dish.edit()

            dish_data = self._dish_to_dict(dish)
            if self.storage.edit_dish(idx, dish_data):
                print("Блюдо обновлено.")
            else:
                print("Ошибка обновления.")
        except (ValueError, IndexError):
            print("Неверный номер.")

    def delete(self):
        if self.use_rest:
            dishes = self.storage.get_all_dishes()
            if not dishes:
                print("Список пуст.")
                return

            for i, data in enumerate(dishes, 1):
                print(f"\nБлюдо {i}: {data.get('name')}")

            try:
                idx = int(input("\nВведите номер блюда: ")) - 1
                if self.storage.delete_dish(idx):
                    print("Блюдо удалено.")
                else:
                    print("Ошибка удаления.")
            except (ValueError, IndexError):
                print("Неверный номер.")
        else:
            if not self.items:
                print("Список пуст.")
                return

            self.show_all()

            try:
                idx = int(input("\nВведите номер блюда: ")) - 1
                removed = self.items.pop(idx)
                print(f"Удалено: {removed.name}")
            except (ValueError, IndexError):
                print("Неверный номер.")

    def clear(self):
        if self.use_rest:
            if input("Очистить все? (y/n): ").lower() == 'y':
                if self.storage.clear_dishes():
                    print("Список очищен.")
                else:
                    print("Ошибка очистки.")
        else:
            self.items = []
            print("Список очищен.")

    def save(self):
        filename = input("Имя файла: ").strip() or "menu.pkl"

        if self.use_rest:
            if self.storage.save_file(filename):
                print(f"Сохранено в {filename}")
            else:
                print("Ошибка сохранения.")
        else:
            self.storage.save(filename, self.items)
            print(f"Сохранено в {filename}")

    def load(self):
        if self.use_rest:
            files = self.storage.get_files()
            if files:
                print("Доступные файлы:")
                for f in files:
                    print(f"  - {f}")

            filename = input("Имя файла: ").strip() or "menu.pkl"

            if self.storage.load_file(filename):
                print(f"Загружено из {filename}")
            else:
                print("Ошибка загрузки.")
        else:
            filename = input("Имя файла: ").strip() or "menu.pkl"
            try:
                self.items = self.storage.load(filename)
                print(f"Загружено из {filename}")
            except FileNotFoundError:
                print("Файл не найден.")