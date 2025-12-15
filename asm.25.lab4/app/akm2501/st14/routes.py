import os
import sqlite3

from flask import redirect, render_template, request, url_for

from . import bp
from .db import ST14_DIR, get_connection
from .flask_io import FlaskIO
from .group_container import GroupContainer
from .sqlite_storage import SQLiteStorage


def _make_io() -> FlaskIO:
    return FlaskIO()


def _get_container() -> GroupContainer:
    io = _make_io()
    container = GroupContainer(io=io, storage=None)
    storage = SQLiteStorage(type_registry=container.type_names)
    container.storage = storage
    container.load()
    return container


@bp.route("/list")
def list_items():
    container = _get_container()
    table_html = container.list_items_html(url_for_func=url_for)
    return render_template(
        "akm2501/st14/page.html",
        page_type="list",
        title="Список сотрудников",
        table_html=table_html,
        count=len(container.items),
    )


@bp.route("/add")
def add_choose():
    container = _get_container()
    type_pairs = [(name, name) for name in container.type_names.keys()]
    return render_template(
        "akm2501/st14/page.html",
        page_type="add_choose",
        title="Выберите тип сотрудника",
        types=type_pairs,
    )


@bp.route("/add/<type_name>", methods=["GET", "POST"])
def add_item(type_name):
    container = _get_container()
    if type_name not in container.type_names:
        return render_template("akm2501/st14/message.html", title="Ошибка", message="Неверный тип")

    io = _make_io()
    if request.method == "POST":
        container.add_item(type_name=type_name, form_data=request.form)
        container.save()
        return redirect(url_for("st0114.list_items"))

    obj = container.type_names[type_name]()
    form_html = io.build_form_html(
        obj,
        url_for("st0114.add_item", type_name=type_name),
        f"Добавление: {type_name}",
        "Добавить",
        url_for("st0114.list_items"),
    )
    return render_template("akm2501/st14/form.html", form_html=form_html)


@bp.route("/edit/<int:item_id>", methods=["GET", "POST"])
def edit_item(item_id):
    container = _get_container()
    if not (0 <= item_id < len(container.items)):
        return render_template("akm2501/st14/message.html", title="Ошибка", message="Сотрудник не найден")

    io = _make_io()
    if request.method == "POST":
        container.edit_item(idx=item_id, form_data=request.form)
        container.save()
        return redirect(url_for("st0114.list_items"))

    obj = container.items[item_id]
    form_html = io.build_form_html(
        obj,
        url_for("st0114.edit_item", item_id=item_id),
        f"Редактирование: {obj.__class__.__name__}",
        "Сохранить",
        url_for("st0114.list_items"),
    )
    return render_template("akm2501/st14/form.html", form_html=form_html)


@bp.route("/delete/<int:item_id>")
def delete_item(item_id):
    container = _get_container()
    container.remove_item(idx=item_id)
    container.save()
    return redirect(url_for("st0114.list_items"))


@bp.route("/save", methods=["GET", "POST"])
def save_items():
    if request.method == "POST":
        filename = request.form.get("filename", "backup.sqlite3").strip() or "backup.sqlite3"
        if not filename.endswith(".sqlite3"):
            filename += ".sqlite3"

        os.makedirs(ST14_DIR, exist_ok=True)
        out_path = os.path.join(ST14_DIR, filename)

        src = get_connection()
        try:
            dst = sqlite3.connect(out_path)
            src.backup(dst)
            dst.close()
        finally:
            src.close()

        return render_template(
            "akm2501/st14/message.html",
            title="Резервная копия создана",
            message=f"Файл: {filename}",
            back_url=url_for("st0114.list_items"),
        )

    return render_template(
        "akm2501/st14/operations.html",
        title="Сохранение данных",
        form_type="save",
    )


@bp.route("/clear", methods=["GET", "POST"])
def clear_items():
    container = _get_container()
    count = len(container.items)
    if request.method == "POST":
        container.clear()
        container.save()
        return render_template(
            "akm2501/st14/message.html",
            title="Очищено",
            message=f"Удалено: {count}",
            back_url=url_for("st0114.list_items"),
        )

    return render_template(
        "akm2501/st14/operations.html",
        title="Очистка данных",
        form_type="clear",
        count=count,
    )
