import pickle
import os
import sys
import sqlite3

from app.akm2501.st08.employees import employee_junior

from .employees import employeeJunior
from .employees import employeeMid
from .employees import employeeSenior
from app.akm2501.st08 import employees, io_strat
from app import akm2501

class my_storage():
	def __init__(self, io, classes, db_path="data/akm2501/st08/data.lab4db"):
		os.makedirs("/".join(db_path.split('/')[:-1]), exist_ok=True)
		self.db_path = db_path
		sys.modules["employees"] = employees
		sys.modules["akm2501"] = akm2501
		sys.modules["io_strat"] = io_strat
		self.id_count = 0
		self.io = io
		self.classes = classes
		self.type_map = {cl.typename: i for i, cl in enumerate(self.classes)}
		self.__initDB()

	def __initDB(self):
		conn = sqlite3.connect(self.db_path)
		cursor = conn.cursor()
		cursor.execute('''
		CREATE TABLE IF NOT EXISTS employees (
			id INTEGER PRIMARY KEY,
			type TEXT NOT NULL,
			name TEXT NOT NULL,
			email TEXT NOT NULL,
			department TEXT NOT NULL,
			salary TEXT NOT NULL,
			mentor TEXT,
			experience TEXT,
			mentees TEXT
			)
		'''
			)
		conn.commit()
		conn.close()
		self.id_count = self.nextIndex()
		
	def countInTable(self):
		conn = sqlite3.connect(self.db_path)
		cursor = conn.cursor()
		cursor.execute("SELECT * FROM employees")
		l = len(cursor.fetchall())
		conn.close()
		return l

	def nextIndex(self):
		conn = sqlite3.connect(self.db_path)
		cursor = conn.cursor()
		cursor.execute("SELECT MAX(id) FROM employees")
		res = cursor.fetchall()[0]
		conn.close()
		l = res[0]
		if (l == None):
			return 0
		return l + 1

	def add(self, obj):
		query_data = obj.getDataForQuery()
		query_data.insert(0, self.id_count)
		self.id_count += 1

		query_str = f'''
		INSERT INTO employees (id, type, name, email, department, salary, mentor{obj.query_str_add})
		VALUES (?,?,?,?,?,?,?{obj.query_data_add})
		'''
		
		conn = sqlite3.connect(self.db_path)
		cursor = conn.cursor()
		cursor.execute(query_str, query_data)
		conn.commit()
		conn.close()

	def edit(self, index, input_source):
		conn = sqlite3.connect(self.db_path)
		cursor = conn.cursor()
		cursor.execute("SELECT * FROM employees WHERE id = ?", (index,))
		row = cursor.fetchall()[0]
		emp = self.classes[self.type_map[row[1]]]()
		for i in range(len(emp.fields)):
			emp.data[emp.fields[i]] = row[2 + i]
		emp.setIO(self.io)
		for i in emp.fields:
			emp.input_(i, input_source)
		
		query_str_add = ""
		query_data = emp.getDataForQuery()
		del query_data[0]
			
		query_data.append(index)

		query_str = f'''
		UPDATE employees
		SET name = ?, email = ?, department = ?, salary = ?, mentor = ?{emp.query_str_edit}
		WHERE id = ?
		'''

		conn = sqlite3.connect(self.db_path)
		cursor = conn.cursor()
		cursor.execute(query_str, query_data)
		conn.commit()
		conn.close()

	def delete(self, index):
		conn = sqlite3.connect(self.db_path)
		cursor = conn.cursor()
		cursor.execute("DELETE FROM employees WHERE id = ?", (index,))
		conn.commit()
		conn.close()

	def getObjsList(self):
		conn = sqlite3.connect(self.db_path)
		cursor = conn.cursor()
		cursor.execute('SELECT * FROM employees')
		rows_q = cursor.fetchall()
		res = []
		for row_q in rows_q:
			ttt = self.classes[self.type_map[row_q[1]]]()
			row = {ttt.fields[i]: row_q[2 + i] for i in range(len(ttt.fields))}
			row["_type"] = row_q[1]
			row["_index"] = row_q[0]
			res.append(row)
		conn.close()
		return res

	def employeesByParam(self, param, value):
		conn = sqlite3.connect(self.db_path)
		cursor = conn.cursor()
		cursor.execute(f'SELECT * FROM employees WHERE {param} = ?', (value,))
		t = cursor.fetchall()
		conn.close()
		return t

	def getPrevStorage(self):
		conn = sqlite3.connect(self.db_path)
		cursor = conn.cursor()
		cursor.execute('SELECT * FROM employees')
		rows_q = cursor.fetchall()
		res = []
		for row_q in rows_q:
			ttt = self.classes[self.type_map[row_q[1]]]()
			i = 2
			for field in ttt.fields:
				ttt.data[field] = row_q[i]
				i += 1
			res.append(ttt)
		conn.close()
		return res

	def clear(self):
		conn = sqlite3.connect(self.db_path)
		cursor = conn.cursor()
		cursor.execute("DELETE FROM employees")
		conn.commit()
		conn.close()
		self.id_count = 0

	def dump(self, filename):
		f_path = "/".join(self.db_path.split('/')[:-1]) + '/' + filename
		f = open(f_path, "wb")
		pickle.dump(self.getPrevStorage(), f)
		f.close()

	def load(self, filename):
		base_path = "/".join(self.db_path.split('/')[:-1]) + '/'
		storage = []
		try:
			f = open(base_path + filename, "rb")
			storage = pickle.load(f)
			f.close()
		except FileNotFoundError:
			storage = []

		self.clear()
		for obj in storage:
			self.add(obj)
		return filename

	def getInfo(self):
		stats = { "Total": self.countInTable() }
		for cl in self.classes:
			stats.update({cl.typename: len(self.employeesByParam("type", cl.typename))})
		return stats
