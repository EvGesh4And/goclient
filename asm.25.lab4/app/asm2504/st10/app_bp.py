from flask import Blueprint, render_template, request, redirect, url_for
import os
from .container import Container
from .strategy_flask_io import FlaskIO
from .strategy_storage_pickle import PickleStorage
from .strategy_storage_sqlite import SQLiteStorage
from .student_bachelor import StudentBachelor
from .student_master import StudentMaster
from .student_graduate import StudentGraduate
from .api import register_api

def create_bp():
    THIS_DIR = os.path.dirname(os.path.abspath(__file__))
    NUM_DIR = int(str(THIS_DIR).split(os.sep)[-1][2:])
    PROJECT_APP_DIR = os.path.abspath(os.path.join(THIS_DIR, '..', '..'))
    TEMPLATES_DIR = os.path.join(PROJECT_APP_DIR, 'templates', 'asm2504', f'st{NUM_DIR}')
    STATIC_DIR = os.path.join(PROJECT_APP_DIR, 'static', 'asm2504', f'st{NUM_DIR}', 'css')
    STORAGE_DIR = os.path.join(PROJECT_APP_DIR, '..', 'data', 'asm2504', f'st{NUM_DIR}', 'server')

    bp_name = 'st' + str(NUM_DIR)
    bp = Blueprint(bp_name, __name__,
                template_folder=TEMPLATES_DIR,
                static_folder=STATIC_DIR)

    CLASS_LIST = [StudentBachelor, StudentMaster, StudentGraduate]
    bp.cont = Container(
        io_strategy=FlaskIO(classes=CLASS_LIST),
        storage_strategy=SQLiteStorage(base_dir=STORAGE_DIR, classes=CLASS_LIST),
        classes=CLASS_LIST)
    
    register_app_bp(bp)
    register_api(bp)
    return bp

def register_app_bp(bp):
    def bp_url(endpoint):
        return f"{bp.name}.{endpoint}"

    @bp.route("/")
    def index():
        items = bp.cont.list_items_with_message()
        indices = range(len(items))
        types = [(i + 1, cls.TYPE_NAME) for i, cls in enumerate(bp.cont.classes)]
        current_storage = bp.cont.storage.__class__.__name__
        msg = request.args.get("msg")
        if not msg:
            msg = bp.cont.io.pop_last_message()
        return render_template("index_knyazev.html",
                            items=items,
                            indices=indices,
                            types=types,
                            current_storage=current_storage,
                            message=msg)


    @bp.route("/storage", methods=["POST"])
    def set_storage():
        current_storage = bp.cont.storage.__class__.__name__
        new_storage = request.form.get("storage")
        current_items = bp.cont.list_items_with_message()
        if new_storage != current_storage:
            if new_storage == "PickleStorage":
                new_store = PickleStorage(base_dir=bp.cont.storage.base_dir, classes=bp.cont.classes,
                                        items=current_items)
            if new_storage == "SQLiteStorage":
                new_store = SQLiteStorage(base_dir=bp.cont.storage.base_dir, classes=bp.cont.classes,
                                        items=current_items)
            bp.cont.storage = new_store
        bp.cont.io.output_message(f'Стратегия изменена на {new_storage}')
        msg = bp.cont.io.pop_last_message()
        return redirect(url_for(bp_url("index"), msg=msg))


    @bp.route("/add", methods=["GET", "POST"])
    def add():
        if request.method == "GET":
            idx = bp.cont.io.select_type_from_request()
            if idx is None:
                msg = bp.cont.io.pop_last_message()
                return redirect(url_for(bp_url("index"), msg=msg))
            cls = bp.cont.classes[idx]
            return render_template("add_knyazev.html", cls_index=idx, cls_name=cls.TYPE_NAME, fields=cls.fields)

        type_idx = bp.cont.io.input_from_request("cls_index")
        if not type_idx or not type_idx.isdigit():
            return redirect(url_for(bp_url("index")))
        type_idx_int = int(type_idx)
        if not (0 <= type_idx_int < len(bp.cont.classes)):
            return redirect(url_for(bp_url("index")))
        cls = bp.cont.classes[type_idx_int]
        raw_fields = bp.cont.io.input_fields(cls())
        obj = bp.cont.create_from_type_index(type_idx_int, raw_fields)
        msg = bp.cont.io.pop_last_message()
        if obj is None:
            return render_template("add_knyazev.html", cls_index=type_idx_int, cls_name=cls.TYPE_NAME, fields=cls.fields, values=raw_fields, msg=msg)
        return redirect(url_for(bp_url("index"), msg=msg))


    @bp.route("/edit/<int:index>", methods=["GET", "POST"])
    def edit(index):
        idx = bp.cont.validate_index_str(str(index))
        if idx is None:
            msg = bp.cont.io.pop_last_message()
            return redirect(url_for(bp_url("index"), msg=msg))
        items = bp.cont.list_items_with_message()
        obj = items[idx]

        if request.method == "GET":
            return render_template("edit_knyazev.html", index=idx, obj=obj, fields=obj.fields)

        updates = bp.cont.io.input_updates(obj)
        obj2 = bp.cont.edit_by_index_str(str(idx), updates)
        msg = bp.cont.io.pop_last_message()
        if obj2 is None:
            return render_template("edit_knyazev.html", index=idx, obj=obj, fields=obj.fields, values=updates, msg=msg)
        return redirect(url_for(bp_url("index"), msg=msg))


    @bp.route("/remove/<int:index>", methods=["POST"])
    def remove(index):
        bp.cont.remove_by_index_str(str(index))
        msg = bp.cont.io.pop_last_message()
        return redirect(url_for(bp_url("index"), msg=msg))


    @bp.route("/clear_list", methods=["POST"])
    def clear_list():
        bp.cont.clear_with_message()
        msg = bp.cont.io.pop_last_message()
        return redirect(url_for(bp_url("index"), msg=msg))


    @bp.route("/save", methods=["POST"])
    def save():
        fname = bp.cont.io.input_from_request("filename")
        if fname:
            bp.cont.save_by_filename(fname)
        msg = bp.cont.io.pop_last_message()
        return redirect(url_for(bp_url("index"), msg=msg))


    @bp.route("/load", methods=["POST"])
    def load():
        fname = bp.cont.io.input_from_request("filename")
        if fname:
            bp.cont.load_by_filename(fname)
        msg = bp.cont.io.pop_last_message()
        return redirect(url_for(bp_url("index"), msg=msg))
