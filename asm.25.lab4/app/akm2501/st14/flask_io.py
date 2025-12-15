from markupsafe import Markup

class FlaskIO:
    def _convert(self, text, to_type):
        if to_type is None:
            return text
        if to_type is bool:
            t = text.strip().lower()
            return t in ("1", "true", "t", "y", "yes", "да", "д", "истина", "on")
        try:
            return to_type(text)
        except Exception:
            return text

    def read_field(self, obj, field_name):
        from flask import request
        expected_type = None
        if hasattr(obj, "FIELDS"):
            expected_type = obj.FIELDS.get(field_name)
        
        if request.method == "POST":
            if expected_type is bool:
                raw = request.form.get(field_name, None)
                value = self._convert("on" if raw is not None else "", bool)
            else:
                raw = request.form.get(field_name, "")
                value = self._convert(raw, expected_type)
            setattr(obj, field_name, value)

    def write_field(self, obj, field_name):
        value = getattr(obj, field_name, None)
        return f"{field_name}: {str(value)}"
    
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
        lines = [f"<h2>{title}</h2>", f'<form method="post" action="{action_url}">']
        
        for fname, ftype in obj.FIELDS.items():
            input_type = self._input_type_for(ftype)
            display_name = fname
            lines.append(f'<p>{display_name}:')
            
            if input_type == "checkbox":
                checked = " checked" if getattr(obj, fname, False) else ""
                lines.append(f'<input type="checkbox" name="{fname}"{checked}>')
            else:
                value = getattr(obj, fname, "")
                lines.append(f'<input type="{input_type}" name="{fname}" value="{str(value)}">')
            lines.append("</p>")
        
        cancel_url = cancel_url or "/"
        lines.extend([
            f'<p><button type="submit">{submit_text}</button> <a href="{cancel_url}">Отмена</a></p>',
            "</form>"
        ])
        return Markup("\n".join(lines))
    
    def build_table_html(self, items_with_ids=None, url_for_func=None):
        items = items_with_ids if items_with_ids else []
        if not items:
            return Markup("<p>Список пуст</p>")
        
        items_list = items if isinstance(items[0], tuple) else [
            (obj, i) for i, obj in enumerate(items)
        ]
        
        lines = ['<table border="1">', "<tr><th>#</th><th>Тип</th><th>Данные</th><th>Действия</th></tr>"]
        
        for i, (obj, item_id) in enumerate(items_list):
            field_parts = [
                f"{fname}: {getattr(obj, fname, '')}"
                for fname in obj.FIELDS.keys()
            ]
            fields_str = "<br>".join(field_parts)
            type_display = obj.__class__.__name__
            
            if url_for_func:
                edit_url = url_for_func('st0114.edit_item', item_id=item_id)
                delete_url = url_for_func('st0114.delete_item', item_id=item_id)
            else:
                edit_url = f'/edit/{item_id}'
                delete_url = f'/delete/{item_id}'
            
            lines.extend([
                "<tr>",
                f"<td>{i+1}</td>",
                f"<td>{type_display}</td>",
                f"<td>{fields_str}</td>",
                f"<td><a href='{edit_url}'>Редактировать</a> | <a href='{delete_url}'>Удалить</a></td>",
                "</tr>"
            ])
        
        lines.append("</table>")
        return Markup("\n".join(lines))
