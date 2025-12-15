from flask import jsonify, request, redirect, url_for
import os
from . import bp
from .storage import PickleStorage
from .containeritem import Container

_storage = None
_container = None

def get_storage():
    global _storage
    if _storage is None:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
        data_dir = os.path.join(project_root, 'data', 'akm2501', 'st09')
        os.makedirs(data_dir, exist_ok=True)
        _storage = PickleStorage(os.path.join(data_dir, 'cardfile.pkl'))
    return _storage

def get_container():
    global _container
    if _container is None:
        _container = Container(get_storage())
    return _container

@bp.route('/')
def index():
    return get_container().show_all()

@bp.route('/showform/<int:item_type>')
def show_form(item_type):
    return get_container().show_form(item_type)

@bp.route('/add', methods=['POST'])
def add_item():
    return get_container().add_from_form()

@bp.route('/edit/<int:item_id>')
def edit_item(item_id):
    return get_container().show_edit_form(item_id)

@bp.route('/update/<int:item_id>', methods=['POST'])
def update_item(item_id):
    return get_container().update_from_form(item_id)

@bp.route('/delete/<int:item_id>')
def delete_item(item_id):
    return get_container().delete_item_web(item_id)

@bp.route('/save_pickle')
def save_pickle():
    get_container().save_to_file()
    return redirect(url_for('st0109.index'))

@bp.route('/load_pickle')
def load_pickle():
    get_container().load_from_file()
    return redirect(url_for('st0109.index'))

# REST API Endpoints
@bp.route('/api/items', methods=['GET'])
def api_get_items():
    storage = get_storage()
    items = storage.get_all_items()
    return jsonify([item.to_dict() for item in items])

@bp.route('/api/items/<int:item_id>', methods=['GET'])
def api_get_item(item_id):
    storage = get_storage()
    item = storage.get_item(item_id)
    if not item:
        return jsonify({'error': 'Item not found'}), 404
    return jsonify(item.to_dict())

@bp.route('/api/items', methods=['POST'])
def api_create_item():
    storage = get_storage()
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    required_fields = ['type', 'name', 'age']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    item_data = {
        'type': data['type'],
        'name': data['name'],
        'age': data['age']
    }
    
    if data['type'] == 'Guest' and 'pass_type' in data:
        item_data['pass_type'] = data['pass_type']
    elif data['type'] == 'Coach' and 'training_type' in data:
        item_data['training_type'] = data['training_type']
    
    if storage.add_item(item_data):
        return jsonify({'message': 'Item created successfully'}), 201
    else:
        return jsonify({'error': 'Failed to create item'}), 500

@bp.route('/api/items/<int:item_id>', methods=['PUT'])
def api_update_item(item_id):
    storage = get_storage()
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    item_data = {}
    if 'name' in data:
        item_data['name'] = data['name']
    if 'age' in data:
        item_data['age'] = data['age']
    if 'pass_type' in data:
        item_data['pass_type'] = data['pass_type']
    if 'training_type' in data:
        item_data['training_type'] = data['training_type']
    
    if storage.update_item(item_id, item_data):
        return jsonify({'message': 'Item updated successfully'})
    else:
        return jsonify({'error': 'Item not found or update failed'}), 404

@bp.route('/api/items/<int:item_id>', methods=['DELETE'])
def api_delete_item(item_id):
    storage = get_storage()
    if storage.delete_item(item_id):
        return jsonify({'message': 'Item deleted successfully'})
    else:
        return jsonify({'error': 'Item not found'}), 404

@bp.route('/api/clear', methods=['POST'])
def api_clear_items():
    storage = get_storage()
    if storage.clear_all():
        return jsonify({'message': 'All items cleared'})
    else:
        return jsonify({'error': 'Clear operation failed'}), 500

@bp.route('/api/items/replace', methods=['POST'])
def api_replace_items():
    storage = get_storage()
    data = request.get_json()
    
    if not isinstance(data, list):
        return jsonify({'error': 'Expected a list of items'}), 400
    
    storage.clear_all()
    
    for item_data in data:
        storage.add_item(item_data)
    
    return jsonify({'message': f'Successfully replaced {len(data)} items'}), 200