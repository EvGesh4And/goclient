from flask import request

FIELD_LABELS = {
    "species": "Вид",
    "habitat": "Среда обитания",
    "behavior": "Поведение",
    "hunting_style": "Стиль охоты",
    "favorite_plant": "Любимое растение",
    "time": "Обновлено",
}


class ConsoleIOStrategy:
    def input(self, prompt):
        return input(prompt)

    def input_field(self, obj, field_name):
        label = FIELD_LABELS.get(field_name, field_name)
        return input(f"{label}: ")

    def output_field(self, obj, field_name, output_dict):
        label = FIELD_LABELS.get(field_name, field_name)
        output_dict[label] = getattr(obj, field_name, "")

    def output(self, data):
        print(data)


class FlaskIOStrategy:
    def input(self, field_name):
        return request.form.get(field_name, "")

    def input_field(self, obj, field_name):
        return request.form.get(field_name, "")

    def output_field(self, obj, field_name, output_dict):
        label = FIELD_LABELS.get(field_name, field_name)
        output_dict[label] = getattr(obj, field_name, "")

    def output(self, data):
        return data


class WSGIIOStrategy:
    def __init__(self, form_data=None):
        self.form_data = form_data or {}

    def input(self, field_name):
        return self.form_data.get(field_name, [""])[0]

    def input_field(self, obj, field_name):
        return self.form_data.get(field_name, [""])[0]

    def output_field(self, obj, field_name, output_dict):
        label = FIELD_LABELS.get(field_name, field_name)
        output_dict[label] = getattr(obj, field_name, "")

    def output(self, data):
        return data