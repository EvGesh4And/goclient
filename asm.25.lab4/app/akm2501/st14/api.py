from typing import Any, Dict

from flask import abort, jsonify, request
from werkzeug.exceptions import HTTPException

from . import bp
from .flask_io import FlaskIO
from .group_container import GroupContainer
from .sqlite_storage import SQLiteStorage


def _get_container() -> GroupContainer:
    io = FlaskIO()
    container = GroupContainer(io=io, storage=None)
    storage = SQLiteStorage(type_registry=container.type_names)
    container.storage = storage
    container.load()
    return container


def _serialize(obj, item_id: int) -> Dict[str, Any]:
    data: Dict[str, Any] = {"id": item_id, "type": obj.__class__.__name__}
    for field_name in obj.FIELDS.keys():
        data[field_name] = getattr(obj, field_name, None)
    return data


@bp.route("/api/meta", methods=["GET"])
def meta():
    container = _get_container()
    types_description = {}
    for name, cls in container.type_names.items():
        fields = {field: field_type.__name__ for field, field_type in cls.FIELDS.items()}
        types_description[name] = {"fields": fields}
    return jsonify({"types": types_description})


@bp.route("/api/employees", methods=["GET"])
def list_employees():
    container = _get_container()
    data = [_serialize(obj, i) for i, obj in enumerate(container.items)]
    return jsonify({"employees": data})


@bp.route("/api/employees/<int:item_id>", methods=["GET"])
def get_employee(item_id: int):
    container = _get_container()
    if not (0 <= item_id < len(container.items)):
        abort(404, description="Сотрудник не найден")
    return jsonify(_serialize(container.items[item_id], item_id))


@bp.route("/api/employees", methods=["POST"])
def create_employee():
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        abort(400, description="Ожидается JSON-объект")

    type_name = payload.get("type")
    container = _get_container()
    if not type_name or type_name not in container.type_names:
        abort(400, description="Неизвестный тип сотрудника")
    if container.add_item(type_name=type_name, json_data=payload):
        container.save()
        new_id = len(container.items) - 1
        return jsonify(_serialize(container.items[new_id], new_id)), 201
    abort(400, description="Не удалось создать запись")


@bp.route("/api/employees/<int:item_id>", methods=["PUT"])
def update_employee(item_id: int):
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        abort(400, description="Ожидается JSON-объект")

    container = _get_container()
    if not (0 <= item_id < len(container.items)):
        abort(404, description="Сотрудник не найден")

    if container.edit_item(idx=item_id, json_data=payload, partial=False):
        container.save()
        return jsonify(_serialize(container.items[item_id], item_id))
    abort(400, description="Не удалось обновить запись")


@bp.route("/api/employees/<int:item_id>", methods=["PATCH"])
def patch_employee(item_id: int):
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        abort(400, description="Ожидается JSON-объект")

    container = _get_container()
    if not (0 <= item_id < len(container.items)):
        abort(404, description="Сотрудник не найден")

    if container.edit_item(idx=item_id, json_data=payload, partial=True):
        container.save()
        return jsonify(_serialize(container.items[item_id], item_id))
    abort(400, description="Не удалось обновить запись")


@bp.route("/api/employees/<int:item_id>", methods=["DELETE"])
def delete_employee(item_id: int):
    container = _get_container()
    if not (0 <= item_id < len(container.items)):
        abort(404, description="Сотрудник не найден")
    if container.remove_item(idx=item_id):
        container.save()
        return ("", 204)
    abort(404, description="Сотрудник не найден")


@bp.route("/api/employees", methods=["DELETE"])
def clear_employees():
    container = _get_container()
    count = len(container.items)
    container.clear()
    container.save()
    return jsonify({"removed": count, "previous_count": count})


@bp.errorhandler(HTTPException)
def handle_http_error(error: HTTPException):
    response = jsonify({
        "error": error.name,
        "message": error.description,
        "status": error.code,
    })
    return response, error.code


@bp.errorhandler(Exception)
def handle_unexpected_error(error: Exception):
    response = jsonify({
        "error": "Internal Server Error",
        "message": str(error),
        "status": 500,
    })
    return response, 500
