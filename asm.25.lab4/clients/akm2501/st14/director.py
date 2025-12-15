from .employee import Employee


class Director(Employee):
    FIELDS = dict(Employee.FIELDS)
    FIELDS.update({
        "has_company_car": bool,
    })

    def __init__(self, io=None):
        super().__init__(io)
        self.has_company_car = False