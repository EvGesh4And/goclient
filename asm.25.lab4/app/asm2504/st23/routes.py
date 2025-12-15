import os
import sys

current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, current_dir)

from flask import render_template, request, redirect, url_for
from . import bp
from .storage import Storage
from .group import Group
from .flask_io import FlaskIOStrategy

storage = Storage()
flask_io = FlaskIOStrategy()
web_group = Group(storage, flask_io)


@bp.route('/')
def index():
    dishes_data = web_group.show_all()
    message = request.args.get('message', '')
    return render_template('asm2504/st23/index.html',
                           dishes=dishes_data,
                           message=message)


@bp.route('/delete/<int:index>')
def delete_dish(index):
    if web_group.delete(index):
        return redirect(url_for('bp.index', message='Блюдо успешно удалено!'))
    else:
        return redirect(url_for('bp.index', message='Блюдо не найдено.'))


@bp.route('/clear')
def clear_all():
    web_group.clear()
    return redirect(url_for('bp.index', message='Все блюда удалены!'))


@bp.route('/add', methods=['GET', 'POST'])
def add_dish():
    if request.method == 'GET':
        return web_group.prepare_add_form()
    elif request.method == 'POST':
        dish_type = request.form.get('dish_type')
        if web_group.add(dish_type, request.form):
            return redirect(url_for('bp.index', message='Блюдо успешно добавлено!'))
        else:
            return web_group.prepare_add_form()


@bp.route('/edit/<int:index>', methods=['GET', 'POST'])
def edit_dish(index):
    if request.method == 'GET':
        result = web_group.prepare_edit_form(index)
        if result:
            return result
        else:
            return redirect(url_for('bp.index', message='Блюдо не найдено.'))
    elif request.method == 'POST':
        if web_group.edit(index, request.form):
            return redirect(url_for('bp.index', message='Блюдо успешно обновлено!'))
        else:
            return web_group.prepare_edit_form(index, error_message="Ошибка при обновлении блюда")


@bp.route('/load', methods=['GET', 'POST'])
def load_data():
    if request.method == 'GET':
        return web_group.prepare_load_form()
    elif request.method == 'POST':
        filename = request.form.get('filename', '').strip()
        if not filename:
            return redirect(url_for('bp.load_data', message='Введите название файла!'))

        if storage.load_from_pickle(filename):
            return redirect(url_for('bp.index', message=f'Данные загружены из файла {filename}!'))
        else:
            return redirect(url_for('bp.load_data', message='Ошибка при загрузке данных!'))


@bp.route('/save', methods=['GET', 'POST'])
def save_data():
    if request.method == 'GET':
        return web_group.prepare_save_form()
    elif request.method == 'POST':
        filename = request.form.get('filename', '').strip()
        if not filename:
            return redirect(url_for('bp.save_data', message='Введите название файла!'))

        if storage.save_to_pickle(filename):
            return redirect(url_for('bp.index', message=f'Данные сохранены в файл {filename}!'))
        else:
            return redirect(url_for('bp.save_data', message='Ошибка при сохранении данных!'))