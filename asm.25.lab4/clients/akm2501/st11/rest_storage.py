import requests
from typing import Dict, Iterable, List, Optional, Tuple

from .models import Animal, Herbivore, Predator

TYPE_MAP: Dict[str, type] = {
    Animal.__name__: Animal,
    Predator.__name__: Predator,
    Herbivore.__name__: Herbivore,
}


class RestStorage:
    def __init__(self, base_url: str = "http://127.0.0.1:5000", module_hint: str = "[2501-11]"):
        self.base_url = base_url.rstrip("/")
        self.module_hint = module_hint
        self.session = requests.Session()
        self.timeout = 5
        self.prefix = self._detect_prefix()
        self.name = f"REST API ({self.base_url})"

    def _detect_prefix(self) -> str:
        try:
            response = self.session.get(f"{self.base_url}/api/", timeout=self.timeout)
            response.raise_for_status()
            data = response.json()
        except Exception as exc:
            raise RuntimeError("Не удалось запросить список модулей. Проверьте URL сервера.") from exc

        candidates = data.get("sts", []) if isinstance(data, dict) else []
        for index, title in candidates:
            if isinstance(title, str) and self.module_hint in title:
                return f"st{index}"
        raise RuntimeError("Не удалось определить маршрут для модуля.")

    def _animals_url(self, suffix: str = "") -> str:
        return f"{self.base_url}/{self.prefix}/api/animals{suffix}"

    def _request(self, method, url: str, **kwargs):
        try:
            response = method(url, timeout=self.timeout, **kwargs)
        except Exception as exc:
            raise RuntimeError("Сервер недоступен. Убедитесь, что приложение запущено.") from exc

        if response.status_code >= 400:
            try:
                payload = response.json()
                message = payload.get("message") or payload.get("error") or response.text
            except Exception:
                message = response.text
            raise RuntimeError(f"Ошибка сервера: {message}")
        return response

    def _object_from_payload(self, payload: Dict) -> Animal:
        cls = TYPE_MAP.get(payload.get("type"))
        if cls is None:
            raise RuntimeError(f"Неизвестный тип '{payload.get('type')}' из API")
        obj = cls()
        for field in cls.fields():
            if field in payload:
                setattr(obj, field, payload[field])
        obj.id = payload.get("id")
        if "time" in payload:
            obj.time = payload["time"]
        return obj

    def _payload_from_object(self, obj: Animal) -> Dict:
        data = {"type": obj.__class__.__name__}
        for field in obj.fields():
            data[field] = getattr(obj, field, "")
        return data

    def list_items(self) -> List[Tuple[str, Animal]]:
        response = self._request(self.session.get, self._animals_url())
        payload = response.json()
        items: List[Tuple[str, Animal]] = []
        for item in payload.get("animals", []):
            obj = self._object_from_payload(item)
            items.append((item.get("id"), obj))
        return items

    def add(self, obj: Animal) -> Optional[str]:
        data = self._payload_from_object(obj)
        response = self._request(self.session.post, self._animals_url(), json=data)
        payload = response.json()
        return payload.get("id")

    def get(self, item_id: str) -> Optional[Animal]:
        response = self._request(self.session.get, self._animals_url(f"/{item_id}"))
        payload = response.json()
        return self._object_from_payload(payload)

    def update(self, item_id: str, obj: Animal) -> bool:
        data = self._payload_from_object(obj)
        self._request(self.session.put, self._animals_url(f"/{item_id}"), json=data)
        return True

    def remove(self, item_id: str) -> bool:
        self._request(self.session.delete, self._animals_url(f"/{item_id}"))
        return True

    def clear(self) -> int:
        response = self._request(self.session.delete, self._animals_url())
        payload = response.json()
        return int(payload.get("removed", 0))

    def save(self, path: Optional[str] = None):
        raise NotImplementedError("Сохранение в файл недоступно для REST-хранилища")

    def load(self, path: Optional[str] = None):
        raise NotImplementedError("Загрузка из файла недоступна для REST-хранилища")

    def add_many(self, objects: Iterable[Animal]) -> int:
        count = 0
        for obj in objects:
            if self.add(obj):
                count += 1
        return count

