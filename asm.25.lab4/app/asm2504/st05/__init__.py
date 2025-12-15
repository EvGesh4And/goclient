from flask import Flask, render_template

from .api.group import Group
from .io_handlers.io_handler import IOHandler
from .io_handlers.flask_handler import FlaskIOHandler
from .models.leader import Leader
from .models.student import Student
from .storage.pickle_storage import PickleStorage

app = Flask(__name__)

from .api import bp as api_bp

groups = [["group", api_bp, "/st05"]]

for title, bp, url in groups:
	app.register_blueprint(bp, url_prefix=url)

@app.route("/")
def index():
	r = ""
	for title, bp, url in groups:
		r += f'<a href="{url}">{title}</a><br>'
	return render_template("index.tpl", groups=r)
