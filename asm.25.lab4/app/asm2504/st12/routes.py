import os
import pickle
import sqlite3
import tempfile

from flask import redirect, render_template, request, url_for

from . import bp
from .db import ST12_DIR, get_connection
from .flask_io import FlaskIO
from .registry import TYPE_REGISTRY, get_type
from .sqlite_storage import SQLiteStorage


def _make_storage() -> SQLiteStorage:
    return SQLiteStorage()


def _make_io() -> FlaskIO:
    return FlaskIO()


@bp.route("/list")
def list_items():
    storage = _make_storage()
    io = _make_io()
    items_with_ids = storage.get_all_with_ids()
    table_html = io.build_table_html(items_with_ids, url_for_func=url_for)
    return render_template(
        "asm2504/st12/list.html",
        table_html=table_html,
        count=len(items_with_ids),
    )


@bp.route("/add")
def add_choose():
    io = _make_io()
    type_pairs = [(name, io.TYPE_NAMES.get(name, name)) for name in TYPE_REGISTRY.keys()]
    return render_template(
        "asm2504/st12/page.html",
        page_type="add_choose",
        title="Выберите тип студента",
        types=type_pairs,
    )


@bp.route("/add/<type_name>", methods=["GET", "POST"])
def add_item(type_name):
    cls = get_type(type_name)
    if cls is None:
        return render_template(
            "asm2504/st12/message.html",
            title="Ошибка",
            message="Неверный тип",
            back_url=url_for("st0412.add_choose"),
        )

    io = _make_io()
    storage = _make_storage()

    if request.method == "POST":
        obj = cls()
        io.fill_object_from_form(obj, request.form)
        storage.add(obj)
        return redirect(url_for("st0412.list_items"))

    form_html = io.build_form_html(
        cls(),
        url_for("st0412.add_item", type_name=type_name),
        f"Добавление: {type_name}",
        "Добавить",
        url_for("st0412.list_items"),
    )
    return render_template("asm2504/st12/form.html", form_html=form_html)


@bp.route("/edit/<int:item_id>", methods=["GET", "POST"])
def edit_item(item_id):
    storage = _make_storage()
    obj = storage.get_by_id(item_id)
    if obj is None:
        return render_template(
            "asm2504/st12/message.html",
            title="Ошибка",
            message="Студент не найден",
            back_url=url_for("st0412.list_items"),
        )

    io = _make_io()
    if request.method == "POST":
        io.fill_object_from_form(obj, request.form)
        storage.update_by_id(item_id, obj)
        return redirect(url_for("st0412.list_items"))

    form_html = io.build_form_html(
        obj,
        url_for("st0412.edit_item", item_id=item_id),
        f"Редактирование: {obj.__class__.__name__}",
        "Сохранить",
        url_for("st0412.list_items"),
    )
    return render_template("asm2504/st12/form.html", form_html=form_html)


@bp.route("/view/<int:item_id>")
def view_item(item_id):
    storage = _make_storage()
    obj = storage.get_by_id(item_id)
    if obj is None:
        return render_template(
            "asm2504/st12/message.html",
            title="Ошибка",
            message="Студент не найден",
            back_url=url_for("st0412.list_items"),
        )
    
    io = _make_io()
    # Format field values for display
    field_data = []
    for fname, ftype in obj.FIELDS.items():
        value = getattr(obj, fname, None)
        if ftype is bool:
            display_value = "да" if value else "нет"
        elif ftype is float:
            display_value = f"{value:.2f}" if value is not None else "0.00"
        else:
            display_value = str(value) if value is not None else "—"
        field_data.append({
            "name": io.FIELD_NAMES.get(fname, fname),
            "value": display_value
        })
    
    return render_template(
        "asm2504/st12/view.html",
        obj=obj,
        item_id=item_id,
        field_data=field_data,
        type_name=io.TYPE_NAMES.get(obj.__class__.__name__, obj.__class__.__name__),
    )


@bp.route("/delete/<int:item_id>")
def delete_item(item_id):
    storage = _make_storage()
    storage.remove_by_id(item_id)
    return redirect(url_for("st0412.list_items"))


@bp.route("/import", methods=["GET", "POST"])
def import_data():
    if request.method == "POST":
        file = request.files.get("pklfile")
        if not file or file.filename == "":
            return render_template(
                "asm2504/st12/message.html",
                title="Ошибка",
                message="Файл не выбран",
                back_url=url_for("st0412.import_data"),
            )

        storage = _make_storage()
        tmp_path = None
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pkl") as tmp_file:
                tmp_path = tmp_file.name
                file.save(tmp_path)

            with open(tmp_path, "rb") as f:
                items = pickle.load(f)

            inserted = storage.add_many(items)
            return render_template(
                "asm2504/st12/message.html",
                title="Импорт завершён",
                message=f"Импортировано: {inserted}",
                back_url=url_for("st0412.list_items"),
            )
        except Exception as exc:
            return render_template(
                "asm2504/st12/message.html",
                title="Ошибка",
                message=f"Не удалось прочитать pickle: {exc}",
                back_url=url_for("st0412.import_data"),
            )
        finally:
            if tmp_path and os.path.exists(tmp_path):
                os.remove(tmp_path)

    return render_template(
        "asm2504/st12/operations.html",
        title="Импорт из файла",
        form_type="import",
    )


@bp.route("/save", methods=["GET", "POST"])
def save_items():
    if request.method == "POST":
        filename = request.form.get("filename", "backup.sqlite3").strip() or "backup.sqlite3"
        if not filename.endswith(".sqlite3"):
            filename += ".sqlite3"

        os.makedirs(ST12_DIR, exist_ok=True)
        out_path = os.path.join(ST12_DIR, filename)

        src = get_connection()
        try:
            dst = sqlite3.connect(out_path)
            src.backup(dst)
            dst.close()
        finally:
            src.close()

        return render_template(
            "asm2504/st12/message.html",
            title="Резервная копия создана",
            message=f"Файл: {filename}",
            back_url=url_for("st0412.list_items"),
        )

    return render_template(
        "asm2504/st12/operations.html",
        title="Сохранение данных",
        form_type="save",
    )


@bp.route("/clear", methods=["GET", "POST"])
def clear_items():
    storage = _make_storage()
    count = len(storage.get_all())
    if request.method == "POST":
        storage.clear()
        return render_template(
            "asm2504/st12/message.html",
            title="Очищено",
            message=f"Удалено: {count}",
            back_url=url_for("st0412.list_items"),
        )

    return render_template(
        "asm2504/st12/operations.html",
        title="Очистка данных",
        form_type="clear",
        count=count,
    )

