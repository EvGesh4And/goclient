from flask import Blueprint, render_template, request, redirect, url_for, jsonify, make_response
import os
try:
    from .camera import Camera
    from .lens import Lens
    from .equipment import Equipment
    from .io_strategy import FlaskIO, RestIO
    from .storage_sqlite import SQLiteStorage
except Exception:
    from camera import Camera
    from lens import Lens
    from equipment import Equipment
    from io_strategy import FlaskIO, RestIO
    from storage_sqlite import SQLiteStorage

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
DATA_FOLDER = os.path.join(PROJECT_ROOT, "data", "asm2504", "st06")
os.makedirs(DATA_FOLDER, exist_ok=True)

bp = Blueprint(
    'st0406',
    __name__,
    url_prefix='/st06',
    template_folder=os.path.join(PROJECT_ROOT, 'app', 'templates', 'asm2504', 'st06')
)

@bp.app_template_global('getattr')
def _template_getattr(obj, name, default=None):
    return getattr(obj, name, default)

storage = SQLiteStorage()
# создаём две стратегии: для web-форм и для REST
io_web = FlaskIO()   # используем для HTML-форм (endpoints /, /add, /edit etc.)
io_rest = RestIO()   # используем для API (/api/*)


def make_empty(kind: str):
    if kind == "camera":
        return Camera()
    elif kind == "lens":
        return Lens()
    else:
        return Equipment()

@bp.route("/")
def index():
    rows = storage.list_items()
    items = []
    for r in rows:
        if r.get("type") == "lens":
            obj = Lens.from_row(r)
        else:
            obj = Camera.from_row(r)
        obj.set_io(io_web)
        items.append(obj)
    return render_template("asm2504/st06/list.html", items=items)

@bp.route("/add/<kind>", methods=["GET", "POST"])
def add(kind):
    if kind not in ("camera", "lens"):
        return redirect(url_for(".index"))
    obj = make_empty(kind)
    if request.method == "POST":
        io_web.assign_fields(obj, request)
        storage.add_item(obj.to_row())
        return redirect(url_for(".index"))
    defs = obj.get_field_defs()
    return render_template("asm2504/st06/form.html",
                           action=url_for(".add", kind=kind),
                           defs=defs, obj=obj, kind=kind)

@bp.route("/edit/<int:idx>", methods=["GET", "POST"])
def edit(idx):
    row = storage.get_item(idx)
    if row is None:
        return redirect(url_for(".index"))
    obj = Camera.from_row(row) if row.get("type") == "camera" else Lens.from_row(row)
    if request.method == "POST":
        io_web.assign_fields(obj, request)
        storage.update_item(idx, obj.to_row())
        return redirect(url_for(".index"))
    defs = obj.get_field_defs()
    return render_template("asm2504/st06/form.html",
                           action=url_for(".edit", idx=idx),
                           defs=defs, obj=obj, kind=type(obj).__name__.lower())

@bp.route("/delete/<int:idx>", methods=["POST"])
def delete(idx):
    storage.delete_item(idx)
    return redirect(url_for(".index"))

@bp.route("/save", methods=["POST"])
def save():
    fn = request.form.get("filename", "data.pickle")
    full_path = os.path.join(DATA_FOLDER, fn)
    ok, msg = storage.save(full_path)
    return redirect(url_for(".index"))

@bp.route("/load", methods=["POST"])
def load():
    fn = request.form.get("filename", "data.pickle")
    full_path = os.path.join(DATA_FOLDER, fn)
    ok, msg = storage.load(full_path)
    return redirect(url_for(".index"))

@bp.route("/clear", methods=["POST"])
def clear():
    storage.clear()
    return redirect(url_for(".index"))


# ---------------- REST API ----------------
@bp.route("/api/items", methods=["GET"])
def api_list_items():
    rows = storage.list_items()
    return jsonify(rows)


@bp.route("/api/items", methods=["POST"])
def api_create_item():
    data = io_rest.extract(request)

    t = Equipment.detect_type(data)
    if t == "lens":
        obj = Lens.from_row(data)
    else:
        obj = Camera.from_row(data)

    new_id = storage.add_item(obj.to_row())
    row = obj.to_row()
    return make_response(jsonify({"id": new_id, "row": row}), 201)


@bp.route("/api/items/<int:idx>", methods=["GET"])
def api_get_item(idx):
    row = storage.get_item(idx)
    if row is None:
        return make_response(jsonify({"error": "not found"}), 404)
    return jsonify(row)


@bp.route("/api/items/<int:idx>", methods=["PUT", "POST"])
def api_update_item(idx):
    data = io_rest.extract(request)

    t = Equipment.detect_type(data)
    obj = Lens.from_row(data) if t == "lens" else Camera.from_row(data)
    ok = storage.update_item(idx, obj.to_row())

    if not ok:
        return make_response(jsonify({"error": "not found"}), 404)
    return jsonify({"ok": True, "row": obj.to_row()})


@bp.route("/api/items/<int:idx>", methods=["DELETE"])
def api_delete_item(idx):
    ok = storage.delete_item(idx)
    if not ok:
        return make_response(jsonify({"error": "not found"}), 404)
    return jsonify({"ok": True})
