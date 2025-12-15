from flask import Blueprint, render_template, request, redirect, url_for, abort, g, jsonify
import os
from .company import Company
from .strategy_io import Flask_IO
from .storage import SQLite_Storage
from .employee import Employee
from .manager import Manager
from .director import Director


def create_blueprint_and_routes():
    this_dir = os.path.dirname(__file__)
    student_dir_name = os.path.basename(this_dir)
    project_root = os.path.abspath(os.path.join(this_dir, '..', '..', '..'))
    templates_folder = os.path.join(project_root, 'app', 'templates', 'asm2504', student_dir_name)
    storage_folder = os.path.join(project_root, 'data', 'asm2504', student_dir_name)
    template_prefix = f'asm2504/{os.path.basename(os.path.dirname(__file__))}'

    bp = Blueprint(student_dir_name, __name__, template_folder=templates_folder)
    bp.storage_folder = storage_folder

    @bp.before_request
    def setup_company():
        pickle_path = os.path.join(bp.storage_folder, 'data.pkl')
        db_path = os.path.join(bp.storage_folder, 'company.db')

        g.storage = SQLite_Storage(db_path=db_path, pickle_path=pickle_path)
        g.company = Company(Flask_IO(), g.storage)

    @bp.teardown_request
    def teardown_db(exception=None):
        db = g.pop('db', None)
        if db is not None:
            db.close()

    @bp.route('/')
    def index():
        return render_template(f'{template_prefix}/index.html', employees=g.company.get_employees())

    @bp.route('/init_db')
    def init_database():
        g.company.init_storage()
        return redirect(url_for('.index'))

    @bp.route('/add', methods=['GET', 'POST'])
    def add_employee():
        if request.method == 'POST' and request.form.get('employee_type'):
            g.company.add_element(request.form.get('employee_type'))
            return redirect(url_for('.index'))
        return render_template(f'{template_prefix}/add_an_employee.html')

    @bp.route('/employee/<int:emp_id>')
    def employee_details(emp_id):
        employee = g.company.get_employee_by_id(emp_id)
        if not employee:
            abort(404)
        return render_template(f'{template_prefix}/employee_details.html', employee=employee)

    @bp.route('/edit/<int:emp_id>', methods=['GET', 'POST'])
    def edit_employee(emp_id):
        employee = g.company.get_employee_by_id(emp_id)
        if not employee:
            abort(404)
        if request.method == 'POST':
            g.company.update_employee(emp_id, request.form)
            return redirect(url_for('.employee_details', emp_id=emp_id))
        return render_template(f'{template_prefix}/edit_employee.html', employee=employee)

    @bp.route('/delete/all', methods=['POST'])
    def delete_all_employees():
        g.company.delete_all_elements()
        return redirect(url_for('.index'))

    @bp.route('/delete/<int:emp_id>', methods=['POST'])
    def delete_employee(emp_id):
        g.company.delete_element(emp_id)
        return redirect(url_for('.index'))

    @bp.route('/save', methods=['POST'])
    def save_to_file():
        g.company.save_elements()
        return redirect(url_for('.index'))

    @bp.route('/load', methods=['POST'])
    def load_from_file():
        g.company.load_elements()
        return redirect(url_for('.index'))

    def emp_to_dict(obj):
        data = {
            'id': obj.id,
            'type': obj.title,
            'name': obj.name,
            'age': obj.age,
            'sex': obj.sex,
            'department': obj.department,
            'salary': obj.salary
        }
        if hasattr(obj, 'team_size'):
            data['team_size'] = obj.team_size
        if hasattr(obj, 'assistant'):
            data['assistant'] = obj.assistant
        return data

    @bp.route('/api/employees', methods=['GET'])
    def api_get_all():
        employees = g.storage.get_employees()
        return jsonify([emp_to_dict(emp) for emp in employees])

    @bp.route('/api/employees/<int:emp_id>', methods=['GET'])
    def api_get_one(emp_id):
        employee = g.storage.get_by_id(emp_id)
        if not employee:
            return jsonify({'error': 'Not found'}), 404
        return jsonify(emp_to_dict(employee))

    @bp.route('/api/employees', methods=['POST'])
    def api_add():
        data = request.json
        cls_map = {'Employee': Employee, 'Manager': Manager, 'Director': Director}
        cls = cls_map.get(data.get('type'), Employee)

        new_emp = cls(None)

        ignore = ['id', 'type']
        for k, v in data.items():
            if k not in ignore and hasattr(new_emp, k):
                setattr(new_emp, k, v)

        g.storage.add_element(new_emp)

        return jsonify(emp_to_dict(new_emp)), 201

    @bp.route('/api/employees/<int:emp_id>', methods=['PUT'])
    def api_update(emp_id):
        employee = g.storage.get_by_id(emp_id)
        if not employee:
            return jsonify({'error': 'Not found'}), 404

        data = request.json
        for k, v in data.items():
            if k != 'id' and hasattr(employee, k):
                setattr(employee, k, v)

        g.storage.update(employee)
        return jsonify(emp_to_dict(employee))

    @bp.route('/api/employees/<int:emp_id>', methods=['DELETE'])
    def api_delete(emp_id):
        g.storage.delete_employee(emp_id)
        return jsonify({'status': 'deleted'})

    @bp.route('/api/employees', methods=['DELETE'])
    def api_delete_all():
        g.storage.delete_all_employees()
        return jsonify({'status': 'all deleted'})

    @bp.route('/api/employees/save', methods=['POST'])
    def api_save():
        try:
            g.company.save_elements()
            return jsonify({'status': 'saved'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @bp.route('/api/employees/load', methods=['POST'])
    def api_load():
        try:
            g.company.load_elements()
            employees = g.storage.get_employees()
            return jsonify([emp_to_dict(emp) for emp in employees]), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    return bp


bp = create_blueprint_and_routes()