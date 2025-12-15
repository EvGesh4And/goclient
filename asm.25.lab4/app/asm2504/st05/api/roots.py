import copy

from flask import jsonify, request, g, render_template, redirect

from ..api import bp
from ..io_handlers.flask_handler import FlaskIOHandler
from ..io_handlers.rest_handler import RESTIOHandler
from ..models.leader import Leader
from ..models.student import Student
from ..storage.db_storage import DBStorage
from ..storage.pickle_storage import PickleStorage
from .group import Group


selfurl = 'group1'

def get_group():
    if 'group' not in g:
        g.group = Group(DBStorage("group"),io_handler=FlaskIOHandler(request))
    return g.group

def get_url_root():
    return '/' + request.url_rule.rule.split('/')[1]

@bp.route("/")
def index():
    group = get_group()
    group.show_items()
    print(request.url_rule)
    print(request.url_rule.rule.split('/'))
    return render_template("asm2504/st05/group/group.tpl", group=group.show_items(), selfurl=get_url_root())



@bp.route("/showform/<int:id>")
def show_form(id):
    group = get_group()
    if id == 1:
        person = Student(io_handler=group.io_handler)
        return render_template("asm2504/st05/group/student_form.tpl", person=person, selfurl=get_url_root())
    elif id == 2:
        worker = Leader(io_handler=group.io_handler)
        return render_template("asm2504/st05/group/leader_form.tpl", person=worker, selfurl=get_url_root())
    else:
        return render_template("asm2504/st05/group/group.tpl", group=group.get_items(), selfurl=get_url_root())

@bp.route("/edit_form/<int:cls_id>/<int:id>")
def edit_form(cls_id, id):
    group = get_group()
    person = group.get_item(id)
    if cls_id == 1:
        return render_template("asm2504/st05/group/student_form.tpl", person=person, selfurl=get_url_root())
    elif cls_id == 2:
        return render_template("asm2504/st05/group/leader_form.tpl", person=person, selfurl=get_url_root())
    else:
        return render_template("asm2504/st05/group/group.tpl", group=group.get_items(), selfurl=get_url_root())

@bp.route("/edit", methods=['POST'])
def edit_item():
    id = int(request.form.get("id"))
    group = get_group()
    person = group.get_item(id)
    person.io_handler = copy.deepcopy(group.io_handler)
    person.id = id
    person.input()
    group.edit(person)
    return redirect(get_url_root())

@bp.route("/delete/<int:id>")
def delete_item(id):
    group = get_group()
    group.delete(id)
    return redirect(get_url_root())


@bp.route("/add", methods=['POST'])
def add():
    type = request.form['obj_class']
    group = get_group()
    cls = group.classes.get(type)
    group.add(cls)

    return redirect(get_url_root())

@bp.route("/load_from_pickle")
def load_from_pickle():
    group = get_group()
    storage = PickleStorage(group)
    for item in storage.get_items():
        item.id = 0
        group.storage.add(item)
    return redirect(get_url_root())

@bp.teardown_request
def teardown_book(ctx):
    get_group().storage.store()


@bp.route("/api/", methods=['GET'])
def api_group():
    group = get_group()
    ids = []
    for item in group.get_items():
        ids.append(item.to_dict())
    return jsonify({'ids': ids})



@bp.route("/api/", methods=['POST'])
def apiadd():
    group = get_group()
    cls_id = request.json.get('cls_id')
    item = None
    if cls_id == 1:
        item = Student(io_handler=RESTIOHandler(request))
    elif cls_id == 2:
        item = Leader(io_handler=RESTIOHandler(request))
    else:
        return jsonify({'error': 'Invalid cls_id'})
    item.input()
    group.storage.add(item)
    return ''



@bp.route("/api/<int:id>", methods=['GET'])
def apiget(id):
    group = get_group()
    item = group.get_item(id)
    if item:
        return jsonify(item.to_dict())
    else:
        return jsonify({'error': 'item not found'})


@bp.route("/api/<int:id>", methods=['PUT'])
def apiset(id):
    group = get_group()
    item = group.get_item(id)
    if not item:
        return jsonify({'error': 'item not found'})

    cls_id = request.json.get('cls_id')
    if cls_id == 1:
        item = Student(io_handler=RESTIOHandler(request))
    elif cls_id == 2:
        item = Leader(io_handler=RESTIOHandler(request))
    else:
        return jsonify({'error': 'Invalid cls_id'})
    item.id = id
    item.input()
    group.storage.edit(item)
    return ''

@bp.route("/api/", methods=['DELETE'])
def apiclean():
    group = get_group()
    group.clear()
    return ''

@bp.route("/api/<int:id>", methods=['DELETE'])
def apidelete(id):
    group = get_group()
    group.delete(id)
    return ''