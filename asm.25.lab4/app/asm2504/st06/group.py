from flask import render_template
from flask import request

class group:
	def f(self):
		return render_template("asm2504/st06/index.html", s="asm2504.st06.group.f()", selfurl='/'+request.url_rule.rule.split('/')[1])
