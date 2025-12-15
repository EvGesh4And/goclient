# storage_pickle.py
import pickle
from typing import List, Any, Type, Optional
from pathlib import Path

class PickleStorage:
    def __init__(self, 
                 classes: Optional[List[Type]] = None, 
                 base_dir: Optional[Path] = '', 
                 items: Optional[List[Any]] = None):
        self._items = list(items) if items is not None else []
        self.classes = list(classes) if classes is not None else []
        self.base_dir: Path = Path(base_dir)

    def _full_path(self, filename: str) -> Path:
        return self.base_dir / filename

    def add(self, obj: Any):
        self._items.append(obj)

    def list(self) -> List[Any]:
        return list(self._items)

    def remove(self, index: int) -> Any:
        return self._items.pop(index)

    def update(self, index: int, obj: Any):
        self._items[index] = obj

    def clear(self):
        self._items.clear()

    def save(self, filename: str):
        path = self._full_path(filename)
        path.parent.mkdir(parents=True, exist_ok=True)
        tosave = [{"__class__": o.__class__.__name__, "data": getattr(o, "_data", {})} for o in self._items]
        path.write_bytes(pickle.dumps(tosave))

    def load(self, filename: str):
        path = self._full_path(filename)
        with open(path, "rb") as f:
            raw = pickle.load(f)
        self._items.clear()
        for entry in raw:
            cls_name = entry.get("__class__")
            data = entry.get("data", {})
            found = None
            for c in self.classes:
                if getattr(c, "__name__", None) == cls_name or getattr(c, "TYPE_NAME", None) == cls_name:
                    found = c
                    break
            if found is None:
                continue
            obj = found()
            if not hasattr(obj, "_data"):
                obj._data = {}
            obj._data.update(data)
            self._items.append(obj)
