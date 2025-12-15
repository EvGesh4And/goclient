from typing import Any

from flask import request, jsonify


class RestIO:
    def default_output(self, card_index):
        return ""

    def output(self, items):
        items_data = []
        for item_id, item in items.items():
            items_data.append(item.get_data())
        return jsonify({'items': items_data})

    def input(self, field: str, default_value: Any | None = None) -> str:
        return request.json.get(field, default_value)

    def input_field(self, field: str, title: str | None = None, default: Any | None = None) -> str:
        return request.json.get(field, default)

    def output_item(self, item):
        if item:
            return jsonify(item.get_data())
        return ""

    def edit_item(self, item):
        pass

    def print(self, data: Any):
        pass