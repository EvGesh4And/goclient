class container():
	def __init__(self, io, storage, classes):
		self.storage = storage
		self.io = io
		self.classes = classes

	def addEl(self, index, input_source):
		obj = self.classes[index]()
		obj.setIO(self.io)
		resp = None
		for i in obj.fields:
			resp = obj.input_(i, input_source)
			if resp != None:
				return resp
		self.storage.add(obj)

	def editEl(self, index, input_source):
		self.storage.edit(index, input_source)

	def delEl(self, index):
		self.storage.delete(index)

	def getObjsList(self):
		return self.storage.getObjsList()

	def clearList(self):
		self.storage.clear()

	def dumpList(self, filename = "data.lab4"):
		self.storage.dump(filename)

	def loadList(self, filename = "data.lab4"):
		return self.storage.load(filename)

	def getInfo(self):
		return self.storage.getInfo()
