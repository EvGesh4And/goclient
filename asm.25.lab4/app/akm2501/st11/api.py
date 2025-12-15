import datetime
from typing import Any, Dict

from flask import abort, jsonify, request
from werkzeug.exceptions import HTTPException

from . import bp
from .models import Animal, Herbivore, Predator
from .storage import SQLiteStorage

TYPE_MAP = {
    Animal.__name__: Animal,
    Predator.__name__: Predator,
    Herbivore.__name__: Herbivore,
}

storage = SQLiteStorage(type_resolver=lambda n: TYPE_MAP.get(n))


def _serialize(obj: Animal) -> Dict[str, Any]:
    data: Dict[str, Any] = {
        "id": obj.id,
        "type": obj.__class__.__name__,
    }
    for field in obj.fields():
        value = getattr(obj, field, "")
        if isinstance(value, datetime.datetime):
            value = value.isoformat()
        data[field] = value
    return data


def _build_object(payload: Dict[str, Any], *, existing: Animal | None = None, partial: bool = False) -> Animal:
    type_name = payload.get("type") if existing is None else payload.get("type", existing.__class__.__name__)
    cls = TYPE_MAP.get(type_name)
    if cls is None:
        abort(400, description="Неизвестный тип животного")

    obj = existing if existing is not None and existing.__class__ is cls else cls()

    missing = []
    for field in obj.fields():
        if field == "time":
            continue
        if field in payload:
            setattr(obj, field, str(payload[field]))
        elif not partial:
            missing.append(field)

    if missing:
        abort(400, description=f"Отсутствуют поля: {', '.join(missing)}")

    obj.time = datetime.datetime.now()
    return obj


@bp.route("/api/meta", methods=["GET"])
def api_meta():
    description = {}
    for name, cls in TYPE_MAP.items():
        description[name] = {"fields": [field for field in cls.fields() if field != "time"]}
    return jsonify({"types": description})


@bp.route("/api/animals", methods=["GET"])
def api_list_animals():
    items = storage.get_all_with_ids()
    result = []
    for item_id, obj in items:
        obj.id = item_id
        result.append(_serialize(obj))
    return jsonify({"animals": result})


@bp.route("/api/animals/<string:item_id>", methods=["GET"])
def api_get_animal(item_id: str):
    obj = storage.get_by_id(item_id)
    if obj is None:
        abort(404, description="Животное не найдено")
    obj.id = item_id
    return jsonify(_serialize(obj))


@bp.route("/api/animals", methods=["POST"])
def api_create_animal():
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        abort(400, description="Ожидается JSON-объект")

    obj = _build_object(payload)
    new_id = storage.add(obj)
    if not new_id:
        abort(500, description="Не удалось создать запись")
    return jsonify(_serialize(obj)), 201


@bp.route("/api/animals/<string:item_id>", methods=["PUT"])
def api_update_animal(item_id: str):
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        abort(400, description="Ожидается JSON-объект")

    existing = storage.get_by_id(item_id)
    if existing is None:
        abort(404, description="Животное не найдено")

    obj = _build_object(payload, existing=existing, partial=False)
    storage.update_by_id(item_id, obj)
    obj.id = item_id
    return jsonify(_serialize(obj))


@bp.route("/api/animals/<string:item_id>", methods=["PATCH"])
def api_patch_animal(item_id: str):
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        abort(400, description="Ожидается JSON-объект")

    existing = storage.get_by_id(item_id)
    if existing is None:
        abort(404, description="Животное не найдено")

    obj = _build_object(payload, existing=existing, partial=True)
    storage.update_by_id(item_id, obj)
    obj.id = item_id
    return jsonify(_serialize(obj))


@bp.route("/api/animals/<string:item_id>", methods=["DELETE"])
def api_delete_animal(item_id: str):
    if not storage.delete_by_id(item_id):
        abort(404, description="Животное не найдено")
    return ("", 204)


@bp.route("/api/animals", methods=["DELETE"])
def api_clear_animals():
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


