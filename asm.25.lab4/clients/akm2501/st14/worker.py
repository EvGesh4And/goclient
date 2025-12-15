from .employee import Employee


class Worker(Employee):
    FIELDS = dict(Employee.FIELDS)
    FIELDS.update({
        "department": str,
    })

    def __init__(self, io=None):
        super().__init__(io)
        self.department = ""