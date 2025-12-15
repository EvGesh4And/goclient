class employee:
	typename = ""
	def __init__(self):
		self.io = None
		self.query_str_add = ""
		self.query_data_add = ""
		self.query_str_edit = ""
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

	def input_(self, name, source):
		return self.io.input_param(self, name, source)
		
	def output_(self, name):
		self.io.output_param(self, name)

	def getDataForQuery(self):
		arr = [self.data[field] for field in self.fields]
		arr.insert(0, self.typename)
		return arr
