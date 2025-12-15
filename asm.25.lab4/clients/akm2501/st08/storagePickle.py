import pickle

class pickleStorage:
	def __init__(self, classes, base_data_path = "data/akm2501/st08/"):
		self.storage = []
		self.classes = classes
		self.base_data_path = base_data_path

	def add(self, obj):
		self.storage.append(obj)

	def edit(self, index):
		for f in self.storage[index].fields:
			self.storage[index].input_(f)

	def delete(self, index):
		del self.storage[index]

	def getObjsList(self):
		res = []
		for ind, emp in enumerate(self.storage):
			row = {f: emp.data[f] for f in emp.fields}
			row["_type"] = emp.typename
			row["_index"] = ind
			res.append(row)
		return res

	def clear(self):
		self.storage.clear()

	def dump(self, filename):
		f = open(self.base_data_path + filename, "wb")
		pickle.dump(self.storage, f)
		f.close()
		return filename

	def load(self, filename):
		self.clear()
		try:
			f = open(self.base_data_path + filename, "rb")
			self.storage = pickle.load(f)
			f.close()
		except FileNotFoundError:
			pass
		return filename

	def getInfo(self):
		stats = { "Total": len(self.storage) }
		for cl in self.classes:
			stats.update({ cl.typename: len(self.employeesByParam("typename", cl.typename)) })

	def employeesByParam(self, param, value):
		k = 0
		for emp in self.storage:
			if hasattr(emp, param):
				if getattr(emp, param) == value:
					k += 1
					continue
			if emp.data[param] == value:
				k += 1
		return k
