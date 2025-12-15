from typing import Any, Dict

from flask import abort, jsonify, request
from werkzeug.exceptions import HTTPException

from . import bp
from .registry import TYPE_REGISTRY, get_type
from .sqlite_storage import SQLiteStorage

BOOLEAN_TRUE = {"true", "1", "yes", "y", "on"}


def _storage() -> SQLiteStorage:
    return SQLiteStorage()


def _serialize(obj, item_id: int) -> Dict[str, Any]:
    data: Dict[str, Any] = {"id": item_id, "type": obj.__class__.__name__}
    for field_name in obj.FIELDS.keys():
        data[field_name] = getattr(obj, field_name, None)
    return data


def _convert_value(value: Any, field_type):
    if field_type is bool:
        if isinstance(value, bool):
            return value
        if value is None:
            return False
        if isinstance(value, (int, float)):
            return bool(value)
        if isinstance(value, str):
            return value.strip().lower() in BOOLEAN_TRUE
        abort(400, description="Некорректное булево значение")
    try:
        return field_type(value)
    except (TypeError, ValueError):
        if field_type is str:
            return "" if value is None else str(value)
        abort(400, description=f"Поле должно иметь тип {field_type.__name__}")


def _build_object(payload: Dict[str, Any], *, existing=None, partial: bool = False):
    if "type" in payload or existing is None:
        type_name = payload.get("type")
    else:
        type_name = existing.__class__.__name__
    cls = get_type(type_name) if type_name else None
    if cls is None:
        abort(400, description="Неизвестный тип студента")

    obj = existing if (existing is not None and existing.__class__ is cls) else cls()
    missing = []

    for field_name, field_type in obj.FIELDS.items():
        if field_name in payload:
            value = _convert_value(payload[field_name], field_type)
            setattr(obj, field_name, value)
        elif not partial:
            missing.append(field_name)

    if missing:
        abort(400, description=f"Отсутствуют обязательные поля: {', '.join(missing)}")

    if hasattr(obj, "age") and obj.age is not None:
        try:
            if int(obj.age) < 0:
                abort(400, description="Возраст не может быть отрицательным")
        except (ValueError, TypeError):
            abort(400, description="Возраст должен быть целым числом")

    return obj


@bp.route("/api/meta", methods=["GET"])
def meta():
    types_description = {}
    for name, cls in TYPE_REGISTRY.items():
        fields = {field: field_type.__name__ for field, field_type in cls.FIELDS.items()}
        types_description[name] = {"fields": fields}
    return jsonify({"types": types_description})


@bp.route("/api/students", methods=["GET"])
def list_students():
    storage = _storage()
    items = storage.get_all_with_ids()
    data = [_serialize(obj, item_id) for obj, item_id in items]
    return jsonify({"students": data})


@bp.route("/api/students/<int:item_id>", methods=["GET"])
def get_student(item_id: int):
    storage = _storage()
    obj = storage.get_by_id(item_id)
    if obj is None:
        abort(404, description="Студент не найден")
    return jsonify(_serialize(obj, item_id))


@bp.route("/api/students", methods=["POST"])
def create_student():
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        abort(400, description="Ожидается JSON-объект")

    obj = _build_object(payload)
    storage = _storage()
    new_id = storage.add(obj)
    if new_id is None:
        abort(500, description="Не удалось создать запись")

    return jsonify(_serialize(obj, new_id)), 201


@bp.route("/api/students/<int:item_id>", methods=["PUT"])
def update_student(item_id: int):
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        abort(400, description="Ожидается JSON-объект")

    storage = _storage()
    existing = storage.get_by_id(item_id)
    if existing is None:
        abort(404, description="Студент не найден")

    obj = _build_object(payload, existing=existing, partial=False)
    if not storage.update_by_id(item_id, obj):
        abort(500, description="Не удалось обновить запись")

    return jsonify(_serialize(obj, item_id))


@bp.route("/api/students/<int:item_id>", methods=["PATCH"])
def patch_student(item_id: int):
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        abort(400, description="Ожидается JSON-объект")

    storage = _storage()
    existing = storage.get_by_id(item_id)
    if existing is None:
        abort(404, description="Студент не найден")

    obj = _build_object(payload, existing=existing, partial=True)
    if not storage.update_by_id(item_id, obj):
        abort(500, description="Не удалось обновить запись")

    return jsonify(_serialize(obj, item_id))


@bp.route("/api/students/<int:item_id>", methods=["DELETE"])
def delete_student(item_id: int):
    storage = _storage()
    if not storage.remove_by_id(item_id):
        abort(404, description="Студент не найден")
    return ("", 204)


@bp.route("/api/students", methods=["DELETE"])
def clear_students():
    storage = _storage()
    count = len(storage.get_all())
    removed = storage.clear()
    return jsonify({"removed": removed, "previous_count": count})


@bp.errorhandler(HTTPException)
def handle_http_error(error: HTTPException):
    response = jsonify(
        {
            "error": error.name,
            "message": error.description,
            "status": error.code,
        }
    )
    return response, error.code


@bp.errorhandler(Exception)
def handle_unexpected_error(error: Exception):
    response = jsonify(
        {
            "error": "Internal Server Error",
            "message": str(error),
            "status": 500,
        }
    )
    return response, 500

