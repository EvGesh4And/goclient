from .employee_junior import employeeJunior

class employeeMid(employeeJunior):
	typename = "Middle"
	def __init__(self):
		super().__init__()
		self.query_str_add += ", experience"
		self.query_data_add += ",?"
		self.query_str_edit += ", experience = ?"
		self.data.update({"experience": ""})
		self.fields.append("experience")
		self.fieldsCrit.append("onlyNum")
