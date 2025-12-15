class employee:
	typename = ""
	def __init__(self):
		self.io = None
		self.data = {
			"name": "",
			"email": "",
			"department": "",
			"salary": ""
			}
		self.fields = ["name", "email", "department", "salary"]
		self.fieldsCrit = ["onlyChars", "any", "onlyChars", "onlyNum"]

	def setIO(self, io):
		self.io = io

	def input_(self, name):
		self.io.input_param(self, name)
		
	def output_(self, name):
		self.io.output_param(self, name)
