from typing import Callable, Dict, Any, Tuple, Optional

class StudentBase:
    TYPE_NAME = None
    fields: Dict[str, str] = {}

    def __init__(self):
        self._data: Dict[str, Any] = {k: None for k in self.fields.keys()}
        self.io_input: Optional[Callable] = None
        self.io_output: Optional[Callable] = None

    def set_io_strategy(self, input_fn: Callable[["StudentBase", str], None],
                        output_fn: Callable[["StudentBase", str], None]):
        if not callable(input_fn) or not callable(output_fn):
            raise TypeError("Стратегии должны быть вызываемыми")
        self.io_input = input_fn
        self.io_output = output_fn

    def input_field(self, name: str):
        if not self.io_input:
            raise RuntimeError("Стратегия ввода не установлена")
        self.io_input(self, name)

    def update_field(self, name: str):
        if not self.io_input:
            raise RuntimeError("Стратегия ввода не установлена")
        self.io_input(self, name)

    def output_field(self, name: str):
        if not self.io_output:
            raise RuntimeError("Стратегия вывода не установлена")
        self.io_output(self, name)

    def __str__(self):
        items = ", ".join(f"{self.fields.get(k, k)}: {v}" for k, v in self._data.items())
        return f"{self.TYPE_NAME} ({items})"

    def validate_field(self, field_name: str, raw: str) -> Tuple[bool, Any]:
        if raw == "":
            return (False, "Поле не может быть пустым")
        return (True, raw)
