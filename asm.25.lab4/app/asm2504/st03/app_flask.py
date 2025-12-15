# import os
# from flask import Flask, render_template, request, redirect, url_for, flash
# from storage_repo import PickleStorage
# from entity import Dish

# app = Flask(__name__)
# app.secret_key = 'secret-key'
# storage = PickleStorage()

# DISH_TYPES = ['Soup', 'MainCourse', 'Dessert', 'Drink']

# @app.route('/')
# def index():
#     dishes = storage.get_all_dishes()
#     return render_template('list.html', items=dishes)

# @app.route('/add', methods=['GET', 'POST'])
# def add():
#     if request.method == 'POST':
#         dish_type = request.form.get('type')
#         name = request.form.get('name')
#         price = float(request.form.get('price'))
#         calories = int(request.form.get('calories'))
#         ingredients = [i.strip() for i in request.form.get('ingredients', '').split(',') if i.strip()]
        
#         dish = Dish(dish_type, name, price, calories, ingredients)
#         storage.add_dish(dish)
#         flash('Блюдо добавлено')
#         return redirect(url_for('index'))
    
#     return render_template('form.html', mode='add', types=DISH_TYPES)

# @app.route('/edit/<int:index>', methods=['GET', 'POST'])
# def edit(index):
#     dish = storage.get_dish(index)
#     if not dish:
#         flash('Блюдо не найдено')
#         return redirect(url_for('index'))
    
#     if request.method == 'POST':
#         dish_type = request.form.get('type')
#         name = request.form.get('name')
#         price = float(request.form.get('price'))
#         calories = int(request.form.get('calories'))
#         ingredients = [i.strip() for i in request.form.get('ingredients', '').split(',') if i.strip()]
        
#         updated_dish = Dish(dish_type, name, price, calories, ingredients)
#         storage.edit_dish(index, updated_dish)
#         flash('Блюдо обновлено')
#         return redirect(url_for('index'))
    
#     return render_template('form.html', mode='edit', entity=dish, types=DISH_TYPES)

# @app.route('/delete/<int:index>', methods=['POST'])
# def delete(index):
#     storage.delete_dish(index)
#     flash('Блюдо удалено')
#     return redirect(url_for('index'))

# @app.route('/save', methods=['POST'])
# def save():
#     if storage.save_to_file():
#         flash('Данные сохранены')
#     else:
#         flash('Ошибка сохранения')
#     return redirect(url_for('index'))

# @app.route('/load', methods=['POST'])
# def load():
#     if storage.load_from_file():
#         flash('Данные загружены')
#     else:
#         flash('Ошибка загрузки')
#     return redirect(url_for('index'))

# @app.route('/clear', methods=['POST'])
# def clear():
#     storage.clear_all()
#     flash('Меню очищено')
#     return redirect(url_for('index'))

# if __name__ == '__main__':
#     app.run(debug=True)