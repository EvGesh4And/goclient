from .employee import employee

class employeeJunior(employee):
	typename = "Junior"
	def __init__(self):
		super().__init__()
		self.data.update({"mentor": ""})
		self.fields.append("mentor")
		self.fieldsCrit.append("onlyChars")
