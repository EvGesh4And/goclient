from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from .storage_repo import SQLiteStorage
from .entity import Dish
from .web_io import WebIO

bp = Blueprint('st03', __name__, template_folder='templates/asm2504/st03', static_folder='static')
storage = SQLiteStorage()

DISH_TYPES = ['Soup', 'MainCourse', 'Dessert', 'Drink']

def create_dish_from_form(form_data):
    io_handler = WebIO()
    io_handler.set_form_data(form_data)
    
    dish = Dish()
    dish.input(io_handler)
    return dish

@bp.route('/')
def index():
    dishes = storage.get_all(Dish)
    message = request.args.get('message')
    error = request.args.get('error')
    return render_template('asm2504/st03/list.html', items=dishes, message=message, error=error)

@bp.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        dish = create_dish_from_form(request.form)
        
        if dish:
            storage.add(dish)
            return redirect(url_for('st03.index', message='Блюдо успешно добавлено'))
    
    return render_template('asm2504/st03/form.html', mode='add', types=DISH_TYPES)

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    dish = storage.get_by_id(id, Dish)
    
    if not dish:
        return redirect(url_for('st03.index', error='Блюдо не найдено'))
    
    if request.method == 'POST':
        updated_dish = create_dish_from_form(request.form)
        
        if updated_dish:
            storage.update(id, updated_dish)
            return redirect(url_for('st03.index', message='Блюдо успешно обновлено'))
    
    io_handler = WebIO()
    dish.output(io_handler)
    form_data = io_handler.get_output_data()
    
    return render_template('asm2504/st03/form.html', mode='edit', entity=form_data, types=DISH_TYPES)

@bp.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    storage.delete(id)
    return redirect(url_for('st03.index', message='Блюдо успешно удалено'))

@bp.route('/save', methods=['POST'])
def save():
    dishes = storage.get_all(Dish)
    success = storage.save_to_file(dishes)
    
    if success:
        return redirect(url_for('st03.index', message='Данные успешно сохранены в файл'))
    else:
        return redirect(url_for('st03.index', error='Ошибка сохранения в файл'))

@bp.route('/load', methods=['POST'])
def load():
    loaded_dishes = storage.load_from_file()
    
    if loaded_dishes is not None:
        success = storage.import_data(loaded_dishes)
        if success:
            return redirect(url_for('st03.index', message='Данные успешно загружены из файла'))
    
    return redirect(url_for('st03.index', error='Ошибка загрузки из файла'))

@bp.route('/clear', methods=['POST'])
def clear():
    storage.clear_all()
    return redirect(url_for('st03.index', message='База данных очищена'))

@bp.route("/group")
def group():
    from .group import group
    return group().f()

# ================ REST API ENDPOINTS ================

@bp.route('/api/dishes', methods=['GET'])
def api_get_dishes():
    """API: Получить все блюда"""
    dishes = storage.get_all(Dish)
    result = []
    for dish in dishes:
        result.append({
            'id': dish.id,
            'type': dish.dish_type,
            'name': dish.name,
            'price': dish.price,
            'calories': dish.calories,
            'ingredients': dish.ingredients
        })
    return jsonify(result)

@bp.route('/api/dishes', methods=['POST'])
def api_create_dish():
    """API: Создать блюдо"""
    data = request.json
    dish = Dish(
        dish_type=data.get('type', ''),
        name=data.get('name', ''),
        price=float(data.get('price', 0)),
        calories=int(data.get('calories', 0)),
        ingredients=data.get('ingredients', [])
    )
    storage.add(dish)
    return jsonify({'id': dish.id}), 201

@bp.route('/api/dishes/<int:id>', methods=['PUT'])
def api_update_dish(id):
    """API: Обновить блюдо"""
    data = request.json
    dish = Dish(
        dish_type=data.get('type', ''),
        name=data.get('name', ''),
        price=float(data.get('price', 0)),
        calories=int(data.get('calories', 0)),
        ingredients=data.get('ingredients', [])
    )
    storage.update(id, dish)
    return jsonify({'success': True})

@bp.route('/api/dishes/<int:id>', methods=['DELETE'])
def api_delete_dish(id):
    """API: Удалить блюдо"""
    storage.delete(id)
    return jsonify({'success': True})

@bp.route('/api/dishes', methods=['DELETE'])
def api_clear_dishes():
    """API: Очистить все блюда"""
    storage.clear_all()
    return jsonify({'success': True})