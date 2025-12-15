from markupsafe import Markup


class FlaskIO:
    FIELD_NAMES = {
        "name": "Имя и фамилия",
        "age": "Возраст",
        "group": "Группа",
        "record_book": "Зачетная книжка",
        "avg_grade": "Средний балл",
        "phone": "Телефон",
        "duties": "Обязанности",
        "union_member": "Член профсоюза",
        "events_count": "Количество мероприятий",
    }

    TYPE_NAMES = {
        "Student": "Студент",
        "Starosta": "Староста",
        "Proforg": "Профорг",
    }

    def _convert_from_form(self, text, to_type):
        if to_type is None:
            return text
        if to_type is bool:
            return text == "on"
        try:
            return to_type(text)
        except (ValueError, TypeError):
            return {int: 0, float: 0.0}.get(to_type, str(text))

    def fill_object_from_form(self, obj, form_data):
        for field_name, field_type in obj.FIELDS.items():
            if field_type is bool:
                raw = form_data.get(field_name, None)
                value = self._convert_from_form("on" if raw is not None else "", bool)
            else:
                raw = form_data.get(field_name, "")
                value = self._convert_from_form(raw, field_type)
            setattr(obj, field_name, value)

    def _input_type_for(self, py_type):
        return {int: "number", float: "number", bool: "checkbox"}.get(py_type, "text")

    def build_form_html(self, obj, action_url, title, submit_text, cancel_url=None):
        lines = [f'<h2>{title}</h2>', f'<form method="post" action="{action_url}" class="form-grid">']

        for fname, ftype in obj.FIELDS.items():
            input_type = self._input_type_for(ftype)
            display_name = self.FIELD_NAMES.get(fname, fname)
            
            if input_type == "checkbox":
                checked = " checked" if getattr(obj, fname, False) else ""
                lines.append(f'<label class="checkbox"><input type="checkbox" name="{fname}"{checked}> {display_name}</label>')
            else:
                value = getattr(obj, fname, "")
                if input_type == "number" and ftype is float:
                    step_attr = ' step="0.01"'
                else:
                    step_attr = ""
                lines.append(f'<label>{display_name}<input type="{input_type}" name="{fname}" value="{str(value)}"{step_attr}></label>')

        cancel_url = cancel_url or "/"
        lines.extend(
            [
                '<div class="actions">',
                f'<button type="submit" class="btn primary">{submit_text}</button>',
                f'<a href="{cancel_url}" class="btn">Отмена</a>',
                '</div>',
                "</form>",
            ]
        )
        return Markup("\n".join(lines))

    def build_table_html(self, items_with_ids=None, url_for_func=None):
        if not items_with_ids:
            return Markup('<p>Пока нет записей.</p>')

        items_with_ids_list = (
            items_with_ids
            if isinstance(items_with_ids[0], tuple)
            else [(obj, i) for i, obj in enumerate(items_with_ids)]
        )

        lines = ['<table class="table">', "<thead><tr><th>#</th><th>Тип</th><th>Данные</th><th>Действия</th></tr></thead>", "<tbody>"]

        for i, (obj, item_id) in enumerate(items_with_ids_list):
            field_parts = [
                f"<strong>{self.FIELD_NAMES.get(fname, fname)}:</strong> {getattr(obj, fname, '') or '—'}"
                for fname in obj.FIELDS.keys()
            ]
            fields_str = "<br>".join(field_parts)
            type_display = self.TYPE_NAMES.get(obj.__class__.__name__, obj.__class__.__name__)

            if url_for_func:
                view_url = url_for_func("st0412.view_item", item_id=item_id)
                edit_url = url_for_func("st0412.edit_item", item_id=item_id)
                delete_url = url_for_func("st0412.delete_item", item_id=item_id)
            else:
                view_url = f"/view/{item_id}"
                edit_url = f"/edit/{item_id}"
                delete_url = f"/delete/{item_id}"

            lines.extend(
                [
                    "<tr>",
                    f"<td>{i + 1}</td>",
                    f"<td><span class='badge'>{type_display}</span></td>",
                    f"<td>{fields_str}</td>",
                    f"<td><div class='actions'><a href='{view_url}' class='btn'>Просмотр</a> <a href='{edit_url}' class='btn'>Изменить</a> <a href='{delete_url}' class='btn danger'>Удалить</a></div></td>",
                    "</tr>",
                ]
            )

        lines.append("</tbody></table>")
        return Markup("\n".join(lines))

