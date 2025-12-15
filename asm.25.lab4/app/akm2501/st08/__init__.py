from flask import Blueprint
from .group import group

bp = Blueprint('st0108', __name__)

gr = group()

@bp.route('/')
def home():
	return gr.home()

@bp.route("/employees")
def list_employees():
	return gr.list_employees()

@bp.route("/employees/add", methods=["GET", "POST"])
def add_employee():
	return gr.add_employee()

@bp.route("/employees/<int:idx>/edit", methods=["GET", "POST"])
def edit_employee(idx: int):
	return gr.edit_employee(idx)

@bp.route("/employees/<int:idx>/delete")
def delete_employee(idx: int):
	return gr.delete_employee(idx)

@bp.route("/save")
def save_data():
	return gr.save_data()

@bp.route("/load")
def load_data():
	return gr.load_data()

@bp.route("/restore")
def restore_data():
	return gr.restore_data()

@bp.route("/clear")
def clear_data():
	return gr.clear_data()

############ API ############

@bp.route("/api/", methods=['GET'])
def home_api():
	return gr.home_api()

@bp.route("/api/employees", methods=['GET'])
def list_employees_api():
	return gr.list_employees_api()

@bp.route("/api/employees/add", methods=["POST"])
def add_employee_api():
	return gr.add_employee_api()

@bp.route("/api/employees/<int:idx>/edit", methods=["GET", "POST"])
def edit_employee_api(idx: int):
	return gr.edit_employee_api(idx)

@bp.route("/api/employees/<int:idx>/delete", methods=['POST'])
def delete_employee_api(idx: int):
	return gr.delete_employee_api(idx)

@bp.route("/api/save", methods=['POST'])
def save_data_api():
	return gr.save_data_api()

@bp.route("/api/load", methods=['POST'])
def load_data_api():
	return gr.load_data_api()

@bp.route("/api/restore", methods=['POST'])
def restore_data_api():
	return gr.restore_data_api()

@bp.route("/api/clear", methods=['POST'])
def clear_data_api():
	return gr.clear_data_api()
