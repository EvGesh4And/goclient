from .employee import Employee
from .worker import Worker
from .manager import Manager
from .director import Director

class GroupContainer:
    def __init__(self, io, storage):
        self.items = []
        self.io = io
        self.storage = storage
        self.types = {
            "1": Worker,
            "2": Manager,
            "3": Director
        }
        self.type_names = {
            "Worker": Worker,
            "Manager": Manager,
            "Director": Director
        }

    def _bind_io(self, obj):
        obj.io = self.io
        return obj

    def add_item(self, type_name=None, form_data=None, json_data=None):
        if type_name:
            cls = self.type_names.get(type_name)
            if cls is None:
                return False
            obj = cls(io=self.io)
            if form_data:
                self.io.fill_object_from_form(obj, form_data)
            elif json_data:
                for field_name, field_type in obj.FIELDS.items():
                    if field_name in json_data:
                        value = json_data[field_name]
                        if field_type is bool:
                            if isinstance(value, bool):
                                pass
                            elif isinstance(value, str):
                                value = value.strip().lower() in ("true", "1", "yes", "y", "on")
                            elif isinstance(value, (int, float)):
                                value = bool(value)
                            else:
                                value = False
                        else:
                            try:
                                value = field_type(value)
                            except (TypeError, ValueError):
                                if field_type is str:
                                    value = "" if value is None else str(value)
                                else:
                                    return False
                        setattr(obj, field_name, value)
            else:
                obj.input_fields()
            self.items.append(obj)
            return True
        else:
            print("Тип объекта: 1) Worker, 2) Manager, 3) Director")
            choice = input("Ваш выбор (1/2/3): ").strip()
            cls = self.types.get(choice)
            if cls is None:
                print("Неизвестный тип.")
                return False
            obj = cls(io=self.io)
            print("Введите поля объекта:")
            obj.input_fields()
            self.items.append(obj)
            print("✔ Добавлено.")
            return True

    def list_items(self):
        if len(self.items) == 0:
            print("Список пуст.")
            return
        for i, obj in enumerate(self.items, 1):
            print("[" + str(i) + "] " + obj.type_name())
            obj.print_fields()
            print("-" * 20)

    def list_items_html(self, url_for_func=None):
        items_with_ids = [(obj, i) for i, obj in enumerate(self.items)]
        return self.io.build_table_html(items_with_ids, url_for_func=url_for_func)

    def _select_index(self):
        self.list_items()
        try:
            raw = input("Номер объекта: ")
            idx = int(raw)
        except Exception:
            print("Неверный номер.")
            return None
        if not (1 <= idx <= len(self.items)):
            print("Неверный диапазон.")
            return None
        return idx - 1

    def edit_item(self, idx=None, form_data=None, json_data=None, partial=False):
        if len(self.items) == 0:
            print("Список пуст.")
            return False
        if idx is not None:
            if not (0 <= idx < len(self.items)):
                return False
            obj = self.items[idx]
            if form_data:
                self.io.fill_object_from_form(obj, form_data)
            elif json_data:
                for field_name, field_type in obj.FIELDS.items():
                    if field_name in json_data:
                        value = json_data[field_name]
                        if field_type is bool:
                            if isinstance(value, bool):
                                pass
                            elif isinstance(value, str):
                                value = value.strip().lower() in ("true", "1", "yes", "y", "on")
                            elif isinstance(value, (int, float)):
                                value = bool(value)
                            else:
                                value = False
                        else:
                            try:
                                value = field_type(value)
                            except (TypeError, ValueError):
                                if field_type is str:
                                    value = "" if value is None else str(value)
                                else:
                                    return False
                        setattr(obj, field_name, value)
                    elif not partial:
                        return False
            else:
                fields = list(obj.FIELDS.keys())
                print("Доступные поля: " + ", ".join(fields))
                field = input("Поле для редактирования: ").strip()
                if field not in obj.FIELDS:
                    print("Нет такого поля.")
                    return False
                self.io.read_field(obj, field)
            return True
        else:
            idx = self._select_index()
            if idx is None:
                return False
            obj = self.items[idx]
            fields = list(obj.FIELDS.keys())
            print("Доступные поля: " + ", ".join(fields))
            field = input("Поле для редактирования: ").strip()
            if field not in obj.FIELDS:
                print("Нет такого поля.")
                return False
            self.io.read_field(obj, field)
            print("✔ Изменено.")
            return True

    def remove_item(self, idx=None):
        if len(self.items) == 0:
            print("Список пуст.")
            return False
        if idx is not None:
            if not (0 <= idx < len(self.items)):
                return False
            removed = self.items.pop(idx)
            return True
        else:
            idx = self._select_index()
            if idx is None:
                return False
            removed = self.items.pop(idx)
            print("✔ Удалён " + removed.type_name() + ".")
            return True

    def clear(self):
        self.items = []
        print("✔ Список очищен.")

    def save(self, path=None):
        self.storage.save(self.items)

    def load(self, path=None):
        data = self.storage.load()
        self.items = []
        for obj in data:
            self._bind_io(obj)
            self.items.append(obj)

