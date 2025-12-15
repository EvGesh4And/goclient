class consoleIO:
	def input_param(self, obj, param):
		while 1:
			data = input(f"Введите новое значение '{param}': ")
			index = obj.fields.index(param)
			if data == '':
				break
			f = False
			if (self.checkInput(data, obj.fieldsCrit[index])):
				f = True
			if (not f):
				self.output_(f"Неправильное значение: {param} принимает {obj.fieldsCrit[index]}")
				continue
			obj.data[param] = data
			break

	def output_param(self, obj, param):
		print(obj.data[param])

	def input_(self, text=""):
		return input(text)

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
