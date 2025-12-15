from flask import jsonify, request
from . import bp
from .storage import Storage
from .group import Group
from .flask_io import FlaskIOStrategy

storage = Storage()
flask_io = FlaskIOStrategy()
web_group = Group(storage, flask_io)


@bp.route('/api/dishes', methods=['GET'])
def api_get_dishes():
    dishes = storage.get_items()
    return jsonify({
        'success': True,
        'count': len(dishes),
        'dishes': dishes
    })


@bp.route('/api/dishes/<int:index>', methods=['GET'])
def api_get_dish(index):
    dish = storage.get_item(index)
    if dish:
        return jsonify({
            'success': True,
            'dish': dish
        })
    return jsonify({
        'success': False,
        'message': 'Блюдо не найдено'
    }), 404


@bp.route('/api/dishes', methods=['POST'])
def api_add_dish():
    data = request.get_json()

    if not data:
        return jsonify({
            'success': False,
            'message': 'Нет данных'
        }), 400

    dish_type = data.get('dish_type')
    form_data = {
        'name': data.get('name', ''),
        'cuisine': data.get('cuisine', ''),
        'calories': str(data.get('calories', 0)),
        'garnish': data.get('garnish', ''),
        'sweetness': str(data.get('sweetness', 5))
    }

    if web_group.add(dish_type, form_data):
        return jsonify({
            'success': True,
            'message': 'Блюдо добавлено'
        }), 201

    return jsonify({
        'success': False,
        'message': 'Ошибка при добавлении блюда'
    }), 400


@bp.route('/api/dishes/<int:index>', methods=['PUT'])
def api_update_dish(index):
    data = request.get_json()

    if not data:
        return jsonify({
            'success': False,
            'message': 'Нет данных'
        }), 400

    dish_dict = storage.get_item(index)
    if not dish_dict:
        return jsonify({
            'success': False,
            'message': 'Блюдо не найдено'
        }), 404

    form_data = {
        'name': data.get('name', dish_dict['name']),
        'cuisine': data.get('cuisine', dish_dict['cuisine']),
        'calories': str(data.get('calories', dish_dict['calories'])),
        'garnish': data.get('garnish', dish_dict.get('garnish', '')),
        'sweetness': str(data.get('sweetness', dish_dict.get('sweetness', 5)))
    }

    if web_group.edit(index, form_data):
        return jsonify({
            'success': True,
            'message': 'Блюдо обновлено'
        })

    return jsonify({
        'success': False,
        'message': 'Ошибка при обновлении'
    }), 400


@bp.route('/api/dishes/<int:index>', methods=['DELETE'])
def api_delete_dish(index):
    if web_group.delete(index):
        return jsonify({
            'success': True,
            'message': 'Блюдо удалено'
        })

    return jsonify({
        'success': False,
        'message': 'Блюдо не найдено'
    }), 404


@bp.route('/api/dishes/clear', methods=['DELETE'])
def api_clear_dishes():
    web_group.clear()
    return jsonify({
        'success': True,
        'message': 'Все блюда удалены'
    })


@bp.route('/api/save', methods=['POST'])
def api_save_data():
    data = request.get_json()
    filename = data.get('filename', '').strip()

    if not filename:
        return jsonify({
            'success': False,
            'message': 'Введите название файла'
        }), 400

    if storage.save_to_pickle(filename):
        return jsonify({
            'success': True,
            'message': f'Данные сохранены в {filename}'
        })

    return jsonify({
        'success': False,
        'message': 'Ошибка при сохранении'
    }), 500


@bp.route('/api/load', methods=['POST'])
def api_load_data():
    data = request.get_json()
    filename = data.get('filename', '').strip()

    if not filename:
        return jsonify({
            'success': False,
            'message': 'Введите название файла'
        }), 400

    if storage.load_from_pickle(filename):
        return jsonify({
            'success': True,
            'message': f'Данные загружены из {filename}'
        })

    return jsonify({
        'success': False,
        'message': 'Ошибка при загрузке'
    }), 500


@bp.route('/api/files', methods=['GET'])
def api_get_files():
    files = storage.get_available_pickle_files()
    return jsonify({
        'success': True,
        'files': files
    })