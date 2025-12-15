
class FlaskIO:
    def get_fields(self, obj):
        fields = {}
        for attr in vars(obj):
            if attr not in ("io_strategy",'edit_field','output_data','input_data'):
                fields[attr] = getattr(obj, attr)
        return fields