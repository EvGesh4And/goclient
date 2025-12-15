from typing import Optional, Tuple

from .console_io import ConsoleIO, FIELD_LABELS
from .models import Animal, Herbivore, Predator


TYPE_LABELS = {
    "Animal": "Обычное животное",
    "Predator": "Хищник",
    "Herbivore": "Травоядное",
}


class GroupContainer:
    def __init__(self, io: ConsoleIO, storage):
        self.io = io
        self.storage = storage
        self.types = {
            "1": Animal,
            "2": Predator,
            "3": Herbivore,
        }

    def set_storage(self, storage) -> None:
        self.storage = storage
        print(f"✔ Текущее хранилище: {self.get_storage_name()}")

    def get_storage_name(self) -> str:
        return getattr(self.storage, "name", self.storage.__class__.__name__)

    def _bind_io(self, obj: Animal) -> Animal:
        obj.io = self.io
        return obj

    def _load_items(self):
        try:
            return self.storage.list_items()
        except Exception as exc:
            print(f"⚠️ Не удалось получить список: {exc}")
            return []

    def _choose_type(self):
        print("Тип: 1) Обычное животное  2) Хищник  3) Травоядное")
        choice = input("Ваш выбор: ").strip()
        cls = self.types.get(choice)
        if cls is None:
            print("Нет такого типа.")
        return cls

    def _select_item(self) -> Optional[Tuple[str, Animal]]:
        items = self._load_items()
        if not items:
            print("Каталог пуст.")
            return None

        for index, (item_id, obj) in enumerate(items, 1):
            obj_type = TYPE_LABELS.get(obj.__class__.__name__, obj.__class__.__name__)
            print(f"[{index}] ID={item_id} • {obj_type}")
            self._bind_io(obj).print_fields()
            print("-" * 20)

        try:
            raw = input("Номер записи: ").strip()
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

    def add_item(self) -> None:
        cls = self._choose_type()
        if cls is None:
            return

        obj = cls()
        obj.io = self.io
        print("Введите данные животного:")
        obj.input_data(self.io)

        try:
            new_id = self.storage.add(obj)
            print(f"✔ Добавлено. ID={new_id}")
        except Exception as exc:
            print(f"⚠️ Не удалось добавить: {exc}")

    def list_items(self) -> None:
        items = self._load_items()
        if not items:
            print("Каталог пуст.")
            return

        print(f"Хранилище: {self.get_storage_name()}")
        for index, (item_id, obj) in enumerate(items, 1):
            obj_type = TYPE_LABELS.get(obj.__class__.__name__, obj.__class__.__name__)
            print(f"[{index}] ID={item_id} • {obj_type}")
            self._bind_io(obj).print_fields()
            print("-" * 20)

    def edit_item(self) -> None:
        selected = self._select_item()
        if not selected:
            return
        item_id, obj = selected
        fields = list(obj.fields())
        readable = [FIELD_LABELS.get(field, field) for field in fields]
        print("Доступные поля:", ", ".join(readable))
        labels_map = {FIELD_LABELS.get(field, field): field for field in fields}
        labels_map.update({field: field for field in fields})
        choice = input("Поле для редактирования: ").strip()
        field = labels_map.get(choice)
        if field is None:
            print("Нет такого поля.")
            return

        self.io.read_field(obj, field)
        try:
            if self.storage.update(item_id, obj):
                print("✔ Изменено.")
            else:
                print("⚠️ Не удалось обновить запись.")
        except Exception as exc:
            print(f"⚠️ Ошибка при обновлении: {exc}")

    def remove_item(self) -> None:
        selected = self._select_item()
        if not selected:
            return
        item_id, obj = selected
        try:
            if self.storage.remove(item_id):
                print(f"✔ Удалено: {obj.__class__.__name__} (ID={item_id})")
            else:
                print("⚠️ Не найдено.")
        except Exception as exc:
            print(f"⚠️ Ошибка при удалении: {exc}")

    def clear(self) -> None:
        try:
            removed = self.storage.clear()
            print(f"✔ Каталог очищен. Удалено: {removed}")
        except Exception as exc:
            print(f"⚠️ Не удалось очистить: {exc}")

    def save(self, path: str | None = None) -> None:
        try:
            self.storage.save(path)
            if hasattr(self.storage, "path"):
                print(f"✔ Сохранено в {self.storage.path}")
            else:
                print("✔ Сохранено.")
        except NotImplementedError as exc:
            print(f"⚠️ {exc}")
        except Exception as exc:
            print(f"⚠️ Не удалось сохранить: {exc}")

    def load(self, path: str | None = None) -> None:
        try:
            count = self.storage.load(path)
            if isinstance(count, int):
                print(f"✔ Загружено объектов: {count}")
            else:
                print("✔ Загрузка выполнена.")
        except NotImplementedError as exc:
            print(f"⚠️ {exc}")
        except Exception as exc:
            print(f"⚠️ Не удалось загрузить: {exc}")

