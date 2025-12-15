FIELD_LABELS = {
    "name": "Имя",
    "age": "Возраст",
    "department": "Отдел",
    "team_size": "Размер команды",
    "has_company_car": "Служебный автомобиль",
}

TYPE_HINTS = {
    str: "строка",
    int: "целое число",
    float: "число",
    bool: "да/нет",
}


class ConsoleIO:
    def _label(self, field_name: str) -> str:
        return FIELD_LABELS.get(field_name, field_name)

    def _convert(self, text, to_type):
        if to_type is None:
            return text

        if to_type is bool:
            t = text.strip().lower()
            return t in ("1", "true", "t", "y", "yes", "да", "д", "истина")

        try:
            return to_type(text)
        except Exception:
            return text

    def _type_hint(self, field_type) -> str:
        if field_type is None:
            return ""
        return TYPE_HINTS.get(field_type, field_type.__name__)

    def _format_value(self, value):
        if isinstance(value, bool):
            return "да" if value else "нет"
        if value is None or value == "":
            return "—"
        return str(value)

    def read_field(self, obj, field_name):
        expected_type = None
        if hasattr(obj, "FIELDS"):
            expected_type = obj.FIELDS.get(field_name)

        label = self._label(field_name)
        hint = self._type_hint(expected_type)
        prompt = f"Введите {label}"
        if hint:
            prompt += f" ({hint})"
        prompt += ": "

        raw = input(prompt)

        try:
            value = self._convert(raw, expected_type)
            setattr(obj, field_name, value)
        except Exception:
            print("Ошибка: неверный формат. Поле не изменено.")

    def write_field(self, obj, field_name):
        value = getattr(obj, field_name, None)
        label = self._label(field_name)
        print(f"{label}: {self._format_value(value)}")