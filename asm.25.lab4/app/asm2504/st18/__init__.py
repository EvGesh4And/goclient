from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from .io_strategies.flask_io import FlaskIO
from .io_strategies.sqlite_storage import SQLiteStorage
from .io_strategies.api_io import APIIO
from .entities.student import Student
from .entities.teacher import Teacher
from .entities.staff import Staff
import json


bp = Blueprint('st18', __name__, template_folder='templates/asm2504/st18')

#interface
@bp.route("/")
def index():
    storage = SQLiteStorage()
    return render_template("asm2504/st18/index.html",
                         current_file=storage.get_filename())

@bp.route("/list")
def list_people():
    storage = SQLiteStorage()

    people = storage.get_all()
    io = FlaskIO()
    people_data = []
    for p in people:
        fields = io.get_fields(p)
        fields["__type__"] = p.__class__.__name__
        people_data.append(fields)

    all_keys = sorted({k for d in people_data for k in d.keys()})
    return render_template("asm2504/st18/list.html", people=people_data, keys=all_keys)

@bp.route("/add", methods=["GET", "POST"])
def add_person():
    storage = SQLiteStorage()
    io = FlaskIO()

    if request.method == "POST":
        role = request.form.get("role")
        cls_map = {"student": Student, "teacher": Teacher, "staff": Staff}
        cls = cls_map.get(role)
        if not cls:
            return "Неизвестный тип!"

        obj = cls(io_strategy=io)
        for field, value in request.form.items():
            if hasattr(obj, field) and field != "io_strategy":
                setattr(obj, field, value)

        storage.add(obj)
        return redirect(url_for("st18.list_people"))

    return render_template("asm2504/st18/add.html")

@bp.route("/edit/<int:person_id>", methods=["GET", "POST"])
def edit_person(person_id):
    
    io = FlaskIO()
    storage = SQLiteStorage()

    person = storage.get(person_id)
    if not person:
        return "Запись не найдена!"
        
    if request.method == "POST":
        for field, value in request.form.items():
            if hasattr(person, field) and field != "io_strategy":
                setattr(person, field, value)
        storage.update(person_id, person)
        return redirect(url_for("st18.list_people"))

    return render_template("asm2504/st18/edit.html", person=person,
                         fields=io.get_fields(person), person_id=person_id)

@bp.route("/delete/<int:person_id>")
def delete_person(person_id):
    storage = SQLiteStorage()
    storage.delete(person_id)
    return redirect(url_for("st18.list_people"))

@bp.route("/clear")
def clear_all():
    storage = SQLiteStorage()
    storage.clear()
    return redirect(url_for("st18.list_people"))

@bp.route("/save", methods=["GET", "POST"])
def save_as():
    storage = SQLiteStorage()
    if request.method == "POST":
        filename = request.form.get("filename")
        if not filename:  
            return "Имя файла не может быть пустым!"
            
        if not filename.endswith(".pkl"):
            filename += ".pkl"
            
        storage.set_filename(filename.replace('.pkl', '.db'))
        storage.save()
        return redirect(url_for("st18.index"))

    return render_template("asm2504/st18/save.html", current=storage.get_filename())

@bp.route("/load", methods=["GET", "POST"])
def load_from():
    storage = SQLiteStorage()
    files = storage.get_available_files("./data/asm2504/st18/")
    if request.method == "POST":
        filename = request.form.get("filename")
        if not filename:  
            return " Файл не выбран!"
            
        if filename.endswith('.pkl'):
            storage.import_from_pickle(f"./data/asm2504/st18/{filename}")
        else:
            storage.set_filename(filename)
        return redirect(url_for("st18.list_people"))

    return render_template("asm2504/st18/load.html", files=files,
                         current=storage.get_filename())


#REST API
@bp.route("/api/people", methods=["GET"])
def api_get_all():
    storage = SQLiteStorage() 
    api_io = APIIO()
    people = storage.get_all()
    people_data = []
    
    for p in people:
        fields = api_io.get_fields(p)
        people_data.append(fields)
    
    return jsonify({
        "success": True,
        "count": len(people_data),
        "people": people_data
    })

@bp.route("/api/people/<int:person_id>", methods=["GET"])
def api_get_one(person_id):
    storage = SQLiteStorage() 
    api_io = APIIO()
    person = storage.get(person_id)
    if not person:
        return jsonify({"success": False, "error": "Запись не найдена"}), 404
    
    person_data = api_io.get_fields(person)
    
    return jsonify({
        "success": True,
        "person": person_data
    })

@bp.route("/api/people", methods=["POST"])
def api_create():
    storage = SQLiteStorage() 
    io = FlaskIO()
    api_io = APIIO()
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "error": "Нет данных"}), 400
    
    obj = api_io.create_object_from_data(data, io_strategy=io)
    
    if not obj:
        return jsonify({"success": False, "error": "Неизвестный тип"}), 400
    
    storage.add(obj)
    
    return jsonify({
        "success": True,
        "message": "Запись создана",
        "id": len(storage.get_all()) - 1
    }), 201

@bp.route("/api/people/<int:person_id>", methods=["PUT"])
def api_update(person_id):
    storage = SQLiteStorage() 
    person = storage.get(person_id)
    if not person:
        return jsonify({"success": False, "error": "Запись не найдена"}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "error": "Нет данных"}), 400
    
    for field, value in data.items():
        if hasattr(person, field) and field != "io_strategy" and field != "type":
            setattr(person, field, value)
    
    storage.update(person_id, person)
    
    return jsonify({
        "success": True,
        "message": "Запись обновлена"
    })

@bp.route("/api/people/<int:person_id>", methods=["DELETE"])
def api_delete(person_id):
    storage = SQLiteStorage()  
    person = storage.get(person_id)
    if not person:
        return jsonify({"success": False, "error": "Запись не найдена"}), 404
    
    storage.delete(person_id)
    
    return jsonify({
        "success": True,
        "message": "Запись удалена"
    })

@bp.route("/api/clear", methods=["DELETE"])
def api_clear():
    storage = SQLiteStorage() 

    storage.clear()
    
    return jsonify({
        "success": True,
        "message": "Все записи удалены"
    })
