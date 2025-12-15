import requests

class restStorage:
	def __init__(self, classes, io, base_url="http://127.0.0.1:5000", module_name="[2501-08]"):
		self.io = io
		self.classes = classes
		self.type_map = {cl.typename: i for i, cl in enumerate(self.classes)}
		self.base_url = base_url
		self.module_name = module_name
		self.timeout = 10
		self.session = requests.Session()
		self.mid_url = f"{base_url.rstrip('/')}/{self._prefix()}/api/"
		
	def _prefix(self):
		resp = self.session.get(f"{self.base_url}/api/", timeout=self.timeout)
		data = resp.json()
		arr = data.get("sts", [])
		for ind, title in arr:
			if self.module_name in title:
				return f"st{ind}"

	def add(self, obj):
		final_url = self.mid_url + "employees/add"
		data = {f: obj.data[f] for f in obj.fields}
		ret = self.session.post(final_url, params=data)
		return None if ret.status_code == 200 else ret.status_code

	def edit(self, index):
		final_url = self.mid_url + f"employees/{index}/edit"
		ret = self.session.get(final_url)
		ret = ret.json()
		clss = self.classes[self.type_map[ret["message"]]]()
		clss.setIO(self.io)
		for f in ret["fields"]:
			clss.input_(f)
		data = {f: clss.data[f] for f in ret["fields"]}
		ret = self.session.post(final_url, params=data)
		return None if ret.status_code == 200 else ret.status_code

	def delete(self, index):
		final_url = self.mid_url + f"employees/{index}/delete"
		ret = self.session.post(final_url)
		return None if ret.status_code == 200 else ret.status_code

	def getObjsList(self):
		final_url = self.mid_url + "employees"
		ret = self.session.get(final_url)
		return ret.json()["employees"]

	def clear(self):
		final_url = self.mid_url + "clear"
		ret = self.session.post(final_url)
		return None if ret.status_code == 200 else ret.status_code

	def dump(self, filename):
		final_url = self.mid_url + "save"
		ret = self.session.post(final_url)
		return None if ret.status_code == 200 else ret.status_code

	def load(self, filename):
		final_url = self.mid_url + "load"
		ret = self.session.post(final_url)
		return None if ret.status_code == 200 else ret.status_code

	def getInfo(self):
		final_url = self.mid_url
		ret = self.session.get(final_url)
		return ret
