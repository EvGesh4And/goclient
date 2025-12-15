import os

from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash, g


def create_bp():
    this_dir = os.path.dirname(__file__)
    student_dir = str(this_dir).split(os.sep)[-1]
    project_app_dir = os.path.abspath(os.path.join(this_dir, "..", "..", ".."))
    templates_dir = os.path.join(project_app_dir, "app", "templates", "asm2504", f"{student_dir}")
    static_dir = os.path.join(project_app_dir, "app", "static", "asm2504", f"{student_dir}")
    storage_dir = os.path.join(project_app_dir, "data", "asm2504", f"{student_dir}")

    _bp = Blueprint(student_dir, __name__, template_folder=templates_dir, static_folder=static_dir)

    return _bp


bp = create_bp()


from .group import Group
from .io_strategy import FlaskIO, IOStrategy
from .storage_strategy import DBStorage, PickleStorage, StorageStrategy


def get_io():
    io = getattr(g, "_io", None)
    if io is None:
        io = g._io = FlaskIO()
    return io


def get_storage():
    storage = getattr(g, "_storage", None)
    if storage is None:
        storage = g._storage = DBStorage()
    return storage


def get_group():
    group = getattr(g, "_group", None)
    if group is None:
        group = g._group = Group(get_storage(), get_io())
    return group

#region Classic

@bp.route("/")
def index():
    students = get_group().get_all()
    return render_template("asm2504/st26/index.html", students=students)


@bp.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        type = request.form.get("type")
        if type:
            get_group().add(type)
            return redirect(url_for("st26.index"))
    return render_template("asm2504/st26/add.html")


@bp.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    obj = get_group().get_by_id(id)
    if request.method == "POST":
        get_group().edit(id)
        return redirect(url_for("st26.index"))
    return render_template("asm2504/st26/edit.html", _obj=obj, type=obj.__class__.__name__)


@bp.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    get_group().delete(id)
    return redirect(url_for("st26.index"))


@bp.route("/clear", methods=["POST"])
def clear():
    get_group().clear()
    return redirect(url_for("st26.index"))


@bp.route("/load", methods=["POST"])
def load():
    get_group().clear()
    get_group().load()
    return redirect(url_for("st26.index"))


@bp.route("/save", methods=["POST"])
def save():
    get_group().save()
    return redirect(url_for("st26.index"))

#endregion

#region API

@bp.route("/api/", methods=["GET"])
def api_index():
    students = get_group().get_all()
    return jsonify([student.output_fields() for student in students])


@bp.route("/api/add", methods=["POST"])
def api_add():
    pass


@bp.route("/api/edit/<int:id>", methods=["PUT"])
def api_edit(id):
    pass


@bp.route("/api/delete/<int:id>", methods=["DELETE"])
def api_delete(id):
    pass


@bp.route("/api/clear", methods=["DELETE"])
def api_clear():
    pass


@bp.route("/api/load", methods=["POST"])
def api_load():
    pass


@bp.route("/api/save", methods=["POST"])
def api_save():
    pass



#endregion