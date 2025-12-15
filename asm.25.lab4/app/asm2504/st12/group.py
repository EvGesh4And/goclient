from flask import jsonify, render_template, request


class group:
    def f(self):
        prefix = request.path.rstrip("/") or "/"
        return render_template("asm2504/st12/index.html", selfurl=prefix)

    def api(self):
        return jsonify({"st": "asm2504.st12"})

