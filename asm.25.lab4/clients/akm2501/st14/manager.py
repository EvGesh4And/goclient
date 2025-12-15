from .employee import Employee


class Manager(Employee):
    FIELDS = dict(Employee.FIELDS)
    FIELDS.update({
        "team_size": int,
    })

    def __init__(self, io=None):
        super().__init__(io)
        self.team_size = 0