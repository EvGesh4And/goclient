import requests
import json
from ..entities.student import Student
from ..entities.teacher import Teacher
from ..entities.staff import Staff
from .console import ConsoleIO

class RESTStorage:
    def __init__(self, base_url="http://127.0.0.1:5000", timeout=5.0):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self.student_number = self._find_student_number()
    
    def _find_student_number(self):
        """Найти номер студента в списке"""
        try:
            response = self.session.get(f"{self.base_url}/api/", timeout=self.timeout)
            if response.status_code == 200:
                data = response.json()
                for st_num, title in data.get('sts', []):
                    if 'Нуритдинов' in title:
                        return st_num
        except:
            pass
        return 8
    
    def _get_url(self, endpoint=""):
        return f"{self.base_url}/st{self.student_number}/api/{endpoint}".rstrip("/")
    
    def save(self, filename, data):
        try:
            response = self.session.delete(self._get_url("clear"), timeout=self.timeout)
            
            count = 0
            for obj in data:
                obj_data = {
                    "type": obj.__class__.__name__.lower()
                }
                
                for attr in dir(obj):
                    if not attr.startswith('_') and attr != 'io_strategy':
                        try:
                            value = getattr(obj, attr)
                            if isinstance(value, (str, int, float, bool, type(None))):
                                obj_data[attr] = value
                        except:
                            pass
                
                response = self.session.post(
                    self._get_url("people"),
                    json=obj_data,
                    headers={'Content-Type': 'application/json'},
                    timeout=self.timeout
                )
                
                if response.status_code in [200, 201]:
                    count += 1
            
            print(f" Отправлено {count} записей на сервер")
            return True
            
        except Exception as e:
            print(f" Ошибка отправки: {e}")
            return False
    
    def load(self, filename):
        try:
            response = self.session.get(self._get_url("people"), timeout=self.timeout)
            
            if response.status_code != 200:
                print(f" Ошибка сервера: {response.status_code}")
                return []
            
            data = response.json()
            
            if not data.get("success", False):
                print(f" Ошибка API: {data.get('error', 'Unknown')}")
                return []
            

            
            cls_map = {
                "student": Student,
                "teacher": Teacher,
                "staff": Staff
            }
            
            io = ConsoleIO()
            objects = []
            people_data = data.get("people", [])
            
            for item in people_data:
                cls_name = item.get("type", "").lower()
                cls = cls_map.get(cls_name)
                
                if cls:
                    obj = cls(io_strategy=io)
                    
                    if hasattr(obj, 'set_data_from_dict'):
                        obj.set_data_from_dict(item)
                    else:
                        for key, value in item.items():
                            if key not in ['type', 'id'] and hasattr(obj, key):
                                if hasattr(obj, 'edit_field'):
                                    try:
                                        obj.edit_field(key, value)
                                    except:
                                        setattr(obj, key, value)
                                else:
                                    setattr(obj, key, value)
                    
                    objects.append(obj)
            
            print(f" Загружено {len(objects)} записей с сервера")
            return objects
            
        except Exception as e:
            print(f" Ошибка загрузки: {e}")
            return []
    
    def add(self, obj):
        try:
            obj_data = {
                "type": obj.__class__.__name__.lower()
            }
            
            for attr in dir(obj):
                if not attr.startswith('_') and attr != 'io_strategy':
                    try:
                        value = getattr(obj, attr)
                        if isinstance(value, (str, int, float, bool, type(None))):
                            obj_data[attr] = value
                    except:
                        pass
            
            response = self.session.post(
                self._get_url("people"),
                json=obj_data,
                headers={'Content-Type': 'application/json'},
                timeout=self.timeout
            )
            
            return response.status_code in [200, 201]
                
        except Exception:
            return False