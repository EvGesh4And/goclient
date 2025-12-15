from .employee_junior import employeeJunior

class employeeMid(employeeJunior):
	typename = "Middle"
	def __init__(self):
		super().__init__()
		self.data.update({"experience": ""})
		self.fields.append("experience")
		self.fieldsCrit.append("onlyNum")




