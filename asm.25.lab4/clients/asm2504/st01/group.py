import requests

if __name__ != '__main__':
    from .entity import BaseEntity, Student, Starosta
    from .console_io import ConsoleIO
    from .pickle_storage import PickleStorage
    from .rest_storage import RestStorage
else:
    from entity import BaseEntity, Student, Starosta
    from console_io import ConsoleIO
    from pickle_storage import PickleStorage
    from rest_storage import RestStorage

class Group:
    def __init__(self, storage_type='pickle', io_strategy=None):
        self.entities = []
        if storage_type == 'pickle':
            self.storage = PickleStorage()
        elif storage_type == 'rest':
            self.storage = RestStorage()
        else:
            raise ValueError("Unknown storage type")
        self.io = io_strategy or ConsoleIO()
        self.entity_from_dict = BaseEntity.from_dict

    def add_entity(self):
        """Добавление элемента с выбором типа."""
        print("Выберите тип: 1 - Студент, 2 - Староста")
        choice = input("Ваш выбор: ")
        if choice == '1':
            ent = Student(self.io)
        elif choice == '2':
            ent = Starosta(self.io)
        else:
            print("Неверный выбор.")
            return
        ent.input_fields()
        # Use storage API if available (keeps behavior consistent) and refresh local list
        if isinstance(self.storage, RestStorage):
            ok = self.storage.add_entity(ent)
            if not ok:
                print("Ошибка добавления на сервер.")
                return
            # refresh authoritative list from API (to get assigned ids)
            self._refresh_from_api()
        else:
            self.entities.append(ent)
        print("Карточка добавлена.")

    def display_list(self):
        """Вывод списка на экран."""
        self.io.display_list(self.entities)

    def load_from_file(self):
        """Чтение из файла."""
        self.entities = self.storage.load(self.entity_from_dict)

    def save_to_file(self):
        """Запись в файл."""
        self.storage.save(self.entities)

    def clear_list(self):
        """Очистка списка."""
        if isinstance(self.storage, RestStorage):
            ok = self.storage.delete_all_entities()
            if not ok:
                print("Ошибка очистки на сервере.")
                return
        self.entities = []
        print("Список очищен.")

    def edit_entity_by_id(self, id):
        """Редактирование карточек по ID."""
        for ent in self.entities:
            if ent.id == id:
                print(f"Редактирование карточки ID {id}")
                ent.input_fields()
                if isinstance(self.storage, RestStorage):
                    ok = self.storage.update_entity(ent)
                    if not ok:
                        print("Ошибка обновления на сервере.")
                        return
                    # refresh local copy
                    self._refresh_from_api()
                print("Карточка обновлена.")
                return
        print("Карточка с таким ID не найдена.")

    def delete_entity_by_id(self, id):
        """Удаление по ID."""
        for i, ent in enumerate(self.entities):
            if ent.id == id:
                if isinstance(self.storage, RestStorage):
                    ok = self.storage.delete_entity(id)
                    if not ok:
                        print("Ошибка удаления на сервере.")
                        return
                    # refresh authoritative list
                    self._refresh_from_api()
                else:
                    del self.entities[i]
                print("Карточка удалена.")
                return
        print("Карточка с таким ID не найдена.")

    # --- additional helpers for file <-> storage operations ---
    def export_to_file(self, filename='cardex.pkl'):
        """Save current in-memory list to a local pickle file (uses PickleStorage)."""
        helper = PickleStorage(filename)
        helper.save(self.entities)

    def import_from_file(self, filename='cardex.pkl'):
        """Load entities from a local pickle file into memory (does not push to remote)."""
        helper = PickleStorage(filename)
        loaded = helper.load(self.entity_from_dict)
        if loaded:
            self.entities = loaded
            print(f"Загружено {len(loaded)} записей из файла.")
            # automatically push imported data to API when using REST
            if isinstance(self.storage, RestStorage):
                ok = self.storage.save_data(self.entities)
                if ok:
                    print('Импортированные данные отправлены на API и синхронизированы.')
                    self._refresh_from_api()
                else:
                    print('Не удалось отправить импортированные данные на API.')
        else:
            print("Файл пуст или не найден.")
        return self.entities

    def push_to_api(self):
        """If current storage is REST, replace remote data with in-memory entities."""
        if isinstance(self.storage, RestStorage):
            ok = self.storage.save_data(self.entities)
            if ok:
                print("Данные отправлены на API.")
            else:
                print("Не удалось отправить данные на API.")
        else:
            print("Текущее хранилище не является REST API.")

    def pull_from_api(self):
        """If current storage is REST, load data from API into memory."""
        if isinstance(self.storage, RestStorage):
            loaded = self.storage.load_data()
            if loaded:
                self.entities = loaded
                print(f"Загружено {len(loaded)} записей с API.")
            else:
                print("Не удалось загрузить данные с API или список пуст.")
        else:
            print("Текущее хранилище не является REST API.")

    def _refresh_from_api(self):
        """Internal helper: refresh local entities from API if REST storage is in use."""
        if isinstance(self.storage, RestStorage):
            try:
                loaded = self.storage.load_data()
                if loaded is not None:
                    self.entities = loaded
            except Exception as e:
                print(f"Ошибка при обновлении данных из API: {e}")
