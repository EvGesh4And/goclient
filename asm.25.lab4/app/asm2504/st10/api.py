from flask import request, jsonify, abort
from typing import Dict, Any
from threading import Lock

def register_api(bp):
    def _validate_entry(e: Any) -> bool:
        return isinstance(e, dict) and "__class__" in e and "data" in e and isinstance(e["data"], dict)

    @bp.route("/api/members", methods=["GET"])
    def api_get_members():
        with Lock():
            members = bp.cont.storage.list()
            return jsonify([serialize_member(m) for m in members]), 200

    @bp.route("/api/members/<int:index>", methods=["GET"])
    def api_get_member(index: int):
        with Lock():
            members = bp.cont.storage.list()
            if not (0 <= index < len(members)):
                return abort(404, "Индекс вне диапазона")
            return jsonify(serialize_member(members[index])), 200
        
    @bp.route("/api/members/add", methods=["POST"])
    def api_add_member():
        entry = request.get_json(force=True)
        if not _validate_entry(entry):
            return abort(400, "Неверная запись")
        with Lock():
            obj = deserialize_entry_to_obj(entry)
            bp.cont.storage.add(obj)
            idx = len(bp.cont.storage.list()) - 1
        return jsonify({"ok": True, "index": idx}), 201

    @bp.route("/api/members/clear_list", methods=["POST"])
    def api_clear_list():
        with Lock():
            bp.cont.clear_with_message()
        return jsonify({"ok": True}), 201
        
    @bp.route("/api/members/edit/<int:index>", methods=["PUT"])
    def api_put_member(index: int):
        entry = request.get_json(force=True)
        if not _validate_entry(entry):
            return abort(400, "Неверная запись")
        with Lock():
            members = bp.cont.storage.list()
            if not (0 <= index < len(members)):
                return abort(404, "Индекс вне диапазона")
            obj = deserialize_entry_to_obj(entry)
            print(index)
            bp.cont.storage.update(index, obj)
        return jsonify({"ok": True, "index": index}), 200

    @bp.route("/api/members/remove/<int:index>", methods=["DELETE"])
    def api_remove_member(index: int):
        with Lock():
            members = bp.cont.storage.list()
            if not (0 <= index < len(members)):
                return abort(404, "Индекс вне диапазона")
            removed = bp.cont.storage.remove(index)
        return jsonify({"ok": True, "removed": serialize_member(removed) if removed is not None else None}), 200

    @bp.route("/api/members/save/<name>", methods=["POST"])
    def api_save_members(name: str):
        with Lock():
            try:
                bp.cont.storage.save(name)
            except Exception as e:
                return abort(500, str(e))
        return jsonify({"ok": True, "saved": name}), 200

    @bp.route("/api/members/load/<name>", methods=["GET"])
    def api_load_members(name: str):
        with Lock():
            try:
                bp.cont.storage.load(name)
            except Exception as e:
                return abort(500, str(e))
            members = bp.cont.storage.list()
            return jsonify([serialize_member(m) for m in members]), 200

    def serialize_member(obj: Any) -> Dict[str, Any]:
        if hasattr(obj, "to_serialized"):
            return obj.to_serialized()
        data = getattr(obj, "_data", None)
        if data is None and hasattr(obj, "__dict__"):
            data = {k: v for k, v in obj.__dict__.items() if not k.startswith("_")}
        return {"__class__": getattr(obj, "TYPE_NAME", type(obj).__name__), "data": data or {}}

    def deserialize_entry_to_obj(entry: Dict[str, Any]):
        cls_name = entry.get("__class__")
        data = entry.get("data", {})
        cls = None
        for c in bp.cont.classes:
            if getattr(c, "TYPE_NAME", c.__name__) == cls_name or c.__name__ == cls_name:
                cls = c
                break
        if cls is None:
            raise ValueError(f"Неизвестный класс: {cls_name}")
        obj = cls()
        if hasattr(cls, "from_serialized"):
            return cls.from_serialized(data)
        try:
            bp.cont.update_fields_obj(obj, data)
        except Exception as e:
            obj._data = data
        return obj
