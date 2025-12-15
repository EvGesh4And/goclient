from flask import render_template
from flask import request
from flask import url_for
from flask import redirect
from flask import jsonify
from flask import Response
		
from .container import container
from .io_strat import io_class
from .employees import employeeJunior
from .employees import employeeMid
from .employees import employeeSenior
from .storage import my_storage

class group:
	def __init__(self):
		self.classes = [
			employeeJunior,
			employeeMid,
			employeeSenior]
		self.type_map = {cl.typename: i for i, cl in enumerate(self.classes)}

		self.io_ = io_class()
		self.my_strg = my_storage(self.io_, self.classes)
		self.employees = container(self.io_, self.my_strg, self.classes)
		self._empSen_ = employeeSenior()

	def home(self):
		message = request.args.get("message", '')
		return render_template(
			"akm2501/st08/home.html",
			stats=self.employees.getInfo(),
			message=message)

	def list_employees(self):
		message = request.args.get("message", '')
		return render_template(
			"akm2501/st08/employees.html",
			employees=self.employees.getObjsList(),
			message=message)

	def add_employee(self):
		message = request.args.get("message", '')
		if request.method == "POST":
			idx = int(request.form.get("type", 0))
			resp = self.employees.addEl(idx)
			if resp != None:
				return redirect(url_for("st0108.add_employee", message=resp))
			return redirect(url_for("st0108.list_employees", message="Сотрудник добавлен"))
		fields = self._empSen_.fields
		return render_template(
			"akm2501/st08/employee_form.html",
			title="Добавить сотрудника",
			fields=fields,
			data={},
			type_selected=0,
			lock_type=False,
			message=message)

	def edit_employee(self, idx: int):
		if request.method == "POST":
			resp = self.employees.editEl(idx, request.form)
			if resp != None:
				return redirect(url_for("st0108.edit_employee", message=resp))
			return redirect(url_for("st0108.list_employees", message="Изменения сохранены"))
		obj_list = self.employees.getObjsList()
		t_type = None
		local_idx = None
		for i in range(len(obj_list)):
			if obj_list[i]["_index"] == idx:
				local_idx = i
				t_type = obj_list[i]["_type"]
				break
		if t_type == None:
			return redirect(url_for("st0108.list_employees", message="Нет такого сотрудника"))
		data = {k: v for k, v in obj_list[local_idx].items() if not k.startswith('_')}
		clss = self.classes[self.type_map[t_type]]()
		fields = clss.fields
		return render_template(
			"akm2501/st08/employee_form.html",
			title="Редактировать сотрудника",
			fields=fields,
			data=data,
			type_selected=self.type_map[t],
			lock_type=True)

	def delete_employee(self, idx: int):
		self.employees.delEl(idx)
		return redirect(url_for("st0108.list_employees", message="Сотрудник удалён"))

	def save_data(self):
		f_name = "data.lab4"
		self.employees.dumpList(f_name)
		return redirect(url_for("st0108.list_employees", message=f"Данные сохранены в {f_name}"))

	def load_data(self):
		f_name = self.employees.loadList("data.lab4")
		return redirect(url_for("st0108.list_employees", message=f"Данные загружены из {f_name}"))

	def restore_data(self):
		f_name = self.employees.loadList("data.lab2")
		return redirect(url_for("st0108.list_employees", message=f"Данные загружены из {f_name}"))

	def clear_data(self):
		self.employees.clearList()
		return redirect(url_for("st0108.list_employees", message="Данные очищены"))

	############ API ############

	def home_api(self):
		resp = {
			"stats": self.employees.getInfo()
			}
		return jsonify(resp)

	def list_employees_api(self):
		resp = {
			"employees": self.employees.getObjsList()
			}
		return jsonify(resp)

	def add_employee_api(self):
		idx = int(request.args.get("type", 0))
		resp_ = self.employees.addEl(idx, request.args)
		if resp_ != None:
			temp_arr = resp_.split(' ')
			resp = {
				"message": resp_,
				"field": temp_arr[2],
				"criteria": temp_arr[4]
				}
			resp = jsonify(resp)
			resp.status_code = 406
			return resp
		resp = {
			"message": "Сотрудник добавлен"
			}
		return jsonify(resp)

	def edit_employee_api(self, idx: int):
		if request.method == "POST":
			resp_ = self.employees.editEl(idx, request.args)
			if resp_ != None:
				temp_arr = resp_.split(' ')
				resp = {
					"message": resp_,
					"field": temp_arr[2],
					"criteria": temp_arr[4]
					}
				resp = jsonify(resp)
				resp.status_code = 406
				return resp
			resp = {
				"message": "Изменения сохранены"
				}
			return jsonify(resp)
		obj_list = self.employees.getObjsList()
		t_type = None
		for i in range(len(obj_list)):
			if obj_list[i]["_index"] == idx:
				t_type = obj_list[i]["_type"]
				break
		if t_type == None:
			resp = {
				"message": f"Нет сотрудника с номером: {idx}"
				}
			resp = jsonify(resp)
			resp.status_code = 400
			return resp
		clss = self.classes[self.type_map[t_type]]()
		resp = {
			"message": f"{t_type}",
			"fields": [f for f in clss.fields]
			}
		return jsonify(resp)

	def delete_employee_api(self, idx: int):
		self.employees.delEl(idx)
		resp = {
			"message": "Сотрудник удалён"
			}
		return jsonify(resp)

	def save_data_api(self):
		f_name = "data.lab4"
		self.employees.dumpList(f_name)
		return jsonify({"message": f"Данные сохранены в {f_name}"})

	def load_data_api(self):
		f_name = self.employees.loadList("data.lab4")
		return jsonify({"message": f"Данные загружены из {f_name}"})

	def restore_data_api(self):
		f_name = self.employees.loadList("data.lab2")
		return jsonify({"message": f"Данные загружены из {f_name}"})

	def clear_data_api(self):
		self.employees.clearList()
		return jsonify({"message": "Данные очищены"})
