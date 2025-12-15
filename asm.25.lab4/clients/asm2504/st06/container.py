if __name__ != '__main__':
    from .console_io import ConsoleIO
    from .camera import Camera
    from .lens import Lens
else:
    from console_io import ConsoleIO
    from camera import Camera
    from lens import Lens

from typing import List, Any

class Catalog:
    def __init__(self, io_strategy=None, storage_strategy=None):
        self.io = io_strategy if io_strategy else ConsoleIO()
        self.storage = storage_strategy 
        self.items: List[Any] = []

    def _ensure_io(self, item):
        if hasattr(item, "set_io"):
            item.set_io(self.io)
        else:
            setattr(item, "io", self.io)

    def _load_items_from_storage(self):
        raw = self.storage.list_items()
        self.items = raw
        for obj in self.items:
            self._ensure_io(obj)

    def add_item(self, item: Any):
        self._ensure_io(item)
        self.storage.add_item(item)
        self._load_items_from_storage()
        print("Элемент добавлен через REST.")

    def list_summary(self):
        self._load_items_from_storage()
        if not self.items:
            print("<пусто>")
            return
        for idx, item in enumerate(self.items, 1):
            t = type(item).__name__
            try:
                extra = item.summary()
            except Exception:
                extra = getattr(item, "manufacturer", "")
            print(f"{idx}) [{t}] {extra}")

    def print_full(self):
        self._load_items_from_storage()
        if not self.items:
            print("<пусто>")
            return
        for idx, item in enumerate(self.items, 1):
            print(f"\n=== Элемент {idx} ===")
            self._ensure_io(item)
            item.output_fields()

    def create_item_interactive(self):
        print("Выберите тип для добавления:")
        print("1) Камера")
        print("2) Объектив")
        t = input("Введите 1 или 2: ").strip()
        if t == "1":
            obj = Camera()
        elif t == "2":
            obj = Lens()
        else:
            print("Неверный выбор.")
            return
        self._ensure_io(obj)
        print("Введите поля для объекта (Enter — оставить текущее/по умолчанию):")
        obj.input_fields()
        self.add_item(obj)

    def edit_item(self):
        self._load_items_from_storage()
        if not self.items:
            print("<пусто>")
            return
        self.list_summary()
        choice = input("Введите номер элемента для редактирования: ").strip()
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(self.items):
                item = self.items[idx]
                self._ensure_io(item)
                print("Редактирование. Для пропуска нажмите Enter.")
                item.input_fields()
                ok = self.storage.update_item(idx, item)
                if not ok:
                    print("Ошибка обновления в storage.")
                else:
                    self._load_items_from_storage()
                    print("Изменения применены через REST.")
            else:
                print("Неверный номер.")
        except ValueError:
            print("Неверный ввод.")

    def delete_item(self):
        self._load_items_from_storage()
        if not self.items:
            print("<пусто>")
            return
        self.list_summary()
        choice = input("Введите номер элемента для удаления: ").strip()
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(self.items):
                ok = self.storage.delete_item(idx)
                if ok:
                    self._load_items_from_storage()
                    print("Элемент удалён через REST.")
                else:
                    print("Ошибка удаления в storage (not found).")
            else:
                print("Неверный номер.")
        except ValueError:
            print("Неверный ввод.")

    def clear(self):
        confirm = input("Очистить весь список? Введите YES для подтверждения: ")
        if confirm == "YES":
            self.storage.clear()
            self._load_items_from_storage()
            print("Список очищен через REST.")
        else:
            print("Отмена.")
