from ..entities.student import Student
from ..entities.teacher import Teacher
from ..entities.staff import Staff

class APIIO:
    def get_fields(self, obj):
        from .flask_io import FlaskIO
        
        flask_io = FlaskIO()
        fields = flask_io.get_fields(obj)

        fields["type"] = obj.__class__.__name__.lower()

        if "io_strategy" in fields:
            del fields["io_strategy"]
        
        return fields
    
    def create_object_from_data(self, data, io_strategy=None):
        
        role = data.get("type")
        cls_map = {"student": Student, "teacher": Teacher, "staff": Staff}
        cls = cls_map.get(role)
        
        if not cls:
            return None
        
        obj = cls(io_strategy=io_strategy)
        
        for field, value in data.items():
            if hasattr(obj, field) and field != "type" and field != "io_strategy":
                setattr(obj, field, value)
        
        return obj