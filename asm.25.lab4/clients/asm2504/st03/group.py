if __name__ != '__main__':
    from .entity import BaseEntity, Soup, MainCourse, Dessert, Drink
    from .console_io import ConsoleIO
    from .pickle_storage import PickleStorage
    from .rest_storage import RestStorage
else:
    from entity import BaseEntity, Soup, MainCourse, Dessert, Drink
    from console_io import ConsoleIO
    from pickle_storage import PickleStorage
    from rest_storage import RestStorage


class Group:
    def __init__(self, storage=None, io_strategy=None):
        # storage может быть PickleStorage или RestStorage
        self.storage = storage or PickleStorage()
        self.io = io_strategy or ConsoleIO()
        self.entities = []

        # Загрузка данных, если хранилище поддерживает load()
        if hasattr(self.storage, "load"):
            try:
                data = self.storage.load()
                self._load_from_storage(data)
            except Exception:
                pass

    # --- Преобразование словарей REST → объекты ---
    def _load_from_storage(self, data):
        """Перевод полученных словарей из REST в объекты."""
        if not data:
            self.entities = []
            return

        if isinstance(data[0], dict):  # это REST-ответ
            self.entities = []
            for d in data:
                dish_type = d.get("type", "MainCourse")
                cls_map = {
                    'Soup': Soup,
                    'MainCourse': MainCourse,
                    'Dessert': Dessert,
                    'Drink': Drink
                }
                cls = cls_map.get(dish_type, MainCourse)
                obj = cls.from_dict(d, self.io)
                self.entities.append(obj)
        else:
            # PickleStorage — сразу список объектов
            self.entities = data

    def _choose_type(self):
        print("Выберите тип блюда:")
        print("  1 - Суп")
        print("  2 - Горячее")
        print("  3 - Десерт")
        print("  4 - Напиток")
        choice = input("Ваш выбор: ").strip()
        if choice == '1':
            return Soup(self.io)
        if choice == '2':
            return MainCourse(self.io)
        if choice == '3':
            return Dessert(self.io)
        if choice == '4':
            return Drink(self.io)
        print("Неверный выбор.")
        return None

    def add_entity(self):
        """Добавление блюда с выбором типа."""
        ent = self._choose_type()
        if ent is None:
            return
        ent.input_fields()
        self.entities.append(ent)

        # REST
        if hasattr(self.storage, "add"):
            r = self.storage.add(ent.to_dict())
            # сохранить id, если REST вернул db_id
            if "id" in r:
                ent.db_id = r["id"]

        print("Блюдо добавлено.")

    def display_list(self):
        """Вывод меню на экран"""
        self.io.display_list(self.entities)

    def load_from_file(self):
        """Чтение из файла или API."""
        data = self.storage.load()
        self._load_from_storage(data)
        print("Данные загружены.")

    def save_to_file(self):
        """Запись в файл или API."""
        if hasattr(self.storage, "save"):
            self.storage.save(self.entities)
            print("Данные сохранены.")
        else:
            print("Это хранилище не поддерживает прямое сохранение.")

    def clear_list(self):
        """Очистка меню."""
        self.entities = []
        if hasattr(self.storage, "clear"):
            self.storage.clear()
        print("Меню очищено.")

    def edit_entity(self, index):
        """Редактирование блюда: выбор конкретного поля."""
        if not (0 <= index < len(self.entities)):
            print("Неверный индекс.")
            return

        ent = self.entities[index]
        
        while True:
            print("\nЧто редактировать?")
            print("1. Название")
            print("2. Цена")
            print("3. Калорийность")
            print("4. Ингредиенты (через запятую)")
            print("0. Назад")
            choice = input("Ваш выбор: ").strip()

            if choice == '0':
                print("Редактирование завершено.")
                break
            elif choice == '1':
                ent.edit_field_by_key("name")
            elif choice == '2':
                ent.edit_field_by_key("price")
            elif choice == '3':
                ent.edit_field_by_key("calories")
            elif choice == '4':
                ent.edit_field_by_key("ingredients")
            else:
                print("Неверный выбор.")
                continue

            print("Поле обновлено.")

        # REST
        if hasattr(self.storage, "update"):
            ent_id = getattr(ent, "db_id", index + 1)
            self.storage.update(ent_id, ent.to_dict())

    def delete_entity(self, index):
        """Удаление блюда по индексу"""
        if not (0 <= index < len(self.entities)):
            print("Неверный индекс.")
            return

        ent = self.entities[index]
        ent_id = getattr(ent, "db_id", index + 1)

        # REST
        if hasattr(self.storage, "delete"):
            self.storage.delete(ent_id)

        del self.entities[index]
        print(f"\"{ent.name}\" удалено из меню")