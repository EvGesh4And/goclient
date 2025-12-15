class RestIO:

    def input(self, obj, field):
        label = obj.field_labels.get(field, field)
        return input(f"{label}: ")

    def output(self, obj, field):
        label = obj.field_labels.get(field, field)
        value = getattr(obj, field)
        print(f"{label}: {value}")