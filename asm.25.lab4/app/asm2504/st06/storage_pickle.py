# storage_pickle.py
import pickle
import os
from typing import Any, List

class PickleStorage:
    """
    Хранилище, содержащее список объектов в памяти и умеющее сохранять/загружать его в файл.
    Интерфейс:
        - list_items() -> List[Any]
        - get_item(idx) -> Any or None
        - add_item(obj)
        - update_item(idx, obj)
        - delete_item(idx)
        - clear()
        - save(filename)
        - load(filename)
    """

    def __init__(self):
        self.items: List[Any] = []

    def _ensure_ext(self, filename: str) -> str:
        base, ext = os.path.splitext(filename)
        if ext.lower() != ".pickle":
            filename = base + ".pickle"
        return filename

    # CRUD in-memory
    def list_items(self) -> List[Any]:
        return self.items

    def get_item(self, idx: int):
        try:
            return self.items[idx]
        except Exception:
            return None

    def add_item(self, obj: Any):
        self.items.append(obj)

    def update_item(self, idx: int, obj: Any):
        if 0 <= idx < len(self.items):
            self.items[idx] = obj
            return True
        return False

    def delete_item(self, idx: int):
        if 0 <= idx < len(self.items):
            self.items.pop(idx)
            return True
        return False

    def clear(self):
        self.items.clear()

    # Persistence
    def save(self, filename: str):
        fn = self._ensure_ext(filename)
        try:
            with open(fn, "wb") as f:
                pickle.dump(self.items, f)
            return True, f"Saved {len(self.items)} items to '{fn}'."
        except Exception as e:
            return False, f"Error saving: {e}"

    def load(self, filename: str):
        fn = self._ensure_ext(filename)
        try:
            with open(fn, "rb") as f:
                data = pickle.load(f)
            if isinstance(data, list):
                self.items = data
                return True, f"Loaded {len(self.items)} items from '{fn}'."
            else:
                return False, "File format invalid (expected list)."
        except FileNotFoundError:
            return False, f"File '{fn}' not found."
        except Exception as e:
            return False, f"Error loading: {e}"
