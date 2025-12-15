from pathlib import Path

from flask import Blueprint, g, redirect, render_template, request, url_for

from app.akm2501.st18.models import Employee, Student
from app.akm2501.st18.io.web import WebIO
from app.akm2501.st18.io.rest import RestIO
from app.akm2501.st18.storage.sqlite import SqliteStorage

bp = Blueprint('st0118', __name__)


def get_storage():
    if 'storage' not in g:
        g.storage = SqliteStorage()
    return g.storage


def get_web_io():
    if 'web_io' not in g:
        g.web_io = WebIO()
    return g.web_io


def get_rest_io():
    if 'rest_io' not in g:
        g.rest_io = RestIO()
    return g.rest_io


@bp.route('/', methods=['GET'])
def index():
    storage = get_storage()
    io = get_web_io()
    items = storage.get_items()
    return io.output(items)


@bp.route('/item/<int:item_id>', methods=['GET'])
def item_view(item_id: int):
    storage = get_storage()
    io = get_web_io()
    item = storage.get(item_id)

    if not item:
        return redirect(url_for('st0118.index'))

    return io.output_item(item)


@bp.route('/edit/<int:item_id>', methods=['GET'])
def edit(item_id: int):
    storage = get_storage()
    io = get_web_io()
    item = storage.get(item_id)

    if not item:
        return redirect(url_for('st0118.index'))

    return io.edit_item(item)


@bp.route('/process/<int:item_id>', methods=['POST'])
def process_item(item_id: int):
    storage = get_storage()
    io = get_web_io()

    if item_id == 0:
        item_type = request.form.get('type')
        if item_type == 'student':
            item = Student()
        elif item_type == 'employee':
            item = Employee()
        else:
            return redirect(url_for('st0118.index'))

        item.input(io)
        storage.add(item)
    else:
        item = storage.get(item_id)
        if not item:
            return redirect(url_for('st0118.index'))

        item.input(io)
        storage.update(item)

    return redirect(url_for('st0118.index'))


@bp.route('/delete/<int:item_id>', methods=['GET', 'POST'])
def delete(item_id: int):
    storage = get_storage()
    storage.delete(item_id)
    return redirect(url_for('st0118.index'))


@bp.route('/add', methods=['GET'])
def add():
    return render_template('akm2501/st18/add.html')


@bp.route('/add/<string:kind>', methods=['GET', 'POST'])
def add_kind(kind: str):
    if request.method == 'GET':
        if kind == 'student':
            return render_template('akm2501/st18/student_form.html', action=url_for('st0118.add_kind', kind=kind))
        elif kind == 'employee':
            return render_template('akm2501/st18/employee_form.html', action=url_for('st0118.add_kind', kind=kind))
        else:
            return redirect(url_for('st0118.index'))

    storage = get_storage()
    io = get_web_io()

    if kind == 'student':
        item = Student()
    elif kind == 'employee':
        item = Employee()
    else:
        return redirect(url_for('st0118.index'))

    item.input(io)
    storage.add(item)

    return redirect(url_for('st0118.index'))


@bp.route('/import', methods=['GET', 'POST'])
def import_from_pickle_to_sql():
    storage = get_storage()

    if request.method == 'GET':
        return render_template('akm2501/st18/import.html')

    file = request.files.get('datafile')
    path = request.form.get('path', '').strip()

    if file and file.filename:
        storage.import_from_upload(file.stream)
    elif path:
        storage.import_from_file(Path(path))

    return redirect(url_for('st0118.index'))


@bp.route('/save', methods=['GET', 'POST'])
def save_to_file():
    storage = get_storage()

    if request.method == 'GET':
        return render_template('akm2501/st18/save.html')

    filename = request.form.get('filename', '').strip()

    if filename:
        if not filename.endswith('.dat'):
            filename += '.dat'

        data_directory = Path(__file__).resolve().parents[4] / 'data' / 'akm2501' / 'st18'
        file_path = data_directory / filename
        storage.save_to_file(file_path)

    return redirect(url_for('st0118.index'))


@bp.route('/clear', methods=['POST'])
def clear():
    storage = get_storage()
    storage.clear()
    return redirect(url_for('st0118.index'))


@bp.route('/api/', methods=['GET'])
def api_index():
    storage = get_storage()
    io = get_rest_io()
    items = storage.get_items()
    return io.output(items)


@bp.route('/api/<int:item_id>', methods=['GET'])
def api_get_item(item_id: int):
    storage = get_storage()
    io = get_rest_io()
    item = storage.get(item_id)
    return io.output_item(item)


@bp.route('/api/', methods=['POST'])
def api_add_item():
    storage = get_storage()
    io = get_rest_io()

    item_type = io.input('type')

    if item_type == 'student':
        item = Student()
    elif item_type == 'employee':
        item = Employee()
    else:
        return {'error': 'Unknown type'}, 400

    item.input(io)
    new_id = storage.add(item)

    return {'id': new_id, 'message': 'Item added'}, 201


@bp.route('/api/<int:item_id>', methods=['PUT'])
def api_update_item(item_id: int):
    storage = get_storage()
    io = get_rest_io()
    item = storage.get(item_id)

    if not item:
        return {'error': 'Item not found'}, 404

    item.input(io)
    storage.update(item)

    return {'message': 'Item updated'}, 200


@bp.route('/api/<int:item_id>', methods=['DELETE'])
def api_delete_item(item_id: int):
    storage = get_storage()
    if storage.delete(item_id):
        return {'message': 'Item deleted'}, 200
    else:
        return {'error': 'Item not found'}, 404


@bp.route('/api/', methods=['DELETE'])
def api_clean():
    storage = get_storage()
    storage.clear()
    return {'message': 'All items deleted'}, 200


@bp.teardown_request
def teardown_storage(ctx):
    if 'storage' in g:
        storage = g.storage
        max_id, items = storage.load()
        storage.store(max_id, items)
