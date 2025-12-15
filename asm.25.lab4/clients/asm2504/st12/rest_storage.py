import requests

from .student import Student
from .starosta import Starosta
from .proforg import Proforg

TYPE_MAP = {
    "Student": Student,
    "Starosta": Starosta,
    "Proforg": Proforg,
}


class RestStorage:
    def __init__(self, base_url: str = "http://127.0.0.1:5000", module_hint: str = "[2504-12]"):
        self.base_url = base_url.rstrip("/")
        self.module_hint = module_hint
        self.session = requests.Session()
        self.timeout = 5
        self._prefix = None

    @property
    def prefix(self) -> str:
        if self._prefix is None:
            self._prefix = self._detect_prefix()
        return self._prefix

    def _detect_prefix(self) -> str:
        try:
            resp = self.session.get(f"{self.base_url}/api/", timeout=self.timeout)
            resp.raise_for_status()
            data = resp.json()
        except Exception as exc:
            raise RuntimeError("Не удалось запросить список модулей. Проверьте URL сервера.") from exc

        candidates = data.get("sts", []) if isinstance(data, dict) else []
        for index, title in candidates:
            if isinstance(title, str) and self.module_hint in title:
                return f"st{index}"
        raise RuntimeError("Не удалось определить маршрут для модуля через /api/.")

    def _students_url(self, suffix: str = "") -> str:
        return f"{self.base_url}/{self.prefix}/api/students{suffix}"

    def _request(self, method, url: str, **kwargs):
        try:
            response = method(url, timeout=self.timeout, **kwargs)
        except Exception as exc:
            raise RuntimeError("Сервер недоступен. Убедитесь, что WSGI-приложение запущено.") from exc

        if response.status_code >= 400:
            try:
                info = response.json()
                message = info.get("message") or info.get("error")
            except Exception:
                message = response.text
            raise RuntimeError(f"Ошибка сервера: {message}")
        return response

    def _object_from_payload(self, payload):
        type_name = payload.get("type")
        cls = TYPE_MAP.get(type_name)
        if cls is None:
            raise RuntimeError(f"Неизвестный тип '{type_name}' из API")
        obj = cls()
        for field in obj.FIELDS.keys():
            if field in payload:
                setattr(obj, field, payload[field])
        # Store the ID if present
        if "id" in payload:
            obj._api_id = payload["id"]
        return obj

    def _payload_from_object(self, obj):
        data = {"type": obj.__class__.__name__}
        for field in obj.FIELDS.keys():
            data[field] = getattr(obj, field, None)
        return data

    def save(self, items, filepath=None):
        """Save items to REST API. If filepath is None, syncs with server."""
        try:
            if filepath is None:
                # Sync mode: replace all data on server
                # Simple approach: clear all and re-add (works for lab scenario)
                try:
                    # Clear all existing
                    self._request(self.session.delete, self._students_url())
                except Exception:
                    pass  # Ignore if already empty
                
                # Add all items
                for obj in items:
                    payload = self._payload_from_object(obj)
                    response = self._request(self.session.post, self._students_url(), json=payload)
                    if response.status_code == 201:
                        data = response.json()
                        if "id" in data:
                            obj._api_id = data["id"]
            else:
                # File mode: not applicable for REST storage
                print("REST storage не поддерживает сохранение в файл")
                return
            print("Данные сохранены на сервер через REST API")
        except Exception as exc:
            print(f"Ошибка при сохранении через REST API: {exc}")
            raise

    def load(self, filepath=None):
        try:
            response = self._request(self.session.get, self._students_url())
            data = response.json()
            items = []
            for item in data.get("students", []):
                items.append(self._object_from_payload(item))
            print(f"Данные загружены с сервера через REST API ({len(items)} объектов)")
            return items
        except Exception as exc:
            print(f"Ошибка при загрузке через REST API: {exc}")
            return []

