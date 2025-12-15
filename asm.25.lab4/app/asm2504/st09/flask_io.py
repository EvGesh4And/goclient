from flask import request
from markupsafe import escape


class FlaskIO:

    def __init__(self):
        self._form_data = None  

    def set_form_data(self, form_data):
        self._form_data = form_data

    def input_field(self, field_name: str, label: str) -> str:
        if self._form_data is not None:
            return self._form_data.get(field_name, "")
        return request.form.get(field_name, "")

    def field_html(self, field_name: str, label: str, value: str = "") -> str:
        val = escape(value) if value is not None else ""
        return f'''
        <div class="form-row">
            <label for="{field_name}">{label}:</label><br>
            <input type="text" id="{field_name}" name="{field_name}" value="{val}" required>
        </div>
        <br>
        '''
