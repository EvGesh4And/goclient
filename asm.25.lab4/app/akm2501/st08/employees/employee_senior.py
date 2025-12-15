from .employee_mid import employeeMid

class employeeSenior(employeeMid):
	typename = "Senior"
	def __init__(self):
		super().__init__()
		self.query_str_add += ", mentees"
		self.query_data_add += ",?"
		self.query_str_edit += ", mentees = ?"
		self.data.update({"mentees": ""})
		self.fields.append("mentees")
		self.fieldsCrit.append("onlyChars")
