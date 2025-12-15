from flask import render_template, request, redirect, url_for

class WebIO:
    def input(self, field_name, default=""):
        return request.form.get(field_name, default)
    
    def render_template(self, template_name, **context):
        return render_template(f'akm2501/st20/{template_name}', **context)
    
    def redirect(self, endpoint):
        return redirect(url_for(endpoint))