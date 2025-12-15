import datetime

class MedicalItem:
    def __init__(self):
        self.id = 0
        self.name = ""
        self.specialty = ""
        self.category = ""
        self.schedule = ""
        self.staff_type = ""
        self.type = "MedicalItem"
        self.created = datetime.datetime.now()
    
    def get_type(self):
        return "Медицинский персонал"
    
    def input_fields(self, io_interface):
        self.name = io_interface.input_data("Введите имя: ")
        self.specialty = io_interface.input_data("Введите специальность: ")
        self.category = io_interface.input_data("Введите категорию: ")
        self.schedule = io_interface.input_data("Введите график работы: ")
    
    def output_fields(self, io_interface):
        io_interface.output_data(self.name, "Имя")
        io_interface.output_data(self.specialty, "Специальность")
        io_interface.output_data(self.category, "Категория")
        io_interface.output_data(self.schedule, "График работы")
    
    def to_dict(self):
        return {
            'id': self.id,
            'type': self.type,
            'name': self.name,
            'specialty': self.specialty,
            'category': self.category,
            'schedule': self.schedule,
            'staff_type': self.staff_type,
            'created': self.created.isoformat() if self.created else None
        }
    
    @classmethod
    def from_dict(cls, data):
        if data.get('type') == 'Nurse':
            obj = Nurse()
        elif data.get('type') == 'Doctor':
            obj = Doctor()
        else:
            obj = cls()
        
        obj.id = data.get('id', 0)
        obj.name = data.get('name', '')
        obj.specialty = data.get('specialty', '')
        obj.category = data.get('category', '')
        obj.schedule = data.get('schedule', '')
        obj.staff_type = data.get('staff_type', '')
        
        created = data.get('created')
        if created:
            obj.created = datetime.datetime.fromisoformat(created)
        
        return obj

class Nurse(MedicalItem):
    def __init__(self):
        super().__init__()
        self.procedure_room = ""
        self.shift = ""
        self.staff_type = "nurse"
        self.type = 'Nurse'
    
    def get_type(self):
        return "Медсестра"
    
    def input_fields(self, io_interface):
        super().input_fields(io_interface)
        self.procedure_room = io_interface.input_data("Введите процедурный кабинет: ")
        self.shift = io_interface.input_data("Введите смену: ")
    
    def output_fields(self, io_interface):
        super().output_fields(io_interface)
        io_interface.output_data(self.procedure_room, "Процедурный кабинет")
        io_interface.output_data(self.shift, "Смена")
    
    def to_dict(self):
        data = super().to_dict()
        data.update({
            'procedure_room': self.procedure_room,
            'shift': self.shift
        })
        return data
    
    @classmethod
    def from_dict(cls, data):
        obj = super().from_dict(data)
        obj.procedure_room = data.get('procedure_room', '')
        obj.shift = data.get('shift', '')
        return obj

class Doctor(MedicalItem):
    def __init__(self):
        super().__init__()
        self.license = ""
        self.specialization = ""
        self.staff_type = "doctor"
        self.type = 'Doctor'
    
    def get_type(self):
        return "Врач"
    
    def input_fields(self, io_interface):
        super().input_fields(io_interface)
        self.license = io_interface.input_data("Введите лицензию: ")
        self.specialization = io_interface.input_data("Введите специализацию: ")
    
    def output_fields(self, io_interface):
        super().output_fields(io_interface)
        io_interface.output_data(self.license, "Лицензия")
        io_interface.output_data(self.specialization, "Специализация")
    
    def to_dict(self):
        data = super().to_dict()
        data.update({
            'license': self.license,
            'specialization': self.specialization
        })
        return data
    
    @classmethod
    def from_dict(cls, data):
        obj = super().from_dict(data)
        obj.license = data.get('license', '')
        obj.specialization = data.get('specialization', '')
        return obj