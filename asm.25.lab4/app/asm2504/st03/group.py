from flask import render_template, request

class group:
    def f(self):
        return render_template("asm2504/st03/index.tpl", s="st03.group.f()", selfurl='/'+request.url_rule.rule.split('/')[1])