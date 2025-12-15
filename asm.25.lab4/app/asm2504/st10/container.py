from typing import List, Type, Dict, Any, Optional

class Container:
    def __init__(self, io_strategy, storage_strategy, classes: List[Type]):
        self.io = io_strategy
        self.storage = storage_strategy
        self.classes: List[Type] = classes

    def validate_index(self, index: int) -> bool:
        items = self.storage.list()
        if not (0 <= index < len(items)):
            self.io.output_message("Индекс вне диапазона")
            return False
        return True

    def validate_index_str(self, index_str: str) -> Optional[int]:
        if not index_str:
            self.io.output_message("Не указан индекс")
            return None
        if not index_str.isdigit():
            self.io.output_message("Ожидался индекс")
            return None
        index = int(index_str)
        if not self.validate_index(index):
            return None
        return index

    def update_fields_obj(self, obj, updates: Dict[str, Any]):
        new_data = dict(getattr(obj, "_data", {}))
        for field, raw in updates.items():
            if field not in obj.fields:
                raise KeyError(f"Неизвестное поле: {field}")
            ok, val_or_err = obj.validate_field(field, raw)
            if not ok:
                raise ValueError(f"{obj.fields[field]}: {val_or_err}")
            new_data[field] = val_or_err
        obj._data = new_data

    def create_from_type_index(self, type_index: int, raw_fields: Dict[str, str]):
        if not (0 <= type_index < len(self.classes)):
            self.io.output_message("Номер вне диапазона")
            return None
        cls = self.classes[type_index]
        obj = cls()
        try:
            self.update_fields_obj(obj, raw_fields)
        except Exception as e:
            self.io.output_message(f"Ошибка при создании. {e}")
            return None
        self.storage.add(obj)
        self.io.output_message(f"Добавлено: {obj}")
        return obj

    def edit_by_index_str(self, index_str: str, updates: Dict[str, Any]):
        idx = self.validate_index_str(index_str)
        if idx is None:
            return None
        try:
            items = self.storage.list()
            obj = items[idx]
            self.update_fields_obj(obj, updates)
            self.storage.update(idx, obj)
            self.io.output_message(f"Изменено: {obj}")
            return obj
        except Exception as e:
            self.io.output_message(f"Ошибка при сохранении. {e}")
            return None

    def remove_by_index_str(self, index_str: str) -> bool:
        idx = self.validate_index_str(index_str)
        if idx is None:
            return False
        try:
            items = self.storage.list()
            obj = items[idx]
            res = self.storage.remove(idx)
            if res is not None:
                self.io.output_message(f"Удалено: {obj}")
                return True
            return False
        except Exception as e:
            self.io.output_message(f"Ошибка: {e}")
            return False

    def clear_with_message(self):
        try:
            self.storage.clear()
            self.io.output_message("Список очищен")
        except Exception as e:
            self.io.output_message(str(e))

    def list_items_with_message(self):
        items = self.storage.list()
        if not items:
            self.io.output_message("Список пуст")
        return items

    def save_by_filename(self, fname: str) -> bool:
        f = (fname or "").strip()
        if not f:
            self.io.output_message("Пустое имя файла")
            return False
        try:
            self.storage.save(f)
            self.io.output_message(f"Сохранено в {f}")
            return True
        except Exception as e:
            self.io.output_message(f"Ошибка при сохранении. {e}")
            return False

    def load_by_filename(self, fname: str) -> bool:
        f = (fname or "").strip()
        if not f:
            self.io.output_message("Пустое имя файла")
            return False
        try:
            self.storage.load(f)
            self.io.output_message(f"Загружено {len(self.storage.list())} объектов из {f}")
            return True
        except Exception as e:
            self.io.output_message(f"Ошибка при загрузке. {e}")
            return False
