FIELD_LABELS = {
    "species": "Вид",
    "habitat": "Среда обитания",
    "behavior": "Поведение",
    "hunting_style": "Стиль охоты",
    "favorite_plant": "Любимое растение",
    "time": "Обновлено",
}


class ConsoleIO:
    def _label(self, field_name: str) -> str:
        return FIELD_LABELS.get(field_name, field_name)

    def input_field(self, obj, field_name: str) -> str:
        return input(f"{self._label(field_name)}: ").strip()

    def output_field(self, obj, field_name: str, output_dict: dict) -> None:
        output_dict[self._label(field_name)] = getattr(obj, field_name, "")

    def read_field(self, obj, field_name: str) -> None:
        setattr(obj, field_name, self.input_field(obj, field_name))

    def show(self, message: str) -> None:
        print(message)