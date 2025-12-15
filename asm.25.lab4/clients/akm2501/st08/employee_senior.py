from .employee_mid import employeeMid

class employeeSenior(employeeMid):
	typename = "Senior"
	def __init__(self):
		super().__init__()
		self.data.update({"mentees": ""})
		self.fields.append("mentees")
		self.fieldsCrit.append("onlyChars")




