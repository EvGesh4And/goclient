from typing import Optional, Tuple

from .director import Director
from .employee import Employee
from .manager import Manager
from .worker import Worker

TYPE_TITLES = {
    "Worker": "Сотрудник",
    "Manager": "Менеджер",
    "Director": "Директор",
}


class GroupContainer:
    def __init__(self, io, storage):
        self.io = io
        self.storage = storage
        self.types = {
            "1": Worker,
            "2": Manager,
            "3": Director,
        }

    def set_storage(self, storage):
        self.storage = storage
        print(f"Текущее хранилище: {self._storage_name()}")

    def _storage_name(self) -> str:
        return getattr(self.storage, "name", self.storage.__class__.__name__)

    def get_storage_name(self) -> str:
        return self._storage_name()

    def _type_title(self, obj: Employee) -> str:
        return TYPE_TITLES.get(obj.__class__.__name__, obj.__class__.__name__)

    def _bind_io(self, obj: Employee) -> Employee:
        obj.io = self.io
        return obj

    def _load_items(self):
        try:
            return self.storage.list_items()
        except Exception as exc:
            print(f"Ошибка: не удалось получить данные ({exc})")
            return []

    def _choose_type(self) -> Optional[type]:
        print("Тип объекта: 1) Сотрудник, 2) Менеджер, 3) Директор")
        choice = input("Ваш выбор (1/2/3): ").strip()
        cls = self.types.get(choice)
        if cls is None:
            print("Нет такого типа.")
        return cls

    def _select_item(self) -> Optional[Tuple[int, Employee]]:
        items = self._load_items()
        if not items:
            print("Список пуст.")
            return None

        for i, (item_id, obj) in enumerate(items, 1):
            print(f"[{i}] ID={item_id} • {self._type_title(obj)}")
            self._bind_io(obj).print_fields()
            print("-" * 20)

        try:
            raw = input("Номер в списке: ")
            idx = int(raw) - 1
        except Exception:
            print("Неверный номер.")
            return None

        if idx < 0 or idx >= len(items):
            print("Неверный диапазон.")
            return None

        item_id, obj = items[idx]
        try:
            fresh = self.storage.get(item_id)
            if fresh is not None:
                obj = fresh
        except Exception:
            pass

        return item_id, obj

    def add_item(self):
        cls = self._choose_type()
        if cls is None:
            return

        obj = cls(io=self.io)
        print("Введите поля объекта:")
        obj.input_fields()

        try:
            new_id = self.storage.add(obj)
            print(f"Запись добавлена. ID={new_id}")
        except Exception as exc:
            print(f"Ошибка: не удалось добавить объект ({exc})")

    def list_items(self):
        items = self._load_items()
        if not items:
            print("Список пуст.")
            return

        print(f"Хранилище: {self._storage_name()}")
        for i, (item_id, obj) in enumerate(items, 1):
            print(f"[{i}] ID={item_id} • {self._type_title(obj)}")
            self._bind_io(obj).print_fields()
            print("-" * 20)

    def edit_item(self):
        selected = self._select_item()
        if not selected:
            return

        item_id, obj = selected
        fields = list(obj.FIELDS.keys())
        label_fn = getattr(self.io, "_label", lambda name: name)
        readable = [label_fn(field) for field in fields]
        print("Доступные поля: " + ", ".join(readable))
        field_input = input("Поле для редактирования: ").strip()
        labels_map = {label_fn(field): field for field in fields}
        labels_map.update({field: field for field in fields})
        field = labels_map.get(field_input)
        if field not in obj.FIELDS:
            print("Нет такого поля.")
            return

        self.io.read_field(obj, field)
        try:
            if self.storage.update(item_id, obj):
                print("Запись изменена.")
            else:
                print("Не удалось изменить запись.")
        except Exception as exc:
            print(f"Ошибка при обновлении: {exc}")

    def remove_item(self):
        selected = self._select_item()
        if not selected:
            return

        item_id, obj = selected
        try:
            if self.storage.remove(item_id):
                print(f"Запись удалена: {self._type_title(obj)} (ID={item_id})")
            else:
                print("Не найдено в хранилище.")
        except Exception as exc:
            print(f"Ошибка при удалении: {exc}")

    def clear(self):
        try:
            removed = self.storage.clear()
            print(f"Хранилище очищено. Удалено записей: {removed}")
        except Exception as exc:
            print(f"Ошибка: не удалось очистить хранилище ({exc})")

    def save(self, path=None):
        try:
            self.storage.save(path)
            target = getattr(self.storage, "path", path)
            if target:
                print(f"Данные сохранены: {target}")
            else:
                print("Данные сохранены.")
        except NotImplementedError as exc:
            print(f"Операция недоступна: {exc}")
        except Exception as exc:
            print(f"Ошибка: не удалось сохранить ({exc})")

    def load(self, path=None):
        try:
            count = self.storage.load(path)
            if isinstance(count, int):
                print(f"Загружено объектов: {count}")
            else:
                print("Загрузка выполнена.")
        except NotImplementedError as exc:
            print(f"Операция недоступна: {exc}")
        except Exception as exc:
            print(f"Ошибка: не удалось загрузить ({exc})")
