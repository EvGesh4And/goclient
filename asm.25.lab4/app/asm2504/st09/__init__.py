from flask import Blueprint, render_template, request, redirect, url_for, send_file, jsonify, make_response
from .storage import SQLiteStorage
from .flask_io import FlaskIO
from .entity import Worker, Manager, Director
import os
import tempfile

bp = Blueprint('st0409', __name__, url_prefix='/st8',
               template_folder=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                                            'templates', 'asm2504', 'st09'))
storage = SQLiteStorage()


# --- вспомогательная функция ---
def create_employee_from_form(emp_type, form_data):
    io = FlaskIO()
    io.set_form_data(form_data)

    cls_map = {
        'Worker': Worker,
        'Manager': Manager,
        'Director': Director
    }
    cls = cls_map.get(emp_type, Worker)
    emp = cls(io)
    emp.input_fields()
    return emp


# --- маршруты HTML ---
@bp.route('/')
def main():
    employees = storage.get_all_entities()
    message = request.args.get("message")
    return render_template('asm2504/st09/index.html', employees=employees, message=message)


@bp.route('/add', methods=['GET', 'POST'])
def add_employee():
    cls_map = {"Worker": Worker, "Manager": Manager, "Director": Director}
    emp_type = request.values.get("type", "Worker")

    io = FlaskIO()
    emp_class = cls_map.get(emp_type, Worker)
    emp = emp_class(io)

    if request.method == "POST" and "save" in request.form:
        emp = create_employee_from_form(emp_type, request.form)
        storage.add_employee(emp)
        return redirect(url_for('st0409.main'))

    form_html = emp.generate_form()
    return render_template(
        'asm2504/st09/add.html',
        title="Добавить сотрудника",
        form_fields=form_html,
        emp_type=emp_type,
        is_edit=False
    )


@bp.route('/edit/<int:emp_id>', methods=['GET', 'POST'])
def edit_employee(emp_id):
    employees = storage.get_all_entities()
    emp = next((e for e in employees if getattr(e, "db_id", None) == emp_id), None)

    if emp is None:
        return redirect(url_for('st0409.main', message="Сотрудник не найден."))

    emp_type = emp.__class__.__name__

    if request.method == 'POST':
        updated_emp = create_employee_from_form(emp_type, request.form)
        storage.update_employee(emp_id, updated_emp)
        return redirect(url_for('st0409.main', message="Сотрудник обновлён."))

    io = FlaskIO()
    emp.io = io
    form_html = emp.generate_form() if hasattr(emp, "generate_form") else "<p>Ошибка формы</p>"

    return render_template(
        'asm2504/st09/edit.html',
        employee=emp,
        form_fields=form_html,
        emp_type=emp_type,
        emp_id=emp_id
    )


@bp.route('/delete/<int:emp_id>', methods=['POST'])
def delete_employee(emp_id):
    try:
        storage.remove_employee(emp_id)
        return redirect(url_for('st0409.main', message="Сотрудник удалён."))
    except Exception as e:
        return redirect(url_for('st0409.main', message=f"Ошибка при удалении: {e}"))


@bp.route('/clear', methods=['POST'])
def clear_all():
    storage.clear_all()
    return redirect(url_for('st0409.main', message="База данных очищена."))


# --- Выгрузка в файл ---
@bp.route("/download", methods=["GET"])
def download_file():
    tmp_path = os.path.join(tempfile.gettempdir(), "employees.pkl")
    storage.export_to_pickle(tmp_path)
    return send_file(tmp_path, as_attachment=True, download_name="employees.pkl")


# --- Загрузка из файла ---
@bp.route("/upload", methods=["POST"])
def upload_file():
    file = request.files.get("file")
    if not file:
        return redirect(url_for("st0409.main"))

    tmp_path = os.path.join(tempfile.gettempdir(), "employees.pkl")
    file.save(tmp_path)
    storage.import_from_pickle(tmp_path)

    return redirect(url_for("st0409.main"))


# REST API

def employee_to_dict(emp):
    """Сериализация сотрудника"""
    data = emp.__dict__.copy()
    data["id"] = getattr(emp, "db_id", None)
    data["type"] = emp.__class__.__name__
    return data


def create_employee_from_dict(data):
    """Создание сотрудника из JSON (API-вариант)"""
    t = data.get("type", "Worker")
    cls_map = {
        "Worker": Worker,
        "Manager": Manager,
        "Director": Director
    }
    cls = cls_map.get(t, Worker)
    io = FlaskIO()
    emp = cls(io)

    for k, v in data.items():
        if hasattr(emp, k):
            setattr(emp, k, v)

    return emp


# ---- API: список ----
@bp.route("/api/items", methods=["GET"])
def api_list_items():
    employees = storage.get_all_entities()
    rows = [employee_to_dict(e) for e in employees]
    return jsonify(rows)


# ---- API: создать ----
@bp.route("/api/items", methods=["POST"])
def api_create_item():
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "Invalid JSON"}), 400

    emp = create_employee_from_dict(data)
    new_id = storage.add_employee(emp)

    return jsonify({"id": new_id, "row": employee_to_dict(emp)}), 201


# ---- API: получить одного ----
@bp.route("/api/items/<int:emp_id>", methods=["GET"])
def api_get_item(emp_id):
    employees = storage.get_all_entities()
    emp = next((e for e in employees if getattr(e, "db_id", None) == emp_id), None)

    if emp is None:
        return jsonify({"error": "not found"}), 404

    return jsonify(employee_to_dict(emp))


# ---- API: обновить ----
@bp.route("/api/items/<int:emp_id>", methods=["PUT", "POST"])
def api_update_item(emp_id):
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "Invalid JSON"}), 400

    emp = create_employee_from_dict(data)

    try:
        storage.update_employee(emp_id, emp)
    except Exception:
        return jsonify({"error": "not found"}), 404

    return jsonify({"ok": True, "row": employee_to_dict(emp)})


# ---- API: удалить ----
@bp.route("/api/items/<int:emp_id>", methods=["DELETE"])
def api_delete_item(emp_id):
    try:
        storage.remove_employee(emp_id)
    except Exception:
        return jsonify({"error": "not found"}), 404

    return jsonify({"ok": True})
