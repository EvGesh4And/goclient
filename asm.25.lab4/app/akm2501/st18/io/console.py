from typing import Any


class ConsoleIO:
    def input(self, field: str, default_value: Any | None = None) -> str:
        input_text = f"{field}: "
        input_data = input(input_text)

        if input_data == "" and default_value is not None:
            return str(default_value)

        return input_data

    def print(self, data: Any):
        print(data)

    def default_output(self, card_index) -> str:
        return ""

    def output(self, items: dict):
        for item in items.values():
            print(item)

    def input_field(self, field: str, title: str | None = None, default: Any | None = None) -> str:
        if field == "id" and default is not None:
            return default
        prompt = title if title else field
        return input(f"{prompt}: ")

    def output_item(self, item) -> str:
        if item:
            return str(item)
        return ""

    def edit_item(self, item):
        pass
