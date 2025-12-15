import requests

from typing import Dict, Iterable, List, Optional, Tuple

from .employee import Employee


class RestStorage:
    def __init__(self, base_url: str = "http://127.0.0.1:5000", module_hint: str = "[2501-14]", type_registry: Dict[str, type] = None):
        self.base_url = base_url.rstrip("/")
        self.module_hint = module_hint
        self.session = requests.Session()
        self.timeout = 5
        self.type_registry = type_registry or {}
        self.prefix = self._detect_prefix()

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
        raise RuntimeError("Не удалось определить маршрут для нашего модуля через /api/.")

    def _employees_url(self, suffix: str = "") -> str:
        return f"{self.base_url}/{self.prefix}/api/employees{suffix}"

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

    def _object_from_payload(self, payload: Dict) -> Employee:
        type_name = payload.get("type")
        cls = self.type_registry.get(type_name)
        if cls is None:
            raise RuntimeError(f"Неизвестный тип сотрудника '{type_name}' из API")
        obj = cls()
        for field in obj.FIELDS.keys():
            if field in payload:
                setattr(obj, field, payload[field])
        return obj

    def _payload_from_object(self, obj: Employee) -> Dict:
        data = {"type": obj.__class__.__name__}
        for field in obj.FIELDS.keys():
            value = getattr(obj, field, None)
            data[field] = value
        return data

    def list_items(self) -> List[Tuple[int, Employee]]:
        response = self._request(self.session.get, self._employees_url())
        data = response.json()
        result: List[Tuple[int, Employee]] = []
        for item in data.get("employees", []):
            obj = self._object_from_payload(item)
            result.append((item.get("id"), obj))
        return result

    def add(self, obj: Employee) -> Optional[int]:
        payload = self._payload_from_object(obj)
        response = self._request(self.session.post, self._employees_url(), json=payload)
        data = response.json()
        return data.get("id")

    def get(self, item_id: int) -> Optional[Employee]:
        response = self._request(self.session.get, self._employees_url(f"/{item_id}"))
        data = response.json()
        return self._object_from_payload(data)

    def update(self, item_id: int, obj: Employee) -> bool:
        payload = self._payload_from_object(obj)
        self._request(self.session.put, self._employees_url(f"/{item_id}"), json=payload)
        return True

    def remove(self, item_id: int) -> bool:
        self._request(self.session.delete, self._employees_url(f"/{item_id}"))
        return True

    def clear(self) -> int:
        response = self._request(self.session.delete, self._employees_url())
        data = response.json()
        return int(data.get("removed", 0))

    def save(self, path: Optional[str] = None):
        raise NotImplementedError("Сохранение в файл недоступно для REST-хранилища")

    def load(self, path: Optional[str] = None):
        raise NotImplementedError("Загрузка из файла недоступна для REST-хранилища")

    def add_many(self, objects: Iterable[Employee]) -> int:
        count = 0
        for obj in objects:
            if self.add(obj):
                count += 1
        return count
