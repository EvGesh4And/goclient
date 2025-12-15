from flask import render_template, request, redirect, url_for
import os

class WebIO:
    def input(self, field_name, default=""):
        return request.form.get(field_name, default)
    
    def output(self, message):
        return message
    
    def render_template(self, template_name, **context):
        # Простое имя файла
        return render_template(template_name, **context)
    
    def redirect(self, endpoint):
        return redirect(url_for(endpoint))