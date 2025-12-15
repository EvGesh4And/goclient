from .container import container
from .consoleIO import consoleIO
from .storagePickle import pickleStorage
from .storageRest import restStorage
from .employee_junior import employeeJunior
from .employee_mid import employeeMid
from .employee_senior import employeeSenior

def f1(arg):
	for i in range(len(arg[1].classes)):
		arg[0].output_(f"{i + 1}: {arg[1].classes[i].typename}")
	ans = arg[0].input_("Введите индекс желаемой должности: ")
	f = False
	if (arg[0].checkInput(ans, "onlyNum")):
		t = int(ans)
		if ((t > 0) and (t <= len(arg[1].classes))):
			f = True
	if (not f):
		arg[0].output_("Неправильный индекс")
		return
	ret = arg[1].addEl(int(ans) - 1)
	if (ret == None):
		arg[0].output_("Пользователь добавлен успешно")
	else:
		arg[0].output_(f"Ошибка добавления пользователя: {ret}")

def f4(arg):
	arr = arg[1].getObjsList()
	arg[0].output_("-" * 20)
	for i in range(len(arr)):
		temp_dict = {k: v for k, v in arr[i].items() if not k.startswith('_')}
		temp_v = arr[i]["_type"]
		temp_idx = arr[i]["_index"]
		arg[0].output_(f"{temp_idx}: {temp_v} : {temp_dict}")
	arg[0].output_("-" * 20)
	return arr

def f2(arg):
	t_arr = f4(arg)
	t_arr = [el["_index"] for el in t_arr]
	ans = arg[0].input_("Введите индекс пользователя для редактирования: ")
	f = False
	if (arg[0].checkInput(ans, "onlyNum")):
		t = int(ans)
		if t_arr.count(t) > 0:
			f = True
	if (not f):
		arg[0].output_("Неправильный индекс")
		return
	index = int(ans)
	ret = arg[1].editEl(index)
	if ret == None:
		arg[0].output_("Пользователь изменён успешно")
	else:
		arg[0].output_(f"Ошибка изменения пользователя: {ret}")

def f3(arg):
	t_arr = f4(arg)
	t_arr = [el["_index"] for el in t_arr]
	ans = arg[0].input_("Введите индекс пользователя для удаления: ")
	f = False
	if (arg[0].checkInput(ans, "onlyNum")):
		t = int(ans)
		if t_arr.count(t) > 0:
			f = True
	if (not f):
		arg[0].output_("Неправильный индекс")
		return
	index = int(ans)
	ret = arg[1].delEl(index)
	if ret == None:
		arg[0].output_("Пользователь удалён успешно")
	else:
		arg[0].output_(f"Ошибка удаления пользователя: {ret}")

def f5(arg):
	arg[1].dumpList()
	arg[0].output_('-' * 20)

def f6(arg):
	arg[1].loadList()
	arg[0].output_('-' * 20)

def f7(arg):
	arg[1].clearList()
	arg[0].output_('-' * 20)

def f0(arg):
	pass

ACTIONS_ = {
	"1": ("Добавить сотрудника", f1),
	"2": ("Редактировать сотрудника", f2),
	"3": ("Удалить сотрудника", f3),
	"4": ("Вывести список всех сотрудников", f4),
	"5": ("Сохранить в файл", f5),
	"6": ("Загрузить из файла", f6),
	"7": ("Очистить список", f7),
	"0": ("Выход", f0)
	}

def printActions(io):
	for i in ACTIONS_:
		io.output_(f"{i}: {ACTIONS_[i][0]}")

def menu_f():
	classes = [
			employeeJunior,
			employeeMid,
			employeeSenior]
	io = consoleIO()
	stor = None
	t = None
	storage_choice = io.input_("Выберите тип хранилища:\n0: PickleStorage\n1: RestStorage\nХранилище: ")
	if io.checkInput(storage_choice, "onlyNum"):
		t = int(storage_choice)
	else:
		io.output_("Неправильный индекс")
		return
	if t == 0:
		stor = pickleStorage(classes)
	else:
		stor = restStorage(classes, io)
	io.output_("-"*20)
	cont = container(io, stor, classes)

	while 1:
		printActions(io)
		f = False
		ans = io.input_("Введите номер действия: ")
		if (io.checkInput(ans, "onlyNum")):
			t = int(ans)
			if ((t >= 0) and (t <= 7)):
				f = True
		if (not f):
			io.output_("Неправильный индекс")
			continue
		if (ans == "0"):
			break
		ACTIONS_[ans][1]((io, cont))
