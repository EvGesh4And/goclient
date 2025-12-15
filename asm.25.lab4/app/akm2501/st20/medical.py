from dataclasses import dataclass
import datetime

@dataclass
class MedicalItem:
    id: int = 0
    name: str = ''
    specialty: str = ''
    category: str = ''
    schedule: str = ''
    staff_type: str = ''
   
    def __post_init__(self):
        self.created = datetime.datetime.now()
        self.type = 'MedicalItem'

    def get_type(self):
        return "Медицинский персонал"
    
    def set_form_data(self, form_data):
        self.name = form_data.get('name', '')
        self.specialty = form_data.get('specialty', '')
        self.category = form_data.get('category', '')
        self.schedule = form_data.get('schedule', '')
        self.staff_type = form_data.get('staff_type', self.staff_type or 'nurse')
    
    def __getstate__(self):
        return self.__dict__.copy()
    
    def __setstate__(self, state):
        self.__dict__.update(state)
    
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
    
    def set_form_data(self, form_data):
        super().set_form_data(form_data)
        self.procedure_room = form_data.get('procedure_room', '')
        self.shift = form_data.get('shift', '')
    
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
    
    def set_form_data(self, form_data):
        super().set_form_data(form_data)
        self.license = form_data.get('license', '')
        self.specialization = form_data.get('specialization', '')
    
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