import requests
from typing import Any, List, Optional, Dict
import os

try:
    from .camera import Camera
    from .lens import Lens
    from .equipment import Equipment
except Exception:
    from camera import Camera
    from lens import Lens
    from equipment import Equipment

data = requests.get("http://127.0.0.1:5000/api/").json()
my_number = next(n for n, t in data["sts"] if "[2504-06]" in t)
DEFAULT_BASE = os.environ.get("LAB4_API_BASE", f"http://127.0.0.1:5000/st{my_number}")

class StorageREST:
    def __init__(self, base: str = DEFAULT_BASE, timeout: float = 5.0):
        self.base = base.rstrip("/")
        self.api = self.base + "/api"
        self.timeout = timeout

    def load(self, filename: Optional[str] = None) -> List[Any]:
        try:
            r = requests.get(f"{self.api}/items", timeout=self.timeout)
            r.raise_for_status()
            rows = r.json()
            result = []
            for rw in rows:
                t = Equipment.detect_type(rw)
                if t == "lens":
                    result.append(Lens.from_row(rw))
                else:
                    result.append(Camera.from_row(rw))
            return result
        except Exception as e:
            print("StorageREST.load error:", e)
            return []

    def save(self, items: List[Any], filename: str = "data.pickle"):
        try:
            r = requests.post(f"{self.base}/save", data={"filename": filename}, timeout=self.timeout)
            if r.status_code in (200, 201, 302):
                return True, f"Requested server to save to '{filename}'"
            return False, f"Server returned {r.status_code}"
        except Exception as e:
            return False, f"Error: {e}"

    def list_items(self) -> List[Any]:
        return self.load()

    def add_item(self, obj: Any) -> Optional[int]:
        row: Dict[str, Any]
        if hasattr(obj, "to_row"):
            row = obj.to_row()
        elif isinstance(obj, dict):
            row = obj
        else:
            raise TypeError("StorageREST.add_item: unsupported object type")
        try:
            r = requests.post(f"{self.api}/items", json=row, timeout=self.timeout)
            r.raise_for_status()
            j = r.json()
            return j.get("id")
        except Exception as e:
            raise

    def update_item(self, idx: int, obj: Any) -> bool:
        if hasattr(obj, "to_row"):
            row = obj.to_row()
        elif isinstance(obj, dict):
            row = obj
        else:
            raise TypeError("StorageREST.update_item: unsupported object type")
        try:
            r = requests.put(f"{self.api}/items/{idx}", json=row, timeout=self.timeout)
            if r.status_code == 404:
                return False
            r.raise_for_status()
            return True
        except Exception:
            return False

    def get_item(self, idx: int) -> Optional[Any]:
        try:
            r = requests.get(f"{self.api}/items/{idx}", timeout=self.timeout)
            if r.status_code == 404:
                return None
            r.raise_for_status()
            rw = r.json()
            t = Equipment.detect_type(rw)
            return Lens.from_row(rw) if t == "lens" else Camera.from_row(rw)
        except Exception:
            return None

    def delete_item(self, idx: int) -> bool:
        try:
            r = requests.delete(f"{self.api}/items/{idx}", timeout=self.timeout)
            if r.status_code == 404:
                return False
            r.raise_for_status()
            return True
        except Exception:
            return False

    def clear(self) -> None:
        rows = self.list_items()
        for i in range(len(rows)-1, -1, -1):
            try:
                self.delete_item(i)
            except Exception:
                pass
