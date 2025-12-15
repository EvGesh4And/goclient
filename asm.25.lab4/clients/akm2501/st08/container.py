# class container():
# 	def __init__(self, io, storage, classes):
# 		self.storage = storage
# 		self.io = io
# 		self.classes = classes
# 		self.type_map = {cl.typename: i for i, cl in enumerate(self.classes)}

# 	def addEl(self, index):
# 		obj = self.classes[index]()
# 		obj.typename = self.type_map[index]
# 		obj.setIO(self.io)
# 		for i in obj.fields:
# 			obj.input_(i)
# 		self.storage.append(obj)
# 		return obj

# 	def editEl(self, index, param):
# 		self.storage[index].input_(param)

# 	def delEl(self, index):
# 		self.storage.remove(index)

# 	def getObjsList(self):
# 		return self.storage

# 	def clearList(self):
# 		self.storage.clear()

# 	def dumpList(self):
# 		self.pickle.save("data.lab1", self.storage)

# 	def loadList(self):
# 		self.storage = self.pickle.load("data.lab1")

class container():
	def __init__(self, io, storage, classes):
		self.storage = storage
		self.io = io
		self.classes = classes

	def addEl(self, index):
		obj = self.classes[index]()
		obj.setIO(self.io)
		resp = None
		for i in obj.fields:
			resp = obj.input_(i)
			if resp != None:
				return resp
		self.storage.add(obj)

	def editEl(self, index):
		self.storage.edit(index)

	def delEl(self, index):
		self.storage.delete(index)

	def getObjsList(self):
		return self.storage.getObjsList()

	def clearList(self):
		self.storage.clear()

	def dumpList(self, filename = "data.lab1"):
		self.storage.dump(filename)

	def loadList(self, filename = "data.lab1"):
		return self.storage.load(filename)

	def getInfo(self):
		return self.storage.getInfo()

