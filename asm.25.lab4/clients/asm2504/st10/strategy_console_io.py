from typing import Dict, Any, List, Type, Tuple, Optional

def _prompt_loop(prompt: str, validator):
    while True:
        raw = input(prompt)
        raw_str = raw.strip()
        ok, res = validator(raw_str)
        if ok:
            return raw_str
        print(f"Ошибка: {res}. Попробуйте ещё раз")

class ConsoleIO:
    def __init__(self, classes: List[Type]):
        self.classes = classes

    def _field_validator(self, obj, field):
        def validator(s: str) -> Tuple[bool, Any]:
            return obj.validate_field(field, s)
        return validator
   
    def input_fields(self, obj) -> Dict[str, str]:
        updates: Dict[str, str] = {}
        for field in obj.fields.keys():
            label = obj.fields[field]
            current = obj._data.get(field) if hasattr(obj, "_data") else None
            prompt = f"{label} [{current}]: " if current is not None else f"{label}: "
            validator = self._field_validator(obj, field)
            raw = _prompt_loop(prompt, validator)
            updates[field] = raw
        return updates

    def input_updates(self, obj) -> Dict[str, str]:
        keys = list(obj.fields.keys())
        readable = [f"{i}. {obj.fields[k]}" for i, k in enumerate(keys, start=1)]
        self.output_message("Доступные поля:\n" + "\n".join(readable))
        choice = input("Введите номер поля для редактирования (пусто — отмена): ").strip()
        if not choice:
            return {}
        if not choice.isdigit():
            self.output_message("Ожидался номер поля")
            return {}
        idx = int(choice) - 1
        if not (0 <= idx < len(keys)):
            self.output_message("Номер вне диапазона")
            return {}
        field = keys[idx]
        label = obj.fields[field]
        current = obj._data.get(field) if hasattr(obj, "_data") else None
        prompt = f"{label} [{current}]: " if current is not None else f"{label}: "
        validator = self._field_validator(obj, field)
        raw = _prompt_loop(prompt, validator)
        return {field: raw}

    def select_type(self) -> Optional[int]:
        choices = ", ".join(f"{i+1} - {cls.TYPE_NAME}" for i, cls in enumerate(self.classes))
        print(f"Выберите тип: {choices}")
        t = input("Тип (номер): ").strip()
        if not t or not t.isdigit():
            self.output_message("Отмена или неверный ввод")
            return None
        type_idx = int(t) - 1
        if not (0 <= type_idx < len(self.classes)):
            self.output_message("Номер вне диапазона")
            return None
        return type_idx

    def select_index(self, items: List[Any]) -> Optional[int]:
        if not items:
            self.output_message("Список пуст")
            return None
        for i, obj in enumerate(items):
            print(f"[{i}] {obj}")
        idx = input("Индекс для редактирования: ").strip()
        if not idx or not idx.isdigit():
            self.output_message("Отмена или неверный ввод")
            return None
        validated = int(idx)
        if not (0 <= validated < len(items)):
            self.output_message("Номер вне диапазона")
            return None
        return validated
    
    def output_message(self, msg: str):
        print(msg)

    def input_raw(self, prompt: str) -> str:
        return input(prompt).strip()
