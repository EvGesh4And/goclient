import os
from flask import Blueprint, render_template, request, redirect, url_for, g, flash, current_app

def create_bp():
    this_dir = os.path.dirname(__file__)
    student_dir = os.path.basename(this_dir)
    project_dir = os.path.abspath(os.path.join(this_dir, '..', '..', '..'))
    templates_dir = os.path.join(project_dir, 'app', 'templates', 'asm2504', student_dir)
    static_dir = os.path.join(project_dir, 'app', 'static', 'asm2504', student_dir)

    bp = Blueprint(
        student_dir, __name__,
        template_folder=templates_dir,
        static_folder=static_dir
    )
    return bp

bp = create_bp()

from .company import Company
from .io_strategy import FlaskIO
from .storage import SQLiteStorage


def get_io():
    if '_io' not in g:
        g._io = FlaskIO()
    return g._io


def get_storage():
    if '_storage' not in g:
        g._storage = SQLiteStorage()
    return g._storage


def get_company():
    if '_company' not in g:
        g._company = Company(get_storage(), get_io())
    return g._company

@bp.route('/')
def index():
    employees = get_company().get_employee_list()
    message = request.args.get('message', '')
    return render_template("asm2504/st24/index.html",
                           employees=employees,
                           message=message,
                           s="st24.index()")

@bp.route('/add', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        emp_type = request.form.get('emp_type')
        if emp_type in ['Employee', 'Manager', 'Director']:
            get_company().add_employee(emp_type)
            return redirect(url_for('st24.index', message='Сотрудник добавлен'))
    return render_template("asm2504/st24/add.html", s="st24.add_employee()")

@bp.route('/edit/<emp_id>', methods=['GET', 'POST'])
def edit_employee(emp_id):
    company = get_company()
    emp = company.storage.get_by_id(emp_id)
    if not emp:
        return redirect(url_for('st24.index', message='Сотрудник не найден'))

    if request.method == 'POST':
        emp.input_data() 
        company.storage.update_by_id(emp_id, emp)
        return redirect(url_for('st24.index', message='Сотрудник обновлён'))

    return render_template("asm2504/st24/edit.html",
                           emp=emp.output_data(),
                           emp_type=emp.__class__.__name__,
                           s="st24.edit_employee()")

@bp.route('/delete/<emp_id>')
def delete_employee(emp_id):
    if get_company().delete_employee(emp_id):
        return redirect(url_for('st24.index', message='Сотрудник удалён'))
    return redirect(url_for('st24.index', message='Ошибка удаления'))

@bp.route('/list')
def employee_list():
    employees = get_company().get_employee_list()
    return render_template("asm2504/st24/list.html", employees=employees, s="st24.employee_list()")

@bp.route('/save', methods=['GET', 'POST'])
def save_to_file():
    if request.method == 'POST':
        filename = request.form.get('filename', 'backup.pkl')
        path = get_company().save_to_file(filename)
        return redirect(url_for('st24.index', message=f'Сохранено в {path}'))
    return render_template("asm2504/st24/save.html", s="st24.save_to_file()")

@bp.route('/load', methods=['GET', 'POST'])
def load_from_file():
    if request.method == 'POST':
        filename = request.form.get('filename')
        if filename:
            success = get_company().load_from_file(filename)
            msg = 'Данные загружены' if success else 'Ошибка загрузки'
            return redirect(url_for('st24.index', message=msg))
    return render_template("asm2504/st24/load.html", s="st24.load_from_file()")

@bp.route('/clear')
def clear_list():
    get_company().clear_list()
    return redirect(url_for('st24.index', message='Список очищен'))

from .api import register_api
register_api(bp)