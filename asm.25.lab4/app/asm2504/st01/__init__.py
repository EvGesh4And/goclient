from flask import Blueprint, render_template, request, redirect, url_for, g, jsonify
from .storage import (
    init_db,
    get_all_entities,
    add_entity,
    update_entity,
    delete_entity,
    clear_all,
    get_entity_by_id,
)
from .flask_io import FlaskIO
from .entity import Student, Starosta, Proforg
from .import_pickle import import_from_lr1
import os

template_dir = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    "templates",
    "asm2504",
    "st01",
)

bp = Blueprint("st0401", __name__, template_folder=template_dir)
io = FlaskIO()
init_db()

# Импорт данных из ЛР1 при первом запуске
import_from_lr1()

print(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
@bp.route("/")
def index():
    entities = get_all_entities()
    type_names = {"student": "Студент", "starosta": "Староста", "proforg": "Профорг", "Student": "Студент", "Starosta": "Староста"}
    return render_template("asm2504/st01/list.html", entities=entities, type_names=type_names)


@bp.route("/add", methods=["GET"])
def add_type():
    return render_template("asm2504/st01/add.html")


@bp.route("/add_form", methods=["GET", "POST"])
def add_form():
    entity_type = request.args.get("type") or request.form.get("type")
    if entity_type not in ["student", "starosta", "proforg"]:
        return "Неверный тип", 400

    ent_class = {"student": Student, "starosta": Starosta, "proforg": Proforg}[
        entity_type
    ]
    ent = ent_class(io)
    error = None

    if request.method == "POST":
        try:
            ent.read_fields()
            ent.validate_and_save()
            data = {
                "type": entity_type,
                "name": ent.name,
                "age": ent.age,
                "group_role": getattr(ent, "group_role", ""),
                "union_activity": getattr(ent, "union_activity", ""),
            }
            add_entity(data)
            return redirect(url_for("st0401.index"))
        except ValueError as e:
            error = str(e)

    return render_template(
        "asm2504/st01/form.html", form_html=ent.generate_form(), entity_type=entity_type, error=error
    )


@bp.route("/edit/<int:entity_id>", methods=["GET", "POST"])
def edit(entity_id):
    ent_row = get_entity_by_id(entity_id)
    # ent_row = next((e for e in entities if e["id"] == entity_id), None)
    if not ent_row:
        return "Не найдено", 404

    ent_class = {"student": Student, "starosta": Starosta, "proforg": Proforg}[
        ent_row["type"]
    ]
    ent = ent_class(io)
    ent.name = ent_row["name"]
    ent.age = ent_row["age"]
    if hasattr(ent, "group_role"):
        ent.group_role = ent_row["group_role"] or ""
    if hasattr(ent, "union_activity"):
        ent.union_activity = ent_row["union_activity"] or ""

    error = None
    if request.method == "POST":
        try:
            ent.read_fields()
            ent.validate_and_save()
            data = {
                "name": ent.name,
                "age": ent.age,
                "group_role": getattr(ent, "group_role", ""),
                "union_activity": getattr(ent, "union_activity", ""),
            }
            update_entity(entity_id, data)
            return redirect(url_for("st0401.index"))
        except ValueError as e:
            error = str(e)

    return render_template(
        "asm2504/st01/form.html",
        form_html=ent.generate_form(),
        entity_type=ent_row["type"],
        entity_id=entity_id,
        error=error,
    )
#request.url_rule.rule.split('/')[1]

@bp.route("/delete/<int:entity_id>")
def delete(entity_id):
    delete_entity(entity_id)
    return redirect(url_for("st0401.index"))


@bp.route("/clear")
def clear():
    clear_all()
    return redirect(url_for("st0401.index"))


# API endpoints
@bp.route("/api/", methods=["GET"])
def api_get_all():
    entities = get_all_entities()
    return jsonify([dict(e) for e in entities])


@bp.route("/api/", methods=["POST"])
def api_add():
    data = request.get_json()
    entity_id = add_entity(data)
    return jsonify({"id": entity_id}), 201


@bp.route("/api/<int:entity_id>", methods=["PUT"])
def api_update(entity_id):
    data = request.get_json()
    update_entity(entity_id, data)
    return jsonify({"status": "ok"})


@bp.route("/api/<int:entity_id>", methods=["DELETE"])
def api_delete(entity_id):
    delete_entity(entity_id)
    return jsonify({"status": "ok"})


@bp.route("/api/clear", methods=["POST"])
def api_clear():
    clear_all()
    return jsonify({"status": "ok"})


@bp.route("/api/st2/", methods=["GET"])
def api_get_students():
    entities = get_all_entities()
    students = [dict(e) for e in entities if e['type'] == 'student']
    return jsonify(students)
