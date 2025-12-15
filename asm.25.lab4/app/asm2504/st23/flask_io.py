class FlaskIOStrategy:
    def input(self, obj, field):
        return ""

    def output(self, obj, field):
        pass

    def process_form_data(self, obj, form_data):
        if hasattr(obj, 'process_form_data'):
            return obj.process_form_data(form_data)
        return ["Объект не поддерживает обработку формы"]

    def prepare_for_display(self, obj, index=None):
        if hasattr(obj, 'prepare_for_display'):
            return obj.prepare_for_display(index)
        return None