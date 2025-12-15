from typing import Dict, List, Type, Optional
from flask import request

class FlaskIO:
    def __init__(self, classes: List[Type]):
        self.classes = classes
        self._last_message: Optional[str] = None

    def select_type_from_request(self) -> Optional[int]:
        t = (request.args.get("type") or "").strip()
        if not t:
            self.output_message("Не указан тип")
            return None
        if not t.isdigit():
            self.output_message("Ожидался номер типа")
            return None
        idx = int(t) - 1
        if not (0 <= idx < len(self.classes)):
            self.output_message("Номер вне диапазона")
            return None
        return idx

    def input_fields(self, obj) -> Dict[str, str]:
        updates: Dict[str, str] = {}
        for k in obj.fields.keys():
            updates[k] = (request.form.get(k) or "").strip()
        return updates

    def input_updates(self, obj) -> Dict[str, str]:
        updates: Dict[str, str] = {}
        for k in obj.fields.keys():
            if k in request.form:
                updates[k] = (request.form.get(k) or "").strip()
        return updates

    def select_index_from_request(self) -> Optional[int]:
        idx_raw = None
        if request.view_args:
            idx_raw = request.view_args.get("index")
        if idx_raw is None:
            self.output_message("Не указан индекс")
            return None
        try:
            ii = int(idx_raw)
        except Exception:
            self.output_message("Ожидался индекс")
            return None
        if not (0 <= ii):
            self.output_message("Неверный индекс")
            return None
        return ii

    def output_message(self, msg: str):
        self._last_message = str(msg)

    def pop_last_message(self) -> Optional[str]:
        m = self._last_message
        self._last_message = None
        return m

    def input_from_request(self, name: str) -> Optional[str]:
        value = (request.form.get(name) or "").strip()
        if not value:
            return None
        return value
