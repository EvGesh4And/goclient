from flask import request


class FlaskIO:
    def input_field(self, field_name, default=""):
        return request.form.get(field_name, default).strip()

    def field_html(self, name, label, value=""):
        return f"""
        <div class="mb-3">
            <label for="{name}" class="form-label">{label}:</label>
            <input type="text" class="form-control" id="{name}" name="{name}" value="{value}" required>
        </div>
        """
