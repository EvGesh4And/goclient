from typing import Any, Dict
from flask import Request

class FlaskIO:
    """
    Стратегия для веб-форм (HTML).
    Извлекает данные из request.form / request.values и
    умеет присваивать их полям объекта.
    """

    def extract(self, request: Request) -> Dict[str, Any]:
        """
        Вернуть словарь полей из form/values (не пробуем JSON).
        """
        return request.form.to_dict() or request.values.to_dict()

    def assign_fields(self, obj: Any, source) -> None:
        """
        Присвоить поля объекту.
        Если source — flask.request, сначала извлекаем словарь через extract().
        Если source — dict, используем его напрямую.
        """
        if hasattr(source, "form") and hasattr(source, "values"):
            data = self.extract(source)
        else:
            data = source or {}

        for name, prompt, default in obj.get_field_defs():
            raw = data.get(name)
            if isinstance(default, bool):
                setattr(obj, name, bool(raw))
            elif isinstance(default, int):
                try:
                    setattr(obj, name, int(raw))
                except (ValueError, TypeError):
                    setattr(obj, name, default)
            elif isinstance(default, float):
                try:
                    setattr(obj, name, float(raw))
                except (ValueError, TypeError):
                    setattr(obj, name, default)
            else:
                setattr(obj, name, raw if raw is not None else default)


class RestIO:
    """
    Стратегия для REST/JSON.
    Извлекает JSON из request.get_json() и присваивает поля объекту.
    """

    def extract(self, request: Request) -> Dict[str, Any]:
        """
        Вернуть JSON-словарь из запроса. Если JSON отсутствует — вернуть пустой dict.
        """
        data = request.get_json(silent=True)
        return data if isinstance(data, dict) else {}

    def assign_fields(self, obj: Any, source) -> None:
        """
        Присвоить поля объекту; source может быть flask.request или dict.
        """
        if hasattr(source, "get_json"):
            data = self.extract(source)
        else:
            data = source or {}

        for name, prompt, default in obj.get_field_defs():
            raw = data.get(name)
            if isinstance(default, bool):
                setattr(obj, name, bool(raw))
            elif isinstance(default, int):
                try:
                    setattr(obj, name, int(raw))
                except (ValueError, TypeError):
                    setattr(obj, name, default)
            elif isinstance(default, float):
                try:
                    setattr(obj, name, float(raw))
                except (ValueError, TypeError):
                    setattr(obj, name, default)
            else:
                setattr(obj, name, raw if raw is not None else default)
