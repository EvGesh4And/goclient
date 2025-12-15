from flask import request

class io_class:
	def input_param(self, obj, param, source):
		data = source.get(param, "")
		index = obj.fields.index(param)
		if data == '':
			return
		if (not self.checkInput(data, obj.fieldsCrit[index])):
			return f"Неправильное значение: {param} принимает {obj.fieldsCrit[index]}"
		else:
			obj.data[param] = data

	def output_param(self, obj, param):
		self.output_(obj.data[param])

	def input_raw(self, source, field_name=""):
		return source.get(field_name, "")

	def output_(self, text):
		print(text)

	def checkInput(self, s, type_s):
		match type_s:
			case "onlyChars":
				return s.replace(" ", "").isalpha()
			case "onlyNum":
				return s.isnumeric()
			case "any":
				return True
		return False
