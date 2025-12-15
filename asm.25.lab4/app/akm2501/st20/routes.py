from flask import redirect, url_for, jsonify, request
import os
from . import bp
from .storage import PickleStorage
from .containeritem import Container

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(current_dir))))
data_dir = os.path.join(project_root, 'data', 'akm2501', 'st20')
os.makedirs(data_dir, exist_ok=True)

pickle_storage = PickleStorage(os.path.join(data_dir, 'medical.pkl'))
container = Container(pickle_storage)

@bp.route('/')
def index():
    return container.show_all()

@bp.route('/showform/<string:staff_type>')
def show_form(staff_type):
    return container.show_form(staff_type)

@bp.route('/add', methods=['POST'])
def add_item():
    return container.add_from_form()

@bp.route('/edit/<int:item_id>')
def edit_item(item_id):
    return container.show_edit_form(item_id)

@bp.route('/update/<int:item_id>', methods=['POST'])
def update_item(item_id):
    return container.update_from_form(item_id)

@bp.route('/delete/<int:item_id>')
def delete_item(item_id):
    return container.delete_item_web(item_id)

@bp.route('/save_pickle')
def save_pickle():
    container.save_to_file()
    return redirect(url_for('st0120.index'))

@bp.route('/load_pickle')
def load_pickle():
    container.load_from_file()
    return redirect(url_for('st0120.index'))

@bp.route('/api/items', methods=['GET'])
def api_get_items():
    items = pickle_storage.get_all_items()
    return jsonify([item.to_dict() for item in items])

@bp.route('/api/items/<int:item_id>', methods=['GET'])
def api_get_item(item_id):
    item = pickle_storage.get_item(item_id)
    if item:
        return jsonify(item.to_dict())
    return jsonify({'error': 'Item not found'}), 404

@bp.route('/api/items', methods=['POST'])
def api_create_item():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    if pickle_storage.add_item(data):
        return jsonify({'success': True, 'message': 'Item created'}), 201
    return jsonify({'error': 'Failed to create item'}), 400

@bp.route('/api/items/<int:item_id>', methods=['PUT'])
def api_update_item(item_id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    if pickle_storage.update_item(item_id, data):
        return jsonify({'success': True, 'message': 'Item updated'})
    return jsonify({'error': 'Item not found or update failed'}), 404

@bp.route('/api/items/<int:item_id>', methods=['DELETE'])
def api_delete_item(item_id):
    if pickle_storage.delete_item(item_id):
        return jsonify({'success': True, 'message': 'Item deleted'})
    return jsonify({'error': 'Item not found'}), 404

@bp.route('/api/stats', methods=['GET'])
def api_get_stats():
    items = pickle_storage.get_all_items()
    nurses = sum(1 for item in items if item.staff_type == 'nurse')
    doctors = sum(1 for item in items if item.staff_type == 'doctor')
    
    return jsonify({
        'total': len(items),
        'nurses': nurses,
        'doctors': doctors
    })