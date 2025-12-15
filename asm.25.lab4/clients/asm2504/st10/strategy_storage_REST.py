import requests
from typing import List, Any, Type, Optional

class RESTStorage:
    def __init__(self,
                 base_url: str = "http://127.0.0.1:5000/api",
                 classes: Optional[List[Type]] = None,
                 timeout: float = 5.0):
        self.base_url = base_url.rstrip("/")
        self.classes = list(classes) if classes is not None else []
        self.timeout = timeout

    def _obj_to_entry(self, o: Any) -> dict:
        return {"__class__": o.__class__.__name__, "data": getattr(o, "_data", {})}

    def _entry_to_obj(self, entry: dict):
        cls_name = entry.get("__class__")
        data = entry.get("data", {})
        for c in self.classes:
            if getattr(c, "__name__", None) == cls_name or getattr(c, "TYPE_NAME", None) == cls_name:
                obj = c()
                if not hasattr(obj, "_data"):
                    obj._data = {}
                obj._data.update(data)
                return obj
        return None

    def list(self) -> List[Any]:
        resp = requests.get(f"{self.base_url}/members", timeout=self.timeout)
        resp.raise_for_status()
        raw = resp.json()
        items = []
        for entry in raw:
            obj = self._entry_to_obj(entry)
            if obj is not None:
                items.append(obj)
        return items

    def add(self, obj: Any):
        resp = requests.post(f"{self.base_url}/members/add", json=self._obj_to_entry(obj), timeout=self.timeout)
        resp.raise_for_status()
        return obj

    def remove(self, index: int) -> Any:
        resp = requests.delete(f"{self.base_url}/members/remove/{index}", timeout=self.timeout)
        if resp.status_code == 404:
            raise IndexError("index out of range")
        resp.raise_for_status()
        removed = resp.json().get("removed")
        return self._entry_to_obj(removed) if removed is not None else None

    def update(self, index: int, obj: Any):
        print(index)
        resp = requests.put(f"{self.base_url}/members/edit/{index}", json=self._obj_to_entry(obj), timeout=self.timeout)
        if resp.status_code == 404:
            raise IndexError("index out of range")
        resp.raise_for_status()
        return obj

    def clear(self):
        resp = requests.post(f"{self.base_url}/members/clear_list", json=[], timeout=self.timeout)
        resp.raise_for_status()

    def save(self, filename: str):
        resp = requests.post(f"{self.base_url}/members/save/{filename}", timeout=self.timeout)
        resp.raise_for_status()

    def load(self, filename: str):
        resp = requests.get(f"{self.base_url}/members/load/{filename}", timeout=self.timeout)
        resp.raise_for_status()
        raw = resp.json()
        items = []
        for entry in raw:
            obj = self._entry_to_obj(entry)
            if obj is not None:
                items.append(obj)
        return items
