from typing import Any

from flask import request, render_template, url_for

from app.akm2501.st18.models import Student, Employee


class WebIO:
    def input(self, field: str, default_value: Any | None = None) -> str:
        value = request.form.get(field, "")

        if value == "" and default_value is not None:
            return str(default_value)

        return value

    def print(self, data: Any):
        pass

    def default_output(self, card_index):
        return card_index.output()

    def input_field(self, field: str, title: str | None = None, default: Any | None = None) -> str:
        return request.form.get(field, default)

    def output(self, items):
        return render_template('akm2501/st18/index.html', items=items)

    def output_item(self, item):
        data = item.get_data() if item else {}
        item_id = item.get_id() if item else 0
        return render_template('akm2501/st18/item.html', item=item, data=data, item_id=item_id)

    def edit_item(self, item):
        if not item:
            return ''

        item_id = item.get_id()
        data = item.get_data()
        action = url_for('st0118.process_item', item_id=item_id)

        if isinstance(item, Student):
            return render_template('akm2501/st18/edit_student.html', item_id=item_id, data=data, action=action)
        elif isinstance(item, Employee):
            return render_template('akm2501/st18/edit_employee.html', item_id=item_id, data=data, action=action)

        return ''
